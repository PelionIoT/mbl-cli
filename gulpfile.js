let path        = require("path");
let del         = require("del");
let merge       = require('merge2');
let gulp        = require("gulp");
let tslint      = require("gulp-tslint");
let typedoc     = require("gulp-typedoc");
let typescript  = require("gulp-typescript");
let sourcemaps  = require("gulp-sourcemaps");

let name = "Mbed Linux CLI";
let configPath = "tsconfig.json";

let srcDir = "src";
let srcFiles = srcDir + "/**/*.ts";
let srcFilesOnly = [
    srcFiles,
    "!" + srcDir + "/_tests/**"
];
let docsDir = "docs";
let nodeDir = "lib";
let typesDir = "types";
let watching = false;

function handleError() {
    if (watching) this.emit("end");
    else process.exit(1);
}

// Set watching
gulp.task("setWatch", () => {
    watching = true;
});

// Clear built directories
gulp.task("clean", () => {
    if (!watching) del([nodeDir, typesDir]);
});

// Lint the source
gulp.task("lint", () => {
    gulp.src(srcFiles)
    .pipe(tslint({
        formatter: "stylish"
    }))
    .pipe(tslint.report({
        emitError: !watching
    }))
});

// Create documentation
gulp.task("doc", () => {
    return gulp.src(srcFilesOnly)
    .pipe(typedoc({
        name: name,
        readme: "src/documentation.md",
        theme: "src/theme",
        mode: "file",
        target: "es6",
        module: "commonjs",
        out: docsDir,
        excludeExternals: true,
        excludePrivate: true,
        hideGenerator: true
    }))
    .on("error", handleError);
});

// Build TypeScript source into CommonJS Node modules
gulp.task("compile", ["clean"], () => {
    return merge([
        gulp.src(srcFiles)
        .pipe(sourcemaps.init())
        .pipe(typescript.createProject(configPath)())
        .on("error", handleError).js
        .pipe(sourcemaps.write(".", {
            sourceRoot: path.relative(nodeDir, srcDir)
        }))
        .pipe(gulp.dest(nodeDir)),
        gulp.src(srcFilesOnly)
        .pipe(typescript.createProject(configPath)())
        .on("error", handleError).dts
        .pipe(gulp.dest(typesDir))
    ]);
});

gulp.task("watch", ["setWatch", "default"], () => {
    gulp.watch(srcFiles, ["lint", "compile"]);
});

gulp.task("default", ["lint", "doc", "compile"]);
