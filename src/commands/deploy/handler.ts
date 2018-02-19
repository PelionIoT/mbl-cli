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

import { createReadStream, existsSync, lstatSync } from "fs";
import { DockerDeployer } from "../../deployers/docker_deployer";
import { Deployer } from "../../deployers/interface";
import { Docker } from "../../utils/docker";
import { log } from "../../utils/logger";
import { Builder } from "../build/builder";
import { DeployCommand } from "./command";

export class Handler {

    private docker: Docker;

    public constructor(private args: DeployCommand) {
        this.docker = new Docker(this.args.address);
    }

    private getStream(): Promise<NodeJS.ReadableStream> {
        if (!existsSync(this.args.source)) {
            return Promise.reject(`Unable to find source '${this.args.source}'`);
            // Assume source is a URL or registry entry
            // return this.docker.deployImage(this.args.source);
        }

        if (lstatSync(this.args.source).isDirectory()) {
            // Build directory and return resulting stream
            const builder = new Builder(this.args);
            const streamToDevice = (this.args.address !== this.args.remote);

            return builder.build(streamToDevice);
        } else {
            // Return stream from file
            log(`Found application '${this.args.source}'`);
            const stream = createReadStream(this.args.source);
            return Promise.resolve(stream);
        }
    }

    public run() {
        const deployer: Deployer = new DockerDeployer(this.docker);
        deployer.addListener(DockerDeployer.EVENT_LOG, log);

        this.getStream()
        .then(imageStream => {

            return this.docker.inspectImage(true)
            .then(imageInfo => {
                log("Stopping any application...");
                return this.docker.stopContainer(true)
                .then(() => this.docker.deleteContainer(true))
                .then(() => {
                    if (imageInfo && imageInfo.Id) {
                        return this.docker.deleteImage(false, true, imageInfo.Id);
                    }
                })
                .then(() => {
                    if (imageStream) {
                        return deployer.deploy(imageStream);
                    }
                })
                .then(() => {
                    log("Starting application...");
                    return this.docker.createContainer();
                })
                .then(() => this.docker.startContainer())
                .then(() => {
                    if (!this.args.detached) {
                        return this.docker.attachContainer()
                        .then(() => log("Attached to application"));
                    }
                });
            });
        })
        .catch(error => log(`Error: ${error}`));
    }
}
