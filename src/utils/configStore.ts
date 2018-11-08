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

import { existsSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";

const CONFIG_FILE = join(__dirname, ".mbl.cfg");

export class ConfigStore<T> {
    public load(): T {
        let data = "{}";

        if (existsSync(CONFIG_FILE)) {
            data = readFileSync(CONFIG_FILE).toString();
        }

        return JSON.parse(data);
    }

    public save(configuration: T): void {
        const data = JSON.stringify(configuration);
        writeFileSync(CONFIG_FILE, data);
    }
}
