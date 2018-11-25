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

import { Chooser } from "./utils/chooser";
import { ConfigStore } from "./utils/configStore";
import { Discovery } from "./utils/discovery";
import { log } from "./utils/logger";

export interface Device {
    name: string;
    address: string;
    port?: number;
}

export interface DeviceConfig {
    selectedDevice: Device;
}

export class DeviceGetter {
    private discovery = new Discovery();
    private chooser = new Chooser(true);
    private store = new ConfigStore<DeviceConfig>();

    public getDevice(): Promise<Device> {
        const config = this.store.load();
        if (config && config.selectedDevice) return Promise.resolve(config.selectedDevice);

        log("Discovering devices...");
        return this.discovery.discoverAll()
        .then(devices => {
            if (devices.length === 0) return null;
            return this.chooser.choose(devices, device => `${device.name} (${device.address})`, "Select a device:");
        });
    }
}
