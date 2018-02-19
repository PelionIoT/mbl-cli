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
import { beforeEach, suite, test } from "intern/lib/interfaces/tdd";
import { stub } from "sinon";
import { DirectoryBuilder } from "../builders/directory_builder";

suite("DockerBuilder", () => {
    const docker: any = {
        // tslint:disable-next-line:no-empty
        buildImage: stub().returns(new Promise(() => {}))
    };

    let builder: DirectoryBuilder;

    beforeEach(() => {
        builder = new DirectoryBuilder(docker);
    });

    test("Should reject if no docker is available", () => {
        docker.getVersion = (some: (err, info) => {}) => { some("error", ""); };

        builder.requiresEmulation()
        .then(() => assert(false))
        .catch(err => assert(err ? true : false));
    });

    test("Should not need qemu if architecture is ARM", () => {
        docker.getVersion = stub().resolves({ Arch: "arm" });

        builder.requiresEmulation()
        .then(emu => assert(!emu))
        .catch(() => assert(false));
    });

    test("Should pipe streams and call build a docker image", () => {
        const checkEmulation = stub().returns(Promise.resolve(false));
        const checkDocker = stub().returns(Promise.resolve());

        builder.requiresEmulation = checkEmulation;
        builder.checkDocker = checkDocker;

        builder.build("")
        .then(() => {
            assert(checkEmulation.called && docker.buildImage.called);
        });
    });
});
