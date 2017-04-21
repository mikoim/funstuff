"use strict";

const assert = require("chai").assert;
const codecheck = require("codecheck");
const app = codecheck.consoleApp(process.env.APP_COMMAND);

describe("daysInYear: 100, daysInMonth: 10, daysInWeek: 5", () => {
  const cases = require("./case_100-10-5.json");
  cases.forEach(v => {
    let desc = v.it || `${v.input.split(" ").pop()} =>=> ${v.output.join(" ")}`;
    it(desc, () => {
      return app.codecheck(v.input.split(" "))
        .then(result => {
          assert.equal(result.code, 0);
          assert.equal(result.stdout[0], v.output);
        });
    });
  });
});

describe("daysInYear: 160, daysInMonth: 30, daysInWeek: 7", () => {
  const cases = require("./case_160-30-7.json");
  cases.forEach(v => {
    let desc = v.it || `${v.input.split(" ").pop()} =>=> ${v.output.join(" ")}`;
    it(desc, () => {
      return app.codecheck(v.input.split(" "))
        .then(result => {
          assert.equal(result.code, 0);
          assert.equal(result.stdout[0], v.output);
        });
    });
  });
});

describe("daysInYear: 365, daysInMonth: 50, daysInWeek: 8", () => {
  const cases = require("./case_365-50-8.json");
  cases.forEach(v => {
    let desc = v.it || `${v.input.split(" ").pop()} =>=> ${v.output.join(" ")}`;
    it(desc, () => {
      return app.codecheck(v.input.split(" "))
        .then(result => {
          assert.equal(result.code, 0);
          assert.equal(result.stdout[0], v.output);
        });
    });
  });
});
