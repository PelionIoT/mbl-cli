import { Writable } from "stream";

export class DevNull extends Writable {
    constructor(options: {} = {}) {
        super(options);
    }

    public _write(_chunk, _encoding, callback) {
        callback();
    }
}
