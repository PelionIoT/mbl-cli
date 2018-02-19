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

import { DEFAULT_IMAGE_ADDRESS } from "../../../deployers/docker_deployer";
import { Docker } from "../../../utils/docker";
import { log } from "../../../utils/logger";

export const command = "stop [address]";
export const describe = "Stop the application on a device";

export interface DeviceCommand {
    address;
}

export const builder: DeviceCommand = {
    address: {
        default: DEFAULT_IMAGE_ADDRESS,
        description: "address of the device"
    }
};

export function handler(args: DeviceCommand) {
    const docker = new Docker(args.address);

    docker.stopContainer()
    .catch(error => log(`Error: ${error}`));
}
