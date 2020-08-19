# README
* LAST UPDATED: 2020-08-19
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: ay2021-1/pep8


## PEP8 Assignment
Similar to driving a car, programmers tend to develop their own methodology of writing code, which is acceptable so long as it gets the job done.
However, just as one has to pass the driver's license examination with an in-the-car demonstration, coders should be able to demonstrate their competency and mastery of coding syntax guidelines, including consistency, readability, and structure.

You may choose any one of your scripts (i.e., utility script, a conversion script, sparse data challenge script, sandbox challenge script, or project script) to be graded based on Python's [PEP8](https://www.python.org/dev/peps/pep-0008/) syntax guidelines.
Upload your script to this directory (keep the original name of your file) and tag the PEP8 Issue with your commit comment.
Be certain to include a purpose statement for your script in the comments at the top so I know what your script is supposed to do.


### Learning Objectives
* Tractable and reusable code development
* Clear and concise code documentation
* Git workflows


### Grading
**5 pt**

**Requirements:**

- Proper syntax, format, and style
    * clear import statements (do not use `*` character)
    * organize your code (e.g., group classes and functions together ahead of your main script); i.e., implement the DRY/DIE principle
    * when possible, group duplicated bits of code into functions for reusability
    * variable and function naming (avoid reserved keywords or ambiguous letters like "l," "I," and "O")
    * use spaces for indentation and white space (no variable-length tabs)
    * use blank lines to separate operational segments of your code
    * limit line length (79-80 characters)
    * do not use non-ASCII characters
- Documentation
    * first line shebang
    * top of script comments should include:
        - author, date (last updated)
        - purpose statement (what is the script supposed to do and what does it need to run; for example: give the assignment description and describe whether it requires input data or creates output data)
    * use inline comments where needed
    * include doc strings with functions (see [PEP257](https://www.python.org/dev/peps/pep-0257/))
    * include attribution (URL, author, date) to copied code (either in entirety or just bits; for example: based on so-and-so)
    * follow English grammar (see [Skrunk & White](https://faculty.washington.edu/heagerty/Courses/b572/public/StrunkWhite.pdf))
- Handles errors and user input
    * include error handling; especially if you are asking users to input some values---_I will test your code with bad inputs_
    * avoid hard-coded directory names or file names unless indicated by the assignment
        - to increase code usability, use `os.path.join` for building directory paths as Mac/Nix systems use `/` while Windows/DOS systems use `\` for path separators; the exception is for URL/URIs, which always use `/`
- Follows the instructions outlined above and answers, solves, or addresses the given assignment without crashing
