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
import { join } from "path";
import { createGunzip } from "zlib";

import * as Dockerode from "dockerode";
import * as request from "request";

export const toolsPath: string = ".mbed";
export const qemuName: string = "qemu-execve";
export const qemuUrl: string = "https://github.com/resin-io/qemu/releases/download/v2.5.50-resin-execve/qemu-execve.gz";

/**
 * QemuUtils
 */
export class QemuUtils {
    constructor(private docker: Dockerode) {}

    /**
     * @param buildPath Image build path
     */
    public setupQemu(buildPath: string): Promise<boolean> {
        return this.check()
        .then(needsQemu => {
            if (!needsQemu) return false;
            return this.download(buildPath)
            .then(() => {
                return true;
            });
        });
    }

    private check(): Promise<boolean> {
        return new Promise((resolve, reject) => {
            this.docker.version((error, info) => {
                if (error) return reject("No docker available");
                resolve(info.Arch !== "arm64");
            });
        });
    }

    /**
     * @param buildPath Image build path
     */
    private download(buildPath: string): Promise<void> {
        return new Promise((resolve, reject) => {

            const mbedPath = join(buildPath, toolsPath);
            const qemuPath = join(mbedPath, qemuName);

            if (existsSync(qemuPath)) return resolve();
            if (!existsSync(mbedPath)) mkdirSync(mbedPath);

            request(qemuUrl)
            .pipe(createGunzip())
            .pipe(createWriteStream(qemuPath))
            .on("close", resolve)
            .on("error", reject);
        });
    }
}
