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

import { DEFAULT_IMAGE_ADDRESS } from "../../deployers/docker_deployer";
import { BuildArgs } from "../build/builder";
import { Handler } from "./handler";

export interface DeployCommand extends BuildArgs {
    address;
    detached;
}

export const command = "deploy [source] [address]";
export const describe = "Deploy an application to a device";

export const builder: DeployCommand = {
    address: {
        default: DEFAULT_IMAGE_ADDRESS,
        description: "address of the device to deploy to"
    },
    detached: {
        alias: "d",
        default: false,
        description: "don't attach to application output"
    },
    force: {
        alias: "f",
        default: false,
        description: "force a rebuild if building",
        type: "boolean"
    },
    noemulation: {
        alias: "n",
        default: false,
        description: "turn off emulation if building",
        type: "boolean"
    },
    remote: {
        alias: "r",
        default: false,
        description: "build any image remotely"
    },
    source: {
        default: ".",
        description: "the application path or source to deploy"
    }
};

export function handler(args: DeployCommand) {
    new Handler(args).run();
}
