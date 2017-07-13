"use strict";

const expect = require("chai").expect;
const codecheck = require("codecheck");
const app = codecheck.consoleApp(process.env.APP_COMMAND);
const testcases = require("./basic_testcases.json");

describe("CLI", () => {
  testcases.forEach((testcase) => {
    it(testcase.title, () => {
      return app.codecheck(testcase.input).then((result) => {
        expect(result.code).to.equal(testcase.code,
          `CLI must exit with status code ${testcase.code}`);
        if (testcase.code !== 0) {
          return;
        }
        expect(result.stdout[0]).to.equal(testcase.output,
          `${testcase.input} should be converted to ${testcase.output}`);
      });
    });
  });
});
