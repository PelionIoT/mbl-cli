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

import { FileDeployer } from "../../deployers/file_deployer";
import { Deployer } from "../../deployers/interface";
import { log } from "../../utils/logger";
import { Builder } from "./builder";
import { BuildCommand } from "./command";

export class Handler {

    private deployer: Deployer;
    private builder: Builder;

    public constructor(args: BuildCommand) {
        this.deployer = new FileDeployer(args.path);
        this.deployer.addListener(FileDeployer.EVENT_LOG, log);
        this.builder = new Builder(args);
    }

    public run() {
        this.builder.build(true)
        .then(stream => this.deployer.deploy(stream))
        .catch(error => log(`Error: ${error}`));
    }
}
