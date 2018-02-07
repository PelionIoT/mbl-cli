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

import { DEFAULT_IMAGE_NAME, ImageDeployer } from "../deploy/image_deployer";
import { log } from "../logger";
import { DockerUtils } from "../util/docker";
import { QemuUtils } from "../util/qemu";
import { DockerBuilder } from "./docker_builder";

export interface BuildCommand {
    directory;
    file;
    force;
    remote;
    tag;
}

export const command = "build [directory] [file]";
export const describe = "Build a directory and create an image";

export const builder: BuildCommand = {
    directory: {
        default: ".",
        description: "the directory to build"
    },
    file: {
        default: DEFAULT_IMAGE_NAME,
        description: "file or directory to save the image to"
    },
    force: {
        alias: "f",
        default: false,
        description: "force a rebuild",
        type: "boolean"
    },
    remote: {
        alias: "r",
        default: false,
        description: "build the image remotely",
        type: "boolean"
    },
    tag: {
        alias: "t",
        default: "mbed-app",
        description: "name and optional tag for the image in the form 'name:tag'"
    }
};

export function handler(argv: BuildCommand) {

    let remoteHost = "10.6.44.215";
    if (argv.remote) log(`using remote docker host ${remoteHost}`);
    else remoteHost = null;

    const dockerUtils = new DockerUtils();
    const docker = dockerUtils.createDockerode(remoteHost);
    const dockerBuilder: DockerBuilder = new DockerBuilder(docker);
    const imageDeployer: ImageDeployer = new ImageDeployer(docker);
    const qemuUtils = new QemuUtils(docker);

    dockerBuilder.addListener(DockerBuilder.EVENT_LOG, log);
    imageDeployer.addListener(ImageDeployer.EVENT_LOG, log);

    dockerBuilder.build(argv.directory, argv.tag, qemuUtils, dockerUtils, argv.force)
    .then(() => imageDeployer.deployStream(argv.tag, argv.file))
    .catch(error => log(`Error: ${error}`));
}
