/*
* Mbed Linux OS CLI
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

import * as yargs from "yargs";

// tslint:disable-next-line:no-unused-expression
yargs
.strict()
.usage("$0 <command> [arguments]")
.version().alias("v", "version")
.help().alias("h", "help")
.commandDir("commands", {
    exclude: /app/,
    recurse: true
})
.demandCommand(1, "")
.recommendCommands()
.epilogue("For more information about Mbed Linux OS, please visit http://mbed.com")
.argv;
