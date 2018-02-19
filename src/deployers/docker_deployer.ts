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
import { Docker } from "../utils/docker";
import { Deployer } from "./interface";

export const DEFAULT_IMAGE_ADDRESS = "resin.local";

/**
 * Docker Deployer
 */
export class DockerDeployer extends EventEmitter implements Deployer {

    /**
     * Log event
     * @event
     */
    public static EVENT_LOG: string = "log";

    /**
     * @param docker Instance of the docker API
     */
    constructor(private docker: Docker) {
        super();
    }

    public deploy(stream: NodeJS.ReadableStream): Promise<any> {
        this.emit(DockerDeployer.EVENT_LOG, `Deploying to '${this.docker.host}'...`);
        return this.docker.deployImage(stream);
    }
}
