import { Transform } from "stream";

export const prettifyStream = new Transform({
    transform(chunk: any, encoding: any, callback: any) {
        if (encoding !== "buffer") {
            return callback(null, chunk.toString(encoding));
        }

        const chunkStr: string = chunk.toString();
        if (chunkStr) {
            chunkStr.split("\n").forEach(strObj => {
                if (!strObj) { return null; }
                const { stream = "" } = JSON.parse(strObj);
                this.push(stream);
            });
        }

        callback();
    }
});
