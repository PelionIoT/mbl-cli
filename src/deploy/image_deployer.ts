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
import { DevNull } from "../util/dev_null";

import * as Dockerode from "dockerode";

/**
 * Image Deployer
 */
export class ImageDeployer {
    /**
     * @param docker Instance of the docker API
     */
    constructor(private docker: Dockerode) {
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
                // Save file
                this.ensureDirectory(dirname(fileName));
                sink = createWriteStream(fileName);
            } else {
                // Otherwise find a device to deploy to
            }

            const image: Dockerode.Image = this.docker.getImage(tag);
            if (!image) { return reject("No image found"); }
            if (sink instanceof DevNull) { return resolve(); }

            image
            .get()
            .then(stream => {
                // tslint:disable-next-line:no-console
                console.log("Deploying image..");
                stream.on("end", resolve)
                .on("error", reject)
                .pipe(sink);
            });
        });
    }
}
