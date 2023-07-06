# Leaderboard Program
A simple Python Utility that allows you to create a leaderboard for multiple programs that are submitted to you. This works for programs written in C but can be easily extended to other languages by changing the compile command in the `eval.py` file.

The program can be modified to run at different time intervals as well, See point 4 in the section below for more details.

# How to use : 
1. Clone the repository
2. Place the submissions to the `submissions` folder in the root directory, each submission should be in it's own folder and the c file should be named `{folder_name}_assignment1.c`
3. Place the test cases in the `test_cases` folder in the root directory, each test case should be in it's own folder and the input and output files should be named `input.txt` and `output.txt` respectively. If we have a test case where there are multiple (infinitely) possible outputs for a single input, then the content of the `output.txt` file should be `Ignore` and we must write a custom validator in the `eval.py` file. An example of this is the `test_cases/2` folder and the `eval.py` file has a Custom Validator for the Knights tour problem which can have multiple different solutions for a single input.
4. Once the things Run the `main.py` file as follows : 
    1. If you want to run the program once, then run `python3 main.py once`
    2. If we want to run the program at regular intervals, then run `python3 main.py regular <interval_in_minutes>`. For example, if we want to run the program every 5 minutes, then run `python3 main.py regular 5`
5. The program will run all the submissions for the given test cases and produce a `leaderboard.csv` file in the root directory.

# Scope of Improvement :
1. Add support for other languages
2. Add support for running multiple test cases in parallel or run multiple groups at once
3. Support for partial test cases being passed (currently pass everything or nothing)