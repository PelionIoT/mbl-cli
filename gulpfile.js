var path        = require("path");
var del         = require("del");
var merge       = require('merge2');
var tslint      = require("tslint");
var gulp        = require("gulp");
var gulpTs      = require("gulp-typescript");
var gulpTslint  = require("gulp-tslint");
var gulpTypedoc = require("gulp-typedoc");

var name = "Mbed Linux CLI";
var docsToc = "";

var srcDir = "src";
var docsDir = "docs";
var nodeDir = "dist";
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

// Lint the source
gulp.task("lint", function() {
    var program = tslint.Linter.createProgram();

    gulp.src(srcDir + "/**/*.ts")
    .pipe(gulpTslint({
        program: program,
        formatter: "stylish"
    }))
    .pipe(gulpTslint.report({
        emitError: false
    }))
});

// Create documentation
gulp.task("doc", function() {
    return gulp.src(srcDir + "/**/*.ts")
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
gulp.task("compile", function() {
    var tsResult = gulp.src(srcDir + "/**/*.ts")
    .pipe(gulpTs({
        target: "es6",
        module: "commonjs",        
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

gulp.task("default", ["clean", "lint", "doc", "compile"]);
