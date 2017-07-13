"use strict";

const expect = require("chai").expect;
const codecheck = require("codecheck");
let app = codecheck.consoleApp(process.env.APP_COMMAND);

describe("Calling Websocket API", () => {
  it("does not return server error", () => {
    return app.codecheck(" ").then( result => {
      expect(result.code).to.equal(0, "expect codecheck CLI to exit with status code 0");
      let actualOutput = result.stdout.join("");
      expect(actualOutput).to.not.contain("Error: ");
    });
  });

  it("outputs response in correct format", () => {
    return app.codecheck("").then( result => {
      expect(result.code).to.equal(0, "expect codecheck CLI to exit with status code 0");
      let actualOutput = result.stdout.join("");
      expect(actualOutput).to.contain(" said: ");
    });
  });

  it("outputs a known server name", () => {
    let serverNames = [
      "World",
      "Alfred",
      "HAL 9800",
      "Lil Jon",
      "Lord Vader",
      "Radiofish",
      "Shakespeare",
      "Jack",
      "Satoshi",
      "Luke Skywalker",
      "Oriental Radio",
      "Dante"
    ];

    return app.codecheck("").then( result => {
      expect(result.code).to.equal(0, "expect codecheck CLI to exit with status code 0");
      let actualOutput = result.stdout.join("");
      let name = actualOutput.split(" said: ")[0];
      expect(name).to.be.oneOf(serverNames);
    });
  });

  it("includes a message from server after '[name] said: '", () => {
    return app.codecheck("").then( result => {
      expect(result.code).to.equal(0, "expect codecheck CLI to exit with status code 0");
      let actualOutput = result.stdout.join("");
      let message = actualOutput.split(" said: ")[1];
      expect(message).to.have.length.above(2);
    });
  });
});
