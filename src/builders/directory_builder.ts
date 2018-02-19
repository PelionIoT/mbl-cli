/*
* Mbed Linux CLI
* Copyright ARM Limited 2017
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

import { EventEmitter } from "events";
import { existsSync } from "fs";
import { basename, join } from "path";
import { Stream } from "stream";
import { pack as packFS } from "tar-fs";
import {
    extract as extractStream,
    pack as packStream
} from "tar-stream";
import { Docker } from "../utils/docker";
import { PrettifyStream } from "../utils/transform";
import { Builder } from "./interface";

/**
 * Directory Builder
 */
export class DirectoryBuilder extends EventEmitter implements Builder {
    /**
     * Log event
     * @event
     */
    public static EVENT_LOG: string = "log";

    /**
     * @param docker Instance of the docker API
     */
    constructor(private docker: Docker, private useEmulation: boolean = true) {
        super();
    }

    /**
     * Run the build stream
     * @param sourceStream The stream to build
     * @param force No-cache force
     * @param needsEmulation Flag if emulation is needed while building the new image
     */
    private buildStream(sourceStream: Stream, force: boolean, needsEmulation: boolean): Promise<void> {
        return new Promise((resolve, reject) => {

            const extract = extractStream();
            const dockerStream = packStream();

            // Add check for Dockerfile
            extract.on("entry", (header, stream, callback) => {
                if (needsEmulation && header.name === "Dockerfile") {
                    let contents = "";

                    stream.on("data", chunk => {
                        contents += chunk.toString("utf8");
                    });

                    stream.on("end", () => {
                        // Add commands to the Dockerfile
                        // const copyCommand = `COPY ./${join(toolsPath, binPath)}/ /usr/bin/`;
                        const startCommand = `RUN [ "cross-build-start" ]`;
                        const endCommand = `RUN [ "cross-build-end" ]`;
                        contents = contents.replace(/^FROM.*$/im, match => `${match}\n${startCommand}`);
                        contents += `\n${endCommand}`;
                        dockerStream.entry({ name: header.name }, contents);
                        callback();
                    });
                    return;
                }

                stream.pipe(dockerStream.entry(header, callback));
            });

            extract.on("finish", () => {
                dockerStream.finalize();
            });
            sourceStream.pipe(extract);

            this.docker.buildImage(dockerStream, force)
            .then(response => {
                response
                .on("end", resolve)
                .on("error", reject)
                .pipe(new PrettifyStream())
                .pipe(process.stdout);
            })
            .catch(error => reject(error));
        });
    }

    /**
     * Build a docker image
     * @param buildPath The directory to build
     * @param ignore A folder pattern to ignore
     */
    public build(buildPath: string, force: boolean = false, ignore: string[] = [ ".git" ]): Promise<void> {
        this.emit(DirectoryBuilder.EVENT_LOG, `Building '${buildPath}'...`);

        return this.checkDocker(buildPath)
        .then(() => this.requiresEmulation())
        .then(needsEmulation => {
            const source = packFS(buildPath, {
                ignore: name => {
                    return ignore.indexOf(basename(name)) >= 0;
                }
            });

            return this.buildStream(source, force, needsEmulation);
        });
    }

    public requiresEmulation(arch: string = "arm"): Promise<boolean> {
        return new Promise((resolve, reject) => {
            if (!this.useEmulation) return resolve(false);

            this.docker.getVersion()
            .then(info => {
                resolve(info.Arch !== arch);
            })
            .catch(() => reject("No docker available"));
        });
    }

    public checkDocker(buildPath: string): Promise<void> {
        return new Promise((resolve, reject) => {
            const dockerFile = join(buildPath, "Dockerfile");
            if (!existsSync(dockerFile)) reject("Dockerfile not found, check directory is a valid Mbed Linux application");

            this.docker.getVersion()
            .then(() => resolve())
            .catch(() => reject("Docker not found, check it's installed and running or build using a remote host"));
        });
    }
}
