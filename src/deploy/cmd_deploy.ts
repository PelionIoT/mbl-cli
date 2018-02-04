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

// deploy could rsync app files to docker container over ssh,
// perhaps watching for local file changes and updating automagically?

import { log } from "../logger";

export interface DeployCommand {
    address;
    force;
    path;
    remote;
    tag;
}

export const command = "deploy [path] [address]";
export const describe = "Deploy a directory or image to a device";

export const builder: DeployCommand = {
    address: {
        description: "address of the device"
    },
    force: {
        alias: "f",
        default: false,
        description: "force a rebuild",
        type: "boolean"
    },
    path: {
        default: ".",
        description: "the directory or image path to deploy"
    },
    remote: {
        alias: "r",
        default: false,
        description: "build the image remotely",
        type: "boolean"
    },
    tag: {
        alias: "t",
        default: "mbed-app",
        description: "the tag name for the image"
    }
};

export function handler(argv: DeployCommand) {
    // scan for devices and give options to user using "inquirer" if count > 1
    log(`command not implemented ${JSON.stringify(argv)}`);
}
