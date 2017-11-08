#!/usr/bin/env node
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
import { before, suite, test } from "intern/lib/interfaces/tdd";
import { Readable, Writable } from "stream";
import { prettifyStream } from "../util/transform";

suite("Stream format", () => {
    let writable: Writable;
    let readable: Readable;

    before(() => {
        writable = new Writable({
            write(chunk: Buffer, encoding: string, callback: any) {
                callback(null, chunk.toString(encoding === "buffer" ? undefined : encoding));
            }
        });
    });

    test("Should be able to transform a null stream", () => {
        let output: string;
        readable = new Readable({
            read() {
                this.push(null);
            }
        });

        writable.on("data", (chunk: Buffer | string) => {
            output += chunk.toString();
        });

        writable.on("end", () => {
            assert(output === "message");
        });

        readable
            .pipe(prettifyStream)
            .pipe(writable);
    });

    test("Should be able to handle non JSON streams gracefully", () => {
        let output: string;
        readable = new Readable({
            read() {
                this.push("Non JSON message");
                this.push(null);
            }
        });

        writable.on("data", (chunk: Buffer | string) => {
            output += chunk.toString();
        });

        writable.on("end", () => {
            assert(output === "Non JSON message");
        });
    });

    test("Should be able to transform a json stream", () => {
        let output: string;
        readable = new Readable({
            read() {
                this.push("{\"stream\":\"message\"}", "utf8");
                this.push(null);
            }
        });

        writable.on("data", (chunk: Buffer | string) => {
            output += chunk.toString();
        });

        writable.on("end", () => {
            assert(output === "message");
        });

        readable
            .pipe(prettifyStream)
            .pipe(writable);
    });
});
