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

import { Transform } from "stream";

/**
 * PrettifyStream
 */
export class PrettifyStream extends Transform {
    /**
     * @param options Stream options
     */
    constructor(options?) {
        super(options);
    }

    /**
     * @param chunk Buffer or string data chunk
     * @param encoding Encoding of chunk
     * @param callback Callback func
     */
    // tslint:disable-next-line:no-empty
    public _transform(chunk: Buffer | string, encoding: string, callback: any = () => {} ) {
        if (!chunk) { return null; }
        if (encoding !== "buffer") {
            return callback(null, (chunk as Buffer).toString(encoding));
        }

        const chunkStr: string = chunk.toString();

        if (chunkStr.indexOf("{") < 0) {
            this.push(chunkStr);
            return callback();
        } else {
            chunkStr.split("\n").forEach(strObj => {
                if (!strObj) { return null; }
                const { stream = "" } = JSON.parse(strObj);
                this.push(stream);
            });
        }

        callback();
    }
}
