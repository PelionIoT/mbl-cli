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
import { existsSync } from "fs";
import { join } from "path";

export class DockerUtils {

    public createDockerode(remote: boolean): Dockerode {
        const options: { [key: string]: string | number } = {};
        if (remote) {
            options.host = "10.6.44.215";
            options.port = 2376;
        } else {
            options.socketPath = "/var/run/docker.sock";
        }
        return new Dockerode(options);
    }

    public checkDocker(buildPath: string, docker: Dockerode): Promise<void> {
        return new Promise((resolve, reject) => {
            const dockerFile = join(buildPath, "Dockerfile");
            if (!existsSync(dockerFile)) reject("Dockerfile not found, check directory is a valid Mbed Linux application");

            docker.version((error, _info) => {
                if (error) return reject("Docker not found, check it's installed and running");
                resolve();
            });
        });
    }
}
