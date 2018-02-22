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

import { DEFAULT_IMAGE_NAME } from "../../deployers/file_deployer";
import { BuildArgs } from "./builder";
import { Handler } from "./handler";

export interface BuildCommand extends BuildArgs {
    path;
}

export const command = "build [source] [path]";
export const describe = "Build an application from source";

export const builder: BuildCommand = {
    force: {
        alias: "f",
        default: false,
        description: "force a complete rebuild",
        type: "boolean"
    },
    noemulation: {
        alias: "n",
        default: false,
        description: "turn off emulation during build",
        type: "boolean"
    },
    path: {
        default: DEFAULT_IMAGE_NAME,
        description: "file or directory to save to"
    },
    remote: {
        alias: "r",
        default: false,
        description: "build the application remotely",
    },
    source: {
        default: ".",
        description: "the source to build"
    }
};

export function handler(args: BuildCommand) {
    new Handler(args).run();
}
