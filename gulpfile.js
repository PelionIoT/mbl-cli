var path        = require("path");
var del         = require("del");
var merge       = require('merge2');
var gulp        = require("gulp");
var typedoc     = require("gulp-typedoc");
var ts          = require("gulp-typescript");

var name = "Mbed Linux CLI";
var docsToc = "";

var srcDir = "src";
var docsDir = "docs";
var nodeDir = "lib";
var typesDir = "types";
var watching = false;

function handleError() {
    if (watching) this.emit("end");
    else process.exit(1);
}

// Clear built directories
gulp.task("clean", function() {
    return del([nodeDir, typesDir]);
});

// Create documentation
gulp.task("doc", function() {
    return gulp.src(srcDir + "/**/*.ts")
    .pipe(typedoc({
        name: name,
        readme: "src/documentation.md",
        theme: "src/theme",
        module: "commonjs",
        target: "es6",
        mode: "file",
        out: docsDir,
        excludeExternals: true,
        excludePrivate: true,
        hideGenerator: true,
        toc: docsToc
    }))
    .on("error", handleError);
});

// Build TypeScript source into CommonJS Node modules
gulp.task("typescript", function() {
    var tsResult = gulp.src(srcDir + "/**/*.ts")
    .pipe(ts({
        target: "es5",
        lib: ["dom", "es5", "es2015.promise"],
        alwaysStrict: true,
        noEmitOnError: true,
        noUnusedLocals: true,
        declaration: true,
        noUnusedParameters: true
    })).on("error", handleError);

    return merge([
        tsResult.dts.pipe(gulp.dest(typesDir)),
        tsResult.js.pipe(gulp.dest(nodeDir))
    ]);
});

gulp.task("watch", ["default"], function() {
    watching = true;
    gulp.watch(srcDir + "/**/*.*", ["default"]);
});

gulp.task("default", ["clean", "doc", "typescript"]);
