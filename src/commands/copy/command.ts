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

import { DeviceCommand } from "../deviceCommand";
import { Handler } from "./handler";

export interface CopyCommand extends DeviceCommand {
    dest;
    src;
}

export const command = "copy <src> <dest> [address]";
export const describe = "Copy a file/folder to a device";

export const builder: CopyCommand = {
    address: {
        description: "address of the device"
    },
    dest: {
        description: "the destination for the file on the device"
    },
    src: {
        description: "the file to deploy"
    }
};

export function handler(args: CopyCommand) {
    new Handler(args).run();
}
