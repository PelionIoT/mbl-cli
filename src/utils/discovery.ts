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

import { Browser, createBrowser, tcp } from "mdns";
import { Device } from "../device";

const DEVICE_TYPE = "ssh";
const TEXT_RECORD = "mblos";

export class Discovery {

    private devices: Device[] = [];
    private finishFn = null;
    private timer = null;
    private browser: Browser = null;
    private found: boolean;

    constructor(private timeout: number = 90) {
    }

    private serviceUp(service) {
        if (service.txtRecord && TEXT_RECORD in service.txtRecord) {
            if (!service.addresses.length) {
                // If a device is found, but doesn't have an IP address, restart scan
                if (this.devices.length === 0) {
                    if (!this.found) {
                        // tslint:disable-next-line:no-console
                        console.log("Device found, awaiting IP address...");
                        this.found = true;
                    }
                    this.restart();
                }
                return;
            }

            this.devices.push({
                address: service.addresses[0],
                name: service.name
            });

            // Once found, wait a little longer for any other devices
            this.wait(0.5);
        }
    }

    private wait(millis: number = this.timeout * 1000) {
        clearTimeout(this.timer);
        if (this.finishFn) {
            this.timer = setTimeout(this.finishFn, millis);
        }
    }

    private restart() {
        setTimeout(this.start.bind(this), 500);
    }

    private start() {
        this.browser = createBrowser(tcp(DEVICE_TYPE));
        this.browser.on("serviceUp", this.serviceUp.bind(this));
        this.browser.start();
        this.wait();
    }

    public discoverAll(): Promise<Device[]> {
        return new Promise((resolve, _reject) => {

            this.finishFn = () => {
                this.browser.stop();
                resolve(this.devices);
            };

            this.start();
        });
    }
}
