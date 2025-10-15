# Project 2: Convex Hull

Submission of my project 2 on the Convex Hull problem.

## Execution Commands
- Main Script: python3 Project2_RM.py
- Test Script: python3 Project2_RM_test.py OR python3 -m unittest Project2_RM_test.py

## Directions

Project2_RM:
- If your Python is up to date, there should be nothing to be done extra here. "random", "time", "csv", "List", "Tuple" are built in libraries.
- If you intend to run and play around with the values, you can go into the "main" at the bottom and set "n_values" or "min/max_coordinate" to equal whatever numbers you'd like. A csv file is then generated and all subsequent runs are stored in there.
    - NOTE: Modifying the values -will- affect performance.
- This doesn't run with arguments off the cmd line as the assignment didn't ask for it and honestly it wasn't needed.
- NOTE: We considered printing the hull points as output, but at our larger values of "n", there's no way that output would make any human readable sense. (At least 10ish points in the n=100 case.)
    - Though we did initially test with smaller arrays of points and can confirm the algorithm works.
    - This [link](https://dccg.upc.edu/teaching/applets/convex_hull.html) helps visualize what I mean.

Project2_RM_test:
- This is our PyUnit testing file. Make sure that both the algo script and this one are in the same folder before you run it.

Overall:
- Both files each have a description at the top and comments throughout to make understanding the code easier.
- Both have been tested and are confirmed to work when executing.
- I've included any plot screenshots outside of the doc in case they're hard to read.

## Code Fun Notes

- Colinearity turned out to be the most annoying thing to deal with and became a solved edge case. Tangents and median finding ("closest pair of points" helped) are right behind it.
- This script is an amalgam of a bunch of pseudocode because the convex hull problem is scarcely covered.
- Using Python's "timsort" here because I didn't want to implement merging myself and its built in, therefore faster. Same with geometric primitives, very interesting.