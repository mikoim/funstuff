"use strict";

var assert = require("chai").assert;
var codecheck = require("codecheck");

describe("test", () => {
  var app = codecheck.consoleApp(process.env.APP_COMMAND);

  it("1 -> 1", function() {
    return app.run(1).spread(function(code, stdOut) {
      assert.equal(code, 0);
      assert.equal(stdOut.length, 1);
      assert.equal(stdOut[0], "1");
    });
  });

  it("2 -> 11", function() {
    return app.run(2).spread(function(code, stdOut) {
      assert.equal(code, 0);
      assert.equal(stdOut.length, 1);
      assert.equal(stdOut[0], "11");
    });
  });

  it("3 -> 21", function() {
    return app.run(3).spread(function(code, stdOut) {
      assert.equal(code, 0);
      assert.equal(stdOut.length, 1);
      assert.equal(stdOut[0], "21");
    });
  });

  it("4 -> 1211", function() {
    return app.run(4).spread(function(code, stdOut) {
      assert.equal(code, 0);
      assert.equal(stdOut.length, 1);
      assert.equal(stdOut[0], "1211");
    });
  });

  it("5 -> 111221", function() {
    return app.run(5).spread(function(code, stdOut) {
      assert.equal(code, 0);
      assert.equal(stdOut.length, 1);
      assert.equal(stdOut[0], "111221");
    });
  });

  it("6 -> 312211", function() {
    return app.run(6).spread(function(code, stdOut) {
      assert.equal(code, 0);
      assert.equal(stdOut.length, 1);
      assert.equal(stdOut[0], "312211");
    });
  });

  it("7 -> 13112221", function() {
    return app.run(7).spread(function(code, stdOut) {
      assert.equal(code, 0);
      assert.equal(stdOut.length, 1);
      assert.equal(stdOut[0], "13112221");
    });
  });
});
