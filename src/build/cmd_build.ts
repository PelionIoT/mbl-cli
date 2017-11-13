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

import { ImageDeployer } from "../deploy/image_deployer";
import { createDockerode } from "../util/docker_factory";
import { QemuUtils } from "../util/qemu";
import { DockerBuilder } from "./docker_builder";

exports.command = "build [path] [file] [host] [tag] [force]";
exports.desc = "Build a directory and output a docker image";
exports.builder = {
    buildhost: {
        choices: [ "local", "remote" ],
        default: "local",
        description: "build the image locally or remotely"
    },
    file: {
        default: null,
        description: "path to save image to"
    },
    force: {
        default: false,
        description: "force a rebuild",
        type: "boolean"
    },
    path: {
        default: ".",
        description: "the directory to build"
    },
    tag: {
        default: "mbed-app",
        description: "The tag name for the image"
    }
};
exports.handler = argv => {
    const docker = createDockerode(argv.buildhost);
    const dockerBuilder: DockerBuilder = new DockerBuilder(docker);
    const imageDeployer: ImageDeployer = new ImageDeployer(docker);
    const qemuUtils: QemuUtils = new QemuUtils(docker);

    dockerBuilder.build(argv.path, argv.tag, qemuUtils, argv.force)
    .then(() => imageDeployer.deployStream(argv.tag, argv.file))
        // tslint:disable-next-line:no-console
    .catch(error => console.log(error));
};
