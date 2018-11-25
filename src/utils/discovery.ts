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

import * as mdns from "mdns-server";
import { isIPv6 } from "net";
import { Device } from "../device";

const DEVICE_TYPE = "._ssh._tcp.local";
const TEXT_RECORD = "mblos";
const SCAN_DELAY = 500;

export class Discovery {

    private devices: { [key: string]: Device } = {};
    private finishFn = null;
    private finishTimer = null;
    private scanTimer = null;
    private browser = null;
    private scanning = false;

    constructor(private timeout: number = 60) {
    }

    private wait(millis: number = this.timeout * 1000) {
        clearTimeout(this.finishTimer);
        if (this.finishFn) {
            this.finishTimer = setTimeout(this.finishFn, millis);
        }
    }

    private scan() {
        this.browser = mdns({
            loopback: true,
            noInit: true,
            reuseAddr: true
        });

        this.browser.on("response", this.onResponse.bind(this));

        this.browser.once("ready", () => {
            if (this.scanning) {
                this.scanTimer = setTimeout(() => {
                    this.browser.destroy(this.scan.bind(this));
                }, SCAN_DELAY);
            }

            this.browser.query({
                questions: [ {
                    name: DEVICE_TYPE,
                    type: "PTR"
                } ]
            });
        });

        this.browser.initServer();
    }

    private onResponse(response, info) {
        const service = {
            addresses: [],
            name: null,
            networkInterface: info.interface,
            port: 22,
            txtRecord: []
        };

        response.answers.forEach(answer => {
            switch (answer.type) {
                case "PTR":
                    const name = answer.data.toString();
                    const offset = name.indexOf(DEVICE_TYPE);
                    if (offset > 0) service.name = name.substring(0, offset);
                    break;
                case "TXT":
                    service.txtRecord.push(answer.data.toString("utf8", 1));
                    break;
                case "SRV":
                    service.port = answer.data.port;
                    break;
                case "A":
                case "AAAA":
                    service.addresses.push(answer.data.toString());
                    break;
            }
        });

        // We found an Mbed Linux device
        if (service.name && service.addresses.length && service.txtRecord.length && service.txtRecord.indexOf(TEXT_RECORD) > -1) {

            // Find IPv6 address
            let address = service.addresses.find(ipAddress => isIPv6(ipAddress));
            if (!address) {
                // If not found, use the first IPv4 address
                address = service.addresses[0];
            } else if (service.networkInterface) {
                // Fully quality the IPv6 address
                address += `%${service.networkInterface}`;
            }

            this.devices[service.name] = {
                address,
                name: service.name,
                port: service.port
            };

            // Once found, wait a little longer for any other devices
            this.wait(200);
        }
    }

    public discoverAll(): Promise<Device[]> {
        return new Promise((resolve, _reject) => {

            this.finishFn = () => {
                this.scanning = false;
                if (this.scanTimer) clearTimeout(this.scanTimer);
                if (this.browser) this.browser.destroy();
                resolve(Object.keys(this.devices).map(key => this.devices[key]));
            };

            this.scanning = true;
            this.scan();
            this.wait();
        });
    }
}
