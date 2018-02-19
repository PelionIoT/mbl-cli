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

import * as Dockerode from "dockerode";
import { EventEmitter } from "events";

const DEFAULT_DOCKER_PORT = 2375;
const DEFAULT_IMAGE_NAME = "mbed-app";

export class Docker extends EventEmitter {

    private _host?: string;
    private docker: Dockerode = null;

    /**
     * Docker constructor
     * @param host The host to use in the host:port format (defaults to local machine)
     */
    public constructor(host?: string) {
        super();

        const options: { [key: string]: string | number } = {};
        if (host) {
            const parts = host.split(":");
            options.host = this._host = parts[0];
            options.port = parts[1] || DEFAULT_DOCKER_PORT;
        } else {
            options.socketPath = "/var/run/docker.sock";
        }

        this.docker = new Dockerode(options);
    }

    /**
     * Get docker host
     */
    get host() {
        return this._host || "local";
    }

    /**
     * Get docker version
     * https://docs.docker.com/engine/api/v1.35/#operation/SystemVersion
     *
     * @returns Promise of version
     */
    public getVersion(): Promise<{
        "Version": string;
        "Os": string;
        "Arch": string;
        "ApiVersion": string;
    }> {
        return this.docker.version();
    }

    /**
     * Get docker information
     * https://docs.docker.com/engine/api/v1.35/#operation/SystemInfo
     *
     * @returns Promise of information
     */
    public getInfo(): Promise<{}> {
        return this.docker.info();
    }

