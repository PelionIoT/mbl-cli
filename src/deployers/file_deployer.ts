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

import { EventEmitter } from "events";
import { createWriteStream, existsSync, lstatSync, mkdirSync } from "fs";
import { dirname, join } from "path";
import { DevNull } from "../utils/dev_null";
import { Deployer } from "./interface";

export const DEFAULT_IMAGE_NAME = "mbed-image.tar";

/**
 * File Deployer
 */
export class FileDeployer extends EventEmitter implements Deployer {

    /**
     * Log event
     * @event
     */
    public static EVENT_LOG: string = "log";

    /**
     * @param docker Instance of the docker API
     */
    constructor(private path: string) {
        super();
    }

    /**
     * Ensure a directory exists
     * @param directory The directory to check
     */
    private ensureDirectory(directory) {
        const dirName = dirname(directory);
        if (!existsSync(dirName)) {
            this.ensureDirectory(dirName);
        }
        if (existsSync(directory)) return;
        mkdirSync(directory);
    }

    /**
     * Deploy an image stream
     * @param fileName The file name to save the image to
     */
    public deploy(stream: NodeJS.ReadableStream): Promise<void> {
        return new Promise((resolve, reject) => {

            let sink = new DevNull();

            if (this.path) {
                // If existing directory passed in, add a filename
                if (existsSync(this.path) && lstatSync(this.path).isDirectory()) {
                    this.path = join(this.path, DEFAULT_IMAGE_NAME);
                }

                // Save file
                this.ensureDirectory(dirname(this.path));
                sink = createWriteStream(this.path);

                this.emit(FileDeployer.EVENT_LOG, `Saving to '${this.path}'...`);
            }

            stream.on("end", resolve)
            .on("error", reject)
            .pipe(sink);
        });
    }
}
