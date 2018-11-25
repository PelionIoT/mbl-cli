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

import * as progress from "progress";
import { log } from "util";
import { Device, DeviceGetter } from "../device";
import { CopyCommand } from "../deviceCommand";
import { Ssh } from "../utils/ssh";

export const command = "get <src> [dest] [address]";
export const describe = "Copy a file from a device";

export const builder: CopyCommand = {
    address: {
        description: "address of the device"
    },
    dest: {
        description: "the local destination for the file"
    },
    src: {
        description: "the remote file to copy"
    }
};

export function handler(args: CopyCommand) {
    const put = (device: Device): Promise<void> => {
        const ssh = new Ssh(device.address, device.port);
        let progressBar = null;

        ssh.on("progress", (event: { chunk: number, total: number }) => {
            if (progressBar === null) {
                progressBar = new progress(`Copying [:bar] :percent :etas`, {
                    complete: "=",
                    incomplete: " ",
                    total: event.total,
                    width: 20
                });
            }

            progressBar.tick(event.chunk);
        });

        return ssh.get(args.src, args.dest);
    };

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

        return put(device);
    })
    .then(() => process.exit())
    .catch(error => {
        if (error) log(error);
        process.exit(1);
    });
}