    /**
     * Build a docker image
     * https://docs.docker.com/engine/api/v1.35/#operation/ImageBuild
     *
     * @param source A path, URL or stream of a tar file to use as a build context
     * @param name A name and optional tag to apply to the image in the name:tag format
     * @param force Whether to force a rebuild
     * @returns Promise of Stream
     */
    public buildImage(source: NodeJS.ReadableStream | string, force: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<NodeJS.ReadableStream> {
        let options: {} = {
            nocache: force,
            t: name
        };

        // Use a remote tar URL instead of a local build context
        if (typeof source === "string" && source.indexOf("http") === 0) {
            options = {
                ...options,
                remote: source
            };
            source = null;
        }

        return this.docker.buildImage(source, options)
        .then(stream => {
            this.docker.modem.followProgress(stream, error => {
                if (error) stream.emit("error", error);
            });

            return stream;
        });
    }

    /**
     * Deploy a docker image
     * https://docs.docker.com/engine/api/v1.35/#operation/ImageCreate
     * https://docs.docker.com/engine/api/v1.35/#operation/ImageLoad
     *
     * @param image A path, URL or stream of a tar file to use as a build context
     * @param name A name and optional tag to apply to the image in the name:tag format
     * @param force Whether to force a rebuild
     * @returns Promise of Stream
     */
    public deployImage(image: NodeJS.ReadableStream | string, name: string = DEFAULT_IMAGE_NAME): Promise<NodeJS.ReadableStream> {
        if (typeof image === "string") {
            let options: {} = {};

            if (image.indexOf("http") === 0) {
                // Assume we are deploying a remote image from a URL
                options = {
                    fromSrc: image
                };
            } else {
                // Otherwise try deploying a remote image from a registry
                options = {
                    fromImage: image
                };
            }

            return new Promise((resolve, reject) => {
                return this.docker.createImage(options)
                .then(stream => {
                    stream.on("end", () => resolve());
                })
                .catch(error => reject(error));
            })
            .then(() => this.docker.getImage(image).tag({
                repo: name
            }));
        }

        // Stream the image to the device
        return this.docker.loadImage(image)
        .then(stream => {
            this.docker.modem.followProgress(stream, error => {
                if (error) stream.emit("error", error);
            });

            return stream;
        });
    }

    /**
     * Inspect a docker image
     * https://docs.docker.com/engine/api/v1.35/#operation/ImageInspect
     *
     * @param ignoreError Whether to ignore any errors
     * @param name The image name to inspect
     * @returns Promise of inspection info
     */
    public inspectImage(ignoreErrors: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<Dockerode.ImageInspectInfo> {
        return new Promise((resolve, reject) => {
            this.docker.getImage(name).inspect()
            .then(info => resolve(info))
            .catch(error => ignoreErrors ? resolve() : reject(error.reason || error));
        });
    }

    /**
     * Get a docker image
     * https://docs.docker.com/engine/api/v1.35/#operation/ImageGet
     *
     * @param ignoreError Whether to ignore any errors
     * @param name The image name to get
     * @returns Promise of image stream
     */
    public getImage(ignoreErrors: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<NodeJS.ReadableStream> {
        return new Promise((resolve, reject) => {
            this.docker.getImage(name).get()
            .then(stream => resolve(stream))
            .catch(error => ignoreErrors ? resolve() : reject(error.reason || error));
        });
    }

    /**
     * Delete a docker image
     * https://docs.docker.com/engine/api/v1.35/#operation/ImageDelete
     *
     * @param ignoreError Whether to ignore any errors
     * @param name The image name to delete
     * @returns Promise
     */
    public deleteImage(ignoreErrors: boolean = false, force: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<void> {
        return new Promise((resolve, reject) => {
            this.docker.getImage(name).remove({
                force
            })
            .then(() => resolve())
            .catch(error => ignoreErrors ? resolve() : reject(error.reason || error));
        });
    }

    /**
     * Create a docker container
     * https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate
     *
     * @param name The image name and optional tag to create from in the name:tag format
     * @returns Promise of Container
     */
    public createContainer(name: string = DEFAULT_IMAGE_NAME, privileged: boolean = true): Promise<Dockerode.Container> {
        return this.docker.createContainer({
            HostConfig: {
                NetworkMode: "host",
                Privileged: privileged,
                /*
                RestartPolicy: {
                    MaximumRetryCount: 0,
                    Name: "always"
                }
                */
            },
            Image: name,
            name
        });
    }

    /**
     * Start a docker container
     * https://docs.docker.com/engine/api/v1.35/#operation/ContainerStart
     *
     * @param ignoreError Whether to ignore any errors
     * @param name The container name to start
     * @returns Promise
     */
    public startContainer(ignoreErrors: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<void> {
        return new Promise((resolve, reject) => {
            this.docker.getContainer(name).start()
            .then(() => resolve())
            .catch(error => ignoreErrors ? resolve() : reject(error.reason || error));
        });
    }

    /**
     * Stop a docker container
     * https://docs.docker.com/engine/api/v1.35/#operation/ContainerStop
     *
     * @param ignoreError Whether to ignore any errors
     * @param name The container name to stop
     * @returns Promise
     */
    public stopContainer(ignoreErrors: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<void> {
        return new Promise((resolve, reject) => {
            this.docker.getContainer(name).stop()
            .then(() => resolve())
            .catch(error => ignoreErrors ? resolve() : reject(error.reason || error));
        });
    }

    /**
     * Restart a docker container
     * https://docs.docker.com/engine/api/v1.35/#operation/ContainerRestart
     *
     * @param ignoreError Whether to ignore any errors
     * @param name The container name to restart
     * @returns Promise
     */
    public restartContainer(ignoreErrors: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<void> {
        return new Promise((resolve, reject) => {
            this.docker.getContainer(name).restart()
            .then(() => resolve())
            .catch(error => ignoreErrors ? resolve() : reject(error.reason || error));
        });
    }

    /**
     * Delete a docker container
     * https://docs.docker.com/engine/api/v1.35/#operation/ContainerDelete
     *
     * @param ignoreError Whether to ignore any errors
     * @param name The container name to delete
     * @returns Promise
     */
    public deleteContainer(ignoreErrors: boolean = false, force: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<void> {
        return new Promise((resolve, reject) => {
            this.docker.getContainer(name).remove({
                force
            })
            .then(() => resolve())
            .catch(error => ignoreErrors ? resolve() : reject(error.reason || error));
        });
    }

    /**
     * Inspect a docker container
     * https://docs.docker.com/engine/api/v1.35/#operation/ContainerInspect
     *
     * @param ignoreError Whether to ignore any errors
     * @param name The container name to inspect
     * @returns Promise of inspection info
     */
    public inspectContainer(ignoreErrors: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<Dockerode.ContainerInspectInfo> {
        return new Promise((resolve, reject) => {
            this.docker.getContainer(name).inspect()
            .then(info => resolve(info))
            .catch(error => ignoreErrors ? resolve() : reject(error.reason || error));
        });
    }

    /**
     * Attach to a docker container
     * https://docs.docker.com/engine/api/v1.35/#operation/ContainerAttach
     *
     * @param name The container name to attach to
     * @returns Promise of stream
     */
    public attachContainer(name: string = DEFAULT_IMAGE_NAME): Promise<void> {
        const container = this.docker.getContainer(name);

        return container.attach({
            logs: true,
            stderr: true,
            stdout: true,
            stream: true
        })
        .then(stream => container.modem.demuxStream(stream, process.stdout, process.stderr));
    }

    /**
     * Get logs from a docker container
     * https://docs.docker.com/engine/api/v1.35/#operation/ContainerLogs
     *
     * @param attach Whether to attach to the container output
     * @param name The container name to get logs from
     * @returns Promise of stream
     */
    public getContainerLogs(attach: boolean = false, name: string = DEFAULT_IMAGE_NAME): Promise<void> {
        const container = this.docker.getContainer(name);

        return container.logs({
            follow: attach,
            stderr: true,
            stdout: true
        })
        .then(stream => container.modem.demuxStream(stream, process.stdout, process.stderr));
    }
}
