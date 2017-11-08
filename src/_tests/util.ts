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
