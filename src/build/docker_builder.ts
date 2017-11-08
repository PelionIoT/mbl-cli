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

import { createWriteStream, existsSync, mkdirSync } from "fs";
import { join } from "path";
import { Stream } from "stream";
import { pack as packFS } from "tar-fs";
import {
    extract as extractStream,
    pack as packStream
} from "tar-stream";
import { createGunzip } from "zlib";
import { prettifyStream } from "../util/transform";

import * as dockerode from "dockerode";
import * as request from "request";

export type typeEnum = "local" | "remote";

/**
 * Docker Builder
 */
export class DockerBuilder {

    private readonly toolsPath: string = ".mbed";
    private readonly qemuUrl: string = "https://github.com/resin-io/qemu/releases/download/v2.5.50-resin-execve/qemu-execve.gz";
    private readonly qemuName: string = "qemu-execve";

    /**
     * The docker API
     */
    private docker: dockerode;

    /**
     * Whether the docker build needs qemu injecting to run on a-class
     */
    private needsQemu: boolean;

    /**
     * @param host Where to undertake the build
     */
    constructor(host: typeEnum) {

        const options: { [key: string]: string | number } = {};

        if (host === "local") {
            options.socketPath = "/var/run/docker.sock";
        } else {
            options.dockerHost = "http://mbed.com";
            options.dockerPort = 2376;
        }

        this.docker = new dockerode(options);
    }

    /**
     * Check the docker architecture to see if we need injection
     */
    private checkQemu(): Promise<void> {
        return new Promise((resolve, reject) => {
            this.docker.version((error, info) => {
                if (error) {
                    return reject("No docker available!");
                }

                this.needsQemu = (info.Arch !== "ARM");
                resolve();
            });
        });
    }

    /**
     * Download qemu as necessary
     * @param buildPath The directory being built
     */
    private downloadQemu(buildPath: string): Promise<void> {
        return new Promise((resolve, reject) => {
            if (!this.needsQemu) {
                return resolve();
            }

            const toolsPath = `${join(buildPath, this.toolsPath)}`;
            const qemuPath = `${join(toolsPath, this.qemuName)}`;

            if (existsSync(qemuPath)) {
                return resolve();
            }

            if (!existsSync(toolsPath)) {
                mkdirSync(toolsPath);
            }

            request(this.qemuUrl)
                .pipe(createGunzip())
                .pipe(createWriteStream(qemuPath))
                .on("close", resolve)
                .on("error", reject);
        });
    }

    /**
     * Run the build stream
     * @param sourceStream The stream to build
     */
    private buildStream(sourceStream: Stream, tag: string, force: boolean): Promise<Stream> {
        return new Promise((resolve, reject) => {

            const extract = extractStream();
            const imageStream = packStream();

            // Add check for Dockerfile
            extract.on("entry", (header, stream, callback) => {
                if (this.needsQemu && header.name === "Dockerfile") {
                    let contents = "";

                    stream.on("data", chunk => {
                        contents += chunk.toString("utf8");
                    });

                    stream.on("end", () => {
                        // Add command to the Dockerfile
                        const index = contents.indexOf("RUN");
                        const command = `COPY ${join(this.toolsPath, this.qemuName)} /tmp/${this.qemuName}`;
                        contents = `${contents.substr(0, index)}\n${command}\n${contents.substr(index)}`;
                        imageStream.entry({ name: header.name }, contents);
                        callback();
                    });
                    return;
                }

                stream.pipe(imageStream.entry(header, callback));
            });

            extract.on("finish", () => {
                imageStream.finalize();
                resolve(imageStream);
            });

            sourceStream.pipe(extract);
            this.docker.buildImage(imageStream, {
                nocache: force,
                t: tag,
            }, (error, response) => {
                if (error) {
                    return reject(error);
                }
                response
                    .pipe(prettifyStream)
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
    public build(buildPath: string, tag: string, force: boolean = false, ignore: string = ".git"): Promise<any> {
        return this.checkQemu()
        .then(() => this.downloadQemu(buildPath))
        .then(() => {
            const source = packFS(buildPath, {
                ignore: name => {
                    return name.indexOf(ignore) >= 0;
                }
            });

            return this.buildStream(source, tag, force);
        });
    }
}
