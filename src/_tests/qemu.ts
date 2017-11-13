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

import { assert } from "chai";
import { suite, test } from "intern/lib/interfaces/tdd";
import { QemuUtils } from "../util/qemu";

suite("setupQemu", () => {
    const docker: any = {
        version: {}
    };

    test("Should reject if no docker is available", () => {
        docker.version = (some: (err, info) => {}) => { some("error", ""); };

        new QemuUtils(docker).setupQemu("./")
        .then(() => assert(false))
        .catch(err => assert(err ? true : false));
    });

    test("Should not need qemu if architecture is ARM", () => {
        docker.version = (some: (err, info) => {}) => {
            const info = { Arch: "arm64" };
            some(null, info);
        };

        new QemuUtils(docker).setupQemu("./")
        .then(needsQemu => assert(!needsQemu))
        .catch(() => assert(false));
    });
});
