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

export type typeEnum = "local" | "remote";

/**
 * @param host Type of host to deploy to
 */
export function createDockerode(host: typeEnum): Dockerode {
    const options: { [key: string]: string | number } = {};
    if (host === "local") {
        options.socketPath = "/var/run/docker.sock";
    } else {
        options.host = "10.6.44.215";
        options.port = 2376;
    }
    return new Dockerode(options);
}
