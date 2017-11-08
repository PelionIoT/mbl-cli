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

import { createWriteStream, existsSync, mkdirSync } from "fs";
import { dirname } from "path";
import { Stream } from "stream";

/**
 * Image Deployer
 */
export class ImageDeployer {

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
     * Deploy a build stream
     * @param stream The stream to deploy
     * @param fileName The file name to save the image to
     */
    public deployStream(stream: Stream, fileName?: string): Promise<any> {
        return new Promise((resolve, reject) => {
            if (fileName) {
                // Save file
                try {
                    this.ensureDirectory(dirname(fileName));
                    stream.pipe(createWriteStream(fileName));
                    resolve();
                } catch (error) {
                    reject(error);
                }
            } else {
                // Otherwise find  adevice to deploy to
            }
        });
    }
}
