var path        = require("path");
var del         = require("del");
var merge       = require('merge2');
var tslint      = require("tslint");
var gulp        = require("gulp");
var sourcemaps  = require("gulp-sourcemaps");
var gulpTs      = require("gulp-typescript");
var gulpTslint  = require("gulp-tslint");
var gulpTypedoc = require("gulp-typedoc");

var name = "Mbed Linux CLI";
var docsToc = "";

var srcDir = "src";
var srcFiles = srcDir + "/**/*.ts";
var srcFilesOnly = [
    srcFiles,
    "!" + srcDir + "/_tests/**"
];
var docsDir = "docs";
var nodeDir = "lib";
var typesDir = "types";
var watching = false;

function handleError() {
    if (watching) this.emit("end");
    else process.exit(1);
}

// Set watching
gulp.task("setWatch", function() {
    watching = true;
});

// Clear built directories
gulp.task("clean", function() {
    return del([nodeDir, typesDir]);
});

// Lint the source
gulp.task("lint", function() {
    var program = tslint.Linter.createProgram("./");

    gulp.src(srcFiles)
    .pipe(gulpTslint({
        program: program,
        formatter: "stylish"
    }))
    .pipe(gulpTslint.report({
        emitError: !watching
    }))
});

// Create documentation
gulp.task("doc", function() {
    return gulp.src(srcFiles)
    .pipe(gulpTypedoc({
        name: name,
        readme: "src/documentation.md",
        theme: "src/theme",
        mode: "file",
        target: "es6",
        module: "commonjs",
        out: docsDir,
        excludeExternals: true,
        excludePrivate: true,
        hideGenerator: true,
        toc: docsToc
    }))
    .on("error", handleError);
});

// Build TypeScript source into CommonJS Node modules
gulp.task("compile", ["clean"], function() {
    return merge([
        gulp.src(srcFiles)
        .pipe(sourcemaps.init())
        .pipe(gulpTs.createProject("tsconfig.json")())
        .on("error", handleError).js
        .pipe(sourcemaps.write(".", {
            sourceRoot: path.relative(nodeDir, srcDir)
        }))
        .pipe(gulp.dest(nodeDir)),
        gulp.src(srcFilesOnly)
        .pipe(gulpTs.createProject("tsconfig.json")())
        .on("error", handleError).dts
        .pipe(gulp.dest(typesDir))
    ]);
});

gulp.task("watch", ["setWatch", "default"], function() {
    gulp.watch(srcFiles, ["default"]);
});

gulp.task("default", ["lint", "doc", "compile"]);
