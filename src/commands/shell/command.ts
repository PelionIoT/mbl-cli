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

import { DeviceGetter } from "../../device";
import { log } from "../../utils/logger";
import { SSH } from "../../utils/ssh";
import { DeviceCommand } from "../deviceCommand";

export const command = "shell [address]";
export const describe = "Get a shell on a device";

export const builder: DeviceCommand = {
    address: {
        description: "address of the device"
    }
};

export function handler(args: DeviceCommand) {

    function connect(address: string): Promise<void> {
        log(`Connecting to ${address}...`);
        const ssh = new SSH(address);
        return ssh.interact();
    }

    Promise.resolve()
    .then(() => {
        if (args.address) return args.address;

        const device = new DeviceGetter();
        return device.getAddress();
    })
    .then(address => {
        if (!address) {
            log("Error: No devices found");
            return;
        }

        return connect(address);
    })
    .then(() => process.exit())
    .catch(error => {
        if (error) log(error);
        process.exit(1);
    });
}
