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
import { join } from "path";
import { Stream } from "stream";
import { pack as packFS } from "tar-fs";
import {
    extract as extractStream,
    pack as packStream
} from "tar-stream";
import { DockerUtils } from "../util/docker";
import { qemuName, QemuUtils, toolsPath } from "../util/qemu";
import { PrettifyStream } from "../util/transform";

import * as Dockerode from "dockerode";

/**
 * Docker Builder
 */
export class DockerBuilder extends EventEmitter {
    /**
     * Log event
     * @event
     */
    public static EVENT_LOG: string = "log";

    /**
     * @param docker Instance of the docker API
     */
    constructor(private docker: Dockerode) {
        super();
    }

    /**
     * Run the build stream
     * @param sourceStream The stream to build
     * @param tag Image tag name
     * @param force No-cache force
     * @param needsQemu Flag if qemu is needed inside the new image
     */
    private buildStream(sourceStream: Stream, tag: string, force: boolean, needsQemu: boolean): Promise<void> {
        return new Promise((resolve, reject) => {

            const extract = extractStream();
            const dockerStream = packStream();

            // Add check for Dockerfile
            extract.on("entry", (header, stream, callback) => {
                if (needsQemu && header.name === "Dockerfile") {
                    let contents = "";

                    stream.on("data", chunk => {
                        contents += chunk.toString("utf8");
                    });

                    stream.on("end", () => {
                        // Add command to the Dockerfile
                        const index = contents.indexOf("RUN");
                        const command = `COPY ${join(toolsPath, qemuName)} /tmp/${qemuName}`;
                        contents = `${contents.substr(0, index)}\n${command}\n${contents.substr(index)}`;
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
            this.docker.buildImage(dockerStream, {
                nocache: force,
                t: tag,
            }, (error, response) => {
                if (error) {
                    return reject(error);
                }
                response
                .on("end", resolve)
                .on("error", reject)
                .pipe(new PrettifyStream())
                .pipe(process.stdout);
            });
        });
    }

    /**
     * Build a docker image
     * @param buildPath The directory to build
     * @param tag The name to use to tag the docker image
     * @param ignore A folder pattern to ignore
     */
    public build(buildPath: string, tag: string, qemu: QemuUtils, dockerUtils: DockerUtils, force: boolean = false, ignore: string = ".git"): Promise<any> {
        this.emit(DockerBuilder.EVENT_LOG, `building ${buildPath} with tag '${tag}'`);

        return dockerUtils.checkDocker(buildPath, this.docker)
        .then(() => qemu.setupQemu(buildPath))
        .then(needsQemu => {
            const source = packFS(buildPath, {
                ignore: name => {
                    return name.indexOf(ignore) >= 0;
                }
            });

            return this.buildStream(source, tag, force, needsQemu);
        });
    }
}
