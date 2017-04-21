# Look and Say!

*This is a [codecheck](https://app.code-check.io/openchallenges) challenge. To get started, [see the docs](https://code-check.github.io/docs/en)* :-)  

The look and say method is a secret method that returns the below results:

If this method receives '1', it should return '1'.
If it receives '2', it should return '11'.  
If it receives '3', it should return '21', and so on.
```
1 -> 1
2 -> 11
3 -> 21
4 -> 1211
5 -> 111221
6 -> 312211
7 -> 13112221
```

## Your Mission

Identify the rule of this sequence and implement the function.

## Implementation
###### CLI
Build the solution as a CLI application.  
Input parameters will be passed as an argument of CLI, and
the output should be written to stdout.

You can use the following languages to solve this challenge.

- NodeJS
- Ruby
- Python (2.x)
- Python3
- Go
- Java

How to make a CLI application with each language is explained in [YOUR LANGUAGE].md

###### Secret Test
You can see 7 testcases in [testcase.js](test/testcase.js).
However, this challenge has 3 additional hidden testcases:

- SecretTest1. Passes an integer of '8', and expects a correct answer.
- SecretTest2. Passes an integer of '20', and expects a correct answer.
- SecretTest3. Passes an integer of '10000'. Find the initial 500 digits of the expected output, and write this in the first line of [answer.md](answer.md). Explain how you solved the problem beginning from line 2.

If your function is implemented correctly, the first 2 tests will pass.

However, if your implementation is too earnest, the last question will eat up all of your memory! :(
Try to find a way to optimize.

PS:
The secret tests will run only when the challenge is submitted,
and the results are never shown in the WebEditor.

## Answer.md
In [answer.md](answer.md) write a brief explanation about:
- The output for SecretTest3
- How your code works
- Problems faced while solving the challenge
- How you solved those problems
