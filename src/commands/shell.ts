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

import { Device, DeviceGetter } from "../device";
import { DeviceCommand } from "../deviceCommand";
import { log } from "../utils/logger";
import { Ssh } from "../utils/ssh";

export const command = "shell [address]";
export const describe = "Get a shell on a device";

export const builder: DeviceCommand = {
    address: {
        description: "address of the device"
    }
};

export function handler(args: DeviceCommand) {
    function shell(device: Device): Promise<void> {
        log(`Connecting to ${device.name}...`);
        const ssh = new Ssh(device.address);
        return ssh.shell();
    }

    Promise.resolve()
    .then(() => {
        if (args.address) {
            return {
                address: args.address,
                name: args.address
            };
        }

        const device = new DeviceGetter();
        return device.getDevice();
    })
    .then(device => {
        if (!device) {
            log("Error: No devices found");
            return;
        }

        return shell(device);
    })
    .then(() => process.exit())
    .catch(error => {
        if (error) log(error);
        process.exit(1);
    });
}
