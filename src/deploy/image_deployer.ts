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
import { DevNull } from "../util/dev_null";

import * as Dockerode from "dockerode";

export const DEFAULT_IMAGE_NAME = "mbed.image";

/**
 * Image Deployer
 */
export class ImageDeployer extends EventEmitter {

    /**
     * Log event
     * @event
     */
    public static EVENT_LOG: string = "log";

    /**
     * @param docker Instance of the docker API
     */
    constructor(private docker: Dockerode) {
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
     * Deploy a build stream
     * @param stream The stream to deploy
     * @param fileName The file name to save the image to
     */
    public deployStream(tag: string, fileName?: string): Promise<void> {
        return new Promise((resolve, reject) => {
            if (!tag) { reject("No image tag specified"); }

            let sink = new DevNull();
            if (fileName) {
                // If existing directory passed in, add a filename
                if (existsSync(fileName) && lstatSync(fileName).isDirectory()) {
                    fileName = join(fileName, DEFAULT_IMAGE_NAME);
                }

                // Save file
                this.ensureDirectory(dirname(fileName));
                sink = createWriteStream(fileName);

                this.emit(ImageDeployer.EVENT_LOG, `Saving '${tag}' to ${fileName}`);
            } else {
                // Otherwise find a device to deploy to
                this.emit(ImageDeployer.EVENT_LOG, `Sending '${tag}' to device`);
            }

            const image: Dockerode.Image = this.docker.getImage(tag);
            if (!image) { return reject("No image found"); }

            image
            .get()
            .then(stream => {
                stream.on("end", resolve)
                .on("error", reject)
                .pipe(sink);
            })
            .catch(reject);
        });
    }
}
