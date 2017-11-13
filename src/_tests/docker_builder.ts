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
import { spy, stub } from "sinon";
import { DockerBuilder } from "../build/docker_builder";

suite("DockerBuilder", () => {
    const docker: any = {
        buildImage: spy()
    };
    let builder: DockerBuilder = new DockerBuilder(docker);

    beforeEach(() => {
        builder = new DockerBuilder(docker);
    });

    test("Should pipe streams and call build a docker image", () => {
        const qemuUtils: any = {
            setupQemu: stub().returns(Promise.resolve(false))
        };

        builder.build("", "", qemuUtils)
        .then(() => {
            assert(qemuUtils.called && docker.buildImage.called);
        });
    });
});
