/*
* Mbed Linux OS CLI
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

export const command = "run <command> [address]";
export const describe = "Run a command on a device";

export interface RunCommand extends DeviceCommand {
    command;
}

export const builder: RunCommand = {
    address: {
        description: "address of the device"
    },
    command: {
        description: "command to run"
    }
};

export function handler(args: RunCommand) {
    function execute(device: Device): Promise<void> {
        const ssh = new Ssh(device.address, device.port);
        return ssh.execute(args.command);
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

        return execute(device);
    })
    .then(() => process.exit())
    .catch(error => {
        if (error) log(error);
        process.exit(1);
    });
}
