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

export interface Item {
    name: string;
}

export class Chooser {

    constructor(private autoSelect: boolean = false) {
    }

    public choose<T extends Item>(items: T[], titleFn: (item: T) => string, message: string): Promise<T> {
        return new Promise((resolve, reject) => {
            // Immeditely resolve with single or null result
            if (this.autoSelect && items.length <= 1) return resolve(items[0]);

            process.stdin.setRawMode(true);
            process.stdin.setEncoding("utf8");
            process.stdin.on("readable", () => {
                const input = process.stdin.read();
                if (input === "\u0003") {
                    process.stdin.setRawMode(false);
                    reject();
                } else if (input) {
                    const index = parseInt(input.toString());
                    if (index && index <= items.length) {
                        process.stdin.setRawMode(false);
                        resolve(items[index - 1]);
                    }
                }
            });

            // tslint:disable-next-line:no-console
            console.log(message);
            items.forEach((item, index) => {
                // tslint:disable-next-line:no-console
                console.log(`${index + 1}: ${titleFn(item)}`);
            });
        });
    }
}
