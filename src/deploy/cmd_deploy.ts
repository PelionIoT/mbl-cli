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

// deploy could rsync app files to docker container over ssh,
// perhaps watching for local file changes and updating automagically?

exports.command = "deploy [path] [device] [host]";
exports.desc = "Deploy an application to a device (building as necessary)";
exports.builder = {
    buildhost: {
        choices: [ "local", "remote" ],
        default: "local",
        description: "build the image locally or remotely"
    },
    device: {
        description: "address of the device"
    },
    path: {
        default: ".",
        description: "the directory to build or path of image to deploy"
    }
};
exports.handler = argv => {
    // scan for devices and give options to user using "inquirer" if count > 1
    // tslint:disable-next-line:no-console
    console.log(argv);
};
