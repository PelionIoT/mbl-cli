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

import { existsSync } from "fs";
import { DirectoryBuilder } from "../../builders/directory_builder";
import { Docker } from "../../utils/docker";
import { log } from "../../utils/logger";

const DEFAULT_REMOTE_HOST = "vm-isg-mbed.on.arm.com:2376";

export interface BuildArgs {
    force;
    noemulation;
    remote;
    source;
}

export class Builder {

    public constructor(private args: BuildArgs) {}

    public build(returnStream: boolean = false): Promise<NodeJS.ReadableStream> {
        if (!existsSync(this.args.source)) {
            return Promise.reject(`Unable to find source '${this.args.source}'`);
        }

        let remoteHost = DEFAULT_REMOTE_HOST;
        if (this.args.remote) {
            if (typeof this.args.remote === "string") remoteHost = this.args.remote.toString();
            log(`Using remote host '${remoteHost}'`);
        } else remoteHost = null;

        const docker = new Docker(remoteHost);
        const builder = new DirectoryBuilder(docker, !this.args.noemulation);

        builder.addListener(DirectoryBuilder.EVENT_LOG, log);

        return builder.build(this.args.source, this.args.force)
        .then(() => {
            if (returnStream) return docker.getImage();
        });
    }
}
