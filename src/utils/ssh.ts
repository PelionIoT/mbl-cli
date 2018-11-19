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

import { EventEmitter } from "events";
import { existsSync } from "fs";
import { basename, join, normalize } from "path";
import { Client } from "ssh2";

export class Ssh extends EventEmitter {

    constructor(private host: string, private username: string = "root", private port: number = 22) {
        super();
    }

    private getSsh(): Promise<Client> {
        return new Promise((resolve, reject) => {
            const ssh = new Client();

            ssh.on("error", error => reject(error.message));
            ssh.on("ready", () => {
                resolve(ssh);
            });

            ssh.connect({
                host: this.host,
                port: this.port,
                username: this.username,
            });
        });
    }

    public shell(): Promise<void> {
        return this.getSsh()
        .then(ssh => {
            return new Promise<void>((resolve, reject) => {
                ssh.on("close", () => resolve());
                ssh.shell((error, stream) => {
                    if (error) return reject(error.message);

                    stream.on("close", () => {
                        ssh.end();
                    });

                    process.stdin.setRawMode(true);
                    process.stdin.setEncoding("utf8");
                    process.stdin.pipe(stream.stdin, { end: false });
                    stream.stdout.pipe(process.stdout, { end: false });
                    stream.stderr.pipe(process.stderr);
                });
            });
        });
    }

    public execute(command: string): Promise<void> {
        return this.getSsh()
        .then(ssh => {
            return new Promise<void>((resolve, reject) => {
                ssh.on("close", () => resolve());
                ssh.exec(command, (error, stream) => {
                    if (error) return reject(error.message);

                    stream.on("close", () => {
                        ssh.end();
                    });

                    stream.stdout.pipe(process.stdout);
                    stream.stderr.pipe(process.stderr);
                });
            });
        });
    }

    public get(source: string, destination?: string): Promise<void> {
        if (!destination) {
            destination = join(process.cwd(), "/");
        }

        if (destination.endsWith("/")) {
            destination = join(destination, basename(source));
        }

        return this.getSsh()
        .then(ssh => {
            return new Promise<void>((resolve, reject) => {
                ssh.on("close", () => resolve());
                ssh.sftp((error, sftp) => {
                    if (error) return reject(error.message);

                    sftp.fastGet(source, destination, {
                        step: (_totalTransferred, chunk, total) => {
                            this.emit("progress", {
                                chunk,
                                total
                            });
                        }
                    }, err => {
                        if (err) return reject(err.message);
                        ssh.end();
                    });
                });
            });
        });
    }

    public put(source: string, destination?: string): Promise<void> {
        if (!existsSync(source)) {
            source = normalize(join(process.cwd(), source));
            if (!existsSync(source)) return Promise.reject("local file doesn't exist");
        }

        if (!destination) {
            destination = basename(source);
        } else if (destination.endsWith("/")) {
            destination = join(destination, basename(source));
        }

        return this.getSsh()
        .then(ssh => {
            return new Promise<void>((resolve, reject) => {
                ssh.on("close", () => resolve());
                ssh.sftp((error, sftp) => {
                    if (error) return reject(error.message);

                    sftp.fastPut(source, destination, {
                        step: (_totalTransferred, chunk, total) => {
                            this.emit("progress", {
                                chunk,
                                total
                            });
                        }
                    }, err => {
                        if (err) return reject(err.message);
                        ssh.end();
                    });
                });
            });
        });
    }
}
