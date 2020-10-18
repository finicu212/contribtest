#### Virtopeanu Alexandru test

## Running the script and tests

Run the generator script by using `python generate.py {source files directory} {output directory}`. 

To run the tests, use `python test_generate.py`.

## Adding more files to test against

`test_generate.py` supports adding more expected output files. To add more files, simply create the expected
.html file in `test/expected_output` and the tester will check if the generator creates it.

----

See an overview of what was done by taking a look at the [merged pull requests](https://github.com/finicu212/contribtest/pulls?q=is%3Apr+is%3Amerged).

A simple plan was devised in [PR #1](https://github.com/finicu212/contribtest/pull/1)
