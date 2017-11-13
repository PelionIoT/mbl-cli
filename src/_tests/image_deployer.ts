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
import { ImageDeployer } from "../deploy/image_deployer";

suite("ImageDeployer", () => {
    let deployer: ImageDeployer;
    const docker: any = {
        getImage: stub().returns(null)
    };

    beforeEach(() => {
        deployer = new ImageDeployer(docker);
    });

    test("Should reject if no image tag is specified", () => {
        deployer.deployStream("")
        .then(() => assert(false))
        .catch(err => assert(err ? true : false));
    });

    test("Should reject if no tag image is found", () => {
        deployer.deployStream("test")
        .then(() => assert(false))
        .catch(err => assert(err ? true : false));
    });
});
