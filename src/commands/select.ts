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

import { DeviceConfig } from "../device";
import { Chooser } from "../utils/chooser";
import { ConfigStore } from "../utils/configStore";
import { Discovery } from "../utils/discovery";
import { log } from "../utils/logger";

export const command = "select";
export const describe = "Select a device";

export function handler() {
    const discovery = new Discovery();
    const chooser = new Chooser();
    const store = new ConfigStore<DeviceConfig>();

    log("Discovering devices...");
    discovery.discoverAll()
    .then(devices => {
        if (devices.length === 0) return log("Error: No devices found");

        devices.push({
            address: null,
            name: "No device",
        });

        return chooser.choose(devices, device => device.address ? `${device.name} (${device.address})` : `${device.name}`, "Select a device:")
        .then(device => store.save({
            selectedDevice: device.address ? device : null
        }));
    })
    .then(() => process.exit())
    .catch(error => {
        if (error) log(`Error: ${error}`);
        process.exit(1);
    });
}
