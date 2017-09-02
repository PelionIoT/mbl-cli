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

import * as program from "commander";
import * as Dockerode from "dockerode";
import * as tarfs from "tar-fs";
import * as tar from "tar-stream";

/*
export { AccountManagementApi } from "./accountManagement/accountManagementApi";
export { CertificatesApi } from "./certificates/certificatesApi";
export { ConnectApi } from "./connect/connectApi";
export { DeviceDirectoryApi } from "./deviceDirectory/deviceDirectoryApi";
export { UpdateApi } from "./update/updateApi";
*/

program
.version("0.1.0")
.option("-p, --peppers", "Add peppers")
.option("-P, --pineapple", "Add pineapple")
.option("-b, --bbq-sauce", "Add bbq sauce")
.option("-c, --cheese [type]", "Add the specified type of cheese [marble]", "marble")
.parse(process.argv);

// tslint:disable-next-line:no-console
console.log("you ordered a pizza with:");
if (program.peppers) {
    // tslint:disable-next-line:no-console
    console.log("  - peppers");
}
if (program.pineapple) {
    // tslint:disable-next-line:no-console
    console.log("  - pineapple");
}
if (program.bbqSauce) {
    // tslint:disable-next-line:no-console
    console.log("  - bbq");
}
// tslint:disable-next-line:no-console
console.log("  - %s cheese", program.cheese);

/*
 use tar-fs to create a stream of tarred folder contents
 pass the stream to docker to build
 return id of build stuff
*/

const sourceDir = "/Users/robmor01/Projects/resinos-sample"; // ".";

// const dockerHost = "";
// const dockerPort = 2376;
const socketPath = "/var/run/docker.sock";

const docker = new Dockerode({
    socketPath: socketPath
});

let architecture = null;

docker.version((error, info) => {
    if (error) {
        // tslint:disable-next-line:no-console
        console.log("no docker running!");
        process.exit();
    }
    // tslint:disable-next-line:no-console
    console.log(`Docker version: ${info.Version}`);
    architecture = info.Arch;
});

const srcPack = tarfs.pack(sourceDir, {
    ignore: name => {
        return name.indexOf(".git") >= 0;
    }
});
const finalPack = tar.pack();

const extract = tar.extract();

extract.on("entry", (header, stream, next) => {
    // tslint:disable-next-line:no-console
    console.log(header.name);

    // ignore git (all hidden folders?)
    let contents = "";
    stream.on("data", chunk => {
        contents += chunk;
    });
    stream.on("end", () => {
        if (header.name === "Dockerfile") {
            const index = contents.indexOf("RUN");
            contents = `${contents.substr(0, index)}\nCOPY blah\n${contents.substr(index)}`;
            finalPack.entry({ name: header.name }, contents);
            // tslint:disable-next-line:no-console
            console.log(contents);
        } else {
            finalPack.entry(header, contents);
        }
        next();
    });
});

extract.on("finish", () => {
    finalPack.finalize();
});

srcPack.pipe(extract);

docker.buildImage(finalPack, {
    t: "test"
// noCache - bool
// squash - bool
// buildArgs - {}
}, (err, response) => {
    // tslint:disable-next-line:no-console
    if (err) return console.log(err);
    // tslint:disable-next-line:no-console
    response.pipe(process.stdout);
});
