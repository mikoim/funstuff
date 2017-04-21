"use strict";

const assert = require("chai").assert;
const codecheck = require("codecheck");

describe("valid cases", function() {
  const app = codecheck.consoleApp(process.env.APP_COMMAND);
  const cases = require('./validcases.json');

  cases.forEach(v => {
    let desc = v.it || `${v.input} =>=> ${v.output.join(" ")}`;
    it(desc, () => {
      return app.codecheck(v.input.split(" "))
        .then(result => {
          assert.equal(result.code, 0);
          assert.deepEqual(result.stdout, v.output);
        });
    });
  });
});

describe("invalid cases", function() {
  const app = codecheck.consoleApp(process.env.APP_COMMAND);
  const cases = require('./invalidcases.json');

  cases.forEach(v => {
    let desc = v.it || `${v.input} =>=> ${v.output.join(" ")}`;
    it(desc, () => {
      return app.codecheck(v.input.split(" "))
        .then(result => {
          assert.equal(result.code, 0);
          assert.deepEqual(result.stdout, v.output);
        });
    });
  });
});
