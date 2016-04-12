# test data for the symmetry tests
# These are very long, so keep them in a
# separate file
import numpy

uniq = {
    "-1": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-2, -1, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [-2, 0, -2],
            [-1, 0, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [-2, 1, -2],
            [-1, 1, -2],
            [0, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-2, 2, -2],
            [-1, 2, -2],
            [0, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-2, -1, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [-2, 0, -1],
            [-1, 0, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [-2, 1, -1],
            [-1, 1, -1],
            [0, 1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [-2, 2, -1],
            [-1, 2, -1],
            [0, 2, -1],
            [1, 2, -1],
            [2, 2, -1],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [2, 1, 0],
            [0, 2, 0],
            [1, 2, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-2, -1, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [-2, 0, 1],
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [-2, 1, 1],
            [-1, 1, 1],
            [0, 1, 1],
            [1, 1, 1],
            [2, 1, 1],
            [-2, 2, 1],
            [-1, 2, 1],
            [0, 2, 1],
            [1, 2, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-2, -1, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [-2, 0, 2],
            [-1, 0, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [-2, 1, 2],
            [-1, 1, 2],
            [0, 1, 2],
            [1, 1, 2],
            [2, 1, 2],
            [-2, 2, 2],
            [-1, 2, 2],
            [0, 2, 2],
            [1, 2, 2],
            [2, 2, 2]]),
    "2/m": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-2, -1, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [-2, 0, -2],
            [-1, 0, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [-2, 1, -2],
            [-1, 1, -2],
            [0, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-2, 2, -2],
            [-1, 2, -2],
            [0, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-2, -1, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [-2, 0, -1],
            [-1, 0, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [-2, 1, -1],
            [-1, 1, -1],
            [0, 1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [-2, 2, -1],
            [-1, 2, -1],
            [0, 2, -1],
            [1, 2, -1],
            [2, 2, -1],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [2, 1, 0],
            [0, 2, 0],
            [1, 2, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-2, -1, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [-2, 0, 1],
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [-2, 1, 1],
            [-1, 1, 1],
            [0, 1, 1],
            [1, 1, 1],
            [2, 1, 1],
            [-2, 2, 1],
            [-1, 2, 1],
            [0, 2, 1],
            [1, 2, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-2, -1, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [-2, 0, 2],
            [-1, 0, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [-2, 1, 2],
            [-1, 1, 2],
            [0, 1, 2],
            [1, 1, 2],
            [2, 1, 2],
            [-2, 2, 2],
            [-1, 2, 2],
            [0, 2, 2],
            [1, 2, 2],
            [2, 2, 2]]),
    "4/mmm": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [1, 1, -2],
            [2, 1, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [1, 1, -1],
            [2, 1, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [1, 1, 1],
            [2, 1, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2]]),
    "6/mmm": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [1, 1, -2],
            [2, 1, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [1, 1, -1],
            [2, 1, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [1, 1, 1],
            [2, 1, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2]]),
    "4/m": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-2, -1, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [-2, 0, -2],
            [-1, 0, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [-2, 1, -2],
            [-1, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-2, 2, -2],
            [-1, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-2, -1, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [-2, 0, -1],
            [-1, 0, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [-2, 1, -1],
            [-1, 1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [-2, 2, -1],
            [-1, 2, -1],
            [1, 2, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-2, -1, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [-2, 0, 0],
            [-1, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [-2, 1, 0],
            [-1, 1, 0],
            [1, 1, 0],
            [2, 1, 0],
            [-2, 2, 0],
            [-1, 2, 0],
            [1, 2, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-2, -1, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [-2, 0, 1],
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [-2, 1, 1],
            [-1, 1, 1],
            [1, 1, 1],
            [2, 1, 1],
            [-2, 2, 1],
            [-1, 2, 1],
            [1, 2, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-2, -1, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [-2, 0, 2],
            [-1, 0, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [-2, 1, 2],
            [-1, 1, 2],
            [1, 1, 2],
            [2, 1, 2],
            [-2, 2, 2],
            [-1, 2, 2],
            [1, 2, 2],
            [2, 2, 2]]),
    "6/m": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-2, -1, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [-2, 0, -2],
            [-1, 0, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [-2, 1, -2],
            [-1, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-2, 2, -2],
            [-1, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-2, -1, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [-2, 0, -1],
            [-1, 0, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [-2, 1, -1],
            [-1, 1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [-2, 2, -1],
            [-1, 2, -1],
            [1, 2, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-2, -1, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [-2, 0, 0],
            [-1, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [-2, 1, 0],
            [-1, 1, 0],
            [1, 1, 0],
            [2, 1, 0],
            [-2, 2, 0],
            [-1, 2, 0],
            [1, 2, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-2, -1, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [-2, 0, 1],
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [-2, 1, 1],
            [-1, 1, 1],
            [1, 1, 1],
            [2, 1, 1],
            [-2, 2, 1],
            [-1, 2, 1],
            [1, 2, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-2, -1, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [-2, 0, 2],
            [-1, 0, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [-2, 1, 2],
            [-1, 1, 2],
            [1, 1, 2],
            [2, 1, 2],
            [-2, 2, 2],
            [-1, 2, 2],
            [1, 2, 2],
            [2, 2, 2]]),
    "-3m1": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-2, -1, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [-2, 0, -2],
            [-1, 0, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [-2, 1, -2],
            [-1, 1, -2],
            [0, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-2, 2, -2],
            [-1, 2, -2],
            [0, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-2, -1, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [-2, 0, -1],
            [-1, 0, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [-2, 1, -1],
            [-1, 1, -1],
            [0, 1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [-2, 2, -1],
            [-1, 2, -1],
            [0, 2, -1],
            [1, 2, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-2, -1, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [-2, 0, 1],
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [-2, 1, 1],
            [-1, 1, 1],
            [0, 1, 1],
            [1, 1, 1],
            [2, 1, 1],
            [-2, 2, 1],
            [-1, 2, 1],
            [0, 2, 1],
            [1, 2, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-2, -1, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [-2, 0, 2],
            [-1, 0, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [-2, 1, 2],
            [-1, 1, 2],
            [0, 1, 2],
            [1, 1, 2],
            [2, 1, 2],
            [-2, 2, 2],
            [-1, 2, 2],
            [0, 2, 2],
            [1, 2, 2],
            [2, 2, 2]]),
    "-31m": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [1, 1, 1],
            [2, 1, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2]]),
    "-3": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [0, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-1, 2, -2],
            [0, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [0, 1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [-1, 2, -1],
            [0, 2, -1],
            [1, 2, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
            [1, 2, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [0, 1, 1],
            [1, 1, 1],
            [2, 1, 1],
            [-1, 2, 1],
            [0, 2, 1],
            [1, 2, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [0, 1, 2],
            [1, 1, 2],
            [2, 1, 2],
            [-1, 2, 2],
            [0, 2, 2],
            [1, 2, 2],
            [2, 2, 2]]),
    "R-3m1": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-2, -1, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [-2, 0, -2],
            [-1, 0, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [-2, 1, -2],
            [-1, 1, -2],
            [0, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-2, 2, -2],
            [-1, 2, -2],
            [0, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-2, -1, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [-2, 0, -1],
            [-1, 0, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [-2, 1, -1],
            [-1, 1, -1],
            [0, 1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [-2, 2, -1],
            [-1, 2, -1],
            [0, 2, -1],
            [1, 2, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-2, -1, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [-2, 0, 0],
            [-1, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [-2, 1, 0],
            [-1, 1, 0],
            [0, 1, 0],
            [1, 1, 0],
            [2, 1, 0],
            [-2, 2, 0],
            [-1, 2, 0],
            [0, 2, 0],
            [1, 2, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-2, -1, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [-2, 0, 1],
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [-2, 1, 1],
            [-1, 1, 1],
            [0, 1, 1],
            [1, 1, 1],
            [2, 1, 1],
            [-2, 2, 1],
            [-1, 2, 1],
            [0, 2, 1],
            [1, 2, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-2, -1, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [-2, 0, 2],
            [-1, 0, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [-2, 1, 2],
            [-1, 1, 2],
            [0, 1, 2],
            [1, 1, 2],
            [2, 1, 2],
            [-2, 2, 2],
            [-1, 2, 2],
            [0, 2, 2],
            [1, 2, 2],
            [2, 2, 2]]),
    "R-31m": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-2, -1, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [-2, 0, -2],
            [-1, 0, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [-2, 1, -2],
            [-1, 1, -2],
            [0, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-2, 2, -2],
            [-1, 2, -2],
            [0, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-2, -2, -1],
            [-1, -2, -1],
            [0, -2, -1],
            [1, -2, -1],
            [2, -2, -1],
            [-2, -1, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [-2, 0, -1],
            [-1, 0, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [-2, 1, -1],
            [-1, 1, -1],
            [0, 1, -1],
            [1, 1, -1],
            [2, 1, -1],
            [-2, 2, -1],
            [-1, 2, -1],
            [0, 2, -1],
            [1, 2, -1],
            [2, 2, -1],
            [-2, -2, 0],
            [-1, -2, 0],
            [0, -2, 0],
            [1, -2, 0],
            [2, -2, 0],
            [-2, -1, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [-2, 0, 0],
            [-1, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [-2, 1, 0],
            [-1, 1, 0],
            [0, 1, 0],
            [1, 1, 0],
            [2, 1, 0],
            [-2, 2, 0],
            [-1, 2, 0],
            [0, 2, 0],
            [1, 2, 0],
            [2, 2, 0],
            [-2, -2, 1],
            [-1, -2, 1],
            [0, -2, 1],
            [1, -2, 1],
            [2, -2, 1],
            [-2, -1, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],
            [2, -1, 1],
            [-2, 0, 1],
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [-2, 1, 1],
            [-1, 1, 1],
            [0, 1, 1],
            [1, 1, 1],
            [2, 1, 1],
            [-2, 2, 1],
            [-1, 2, 1],
            [0, 2, 1],
            [1, 2, 1],
            [2, 2, 1],
            [-2, -2, 2],
            [-1, -2, 2],
            [0, -2, 2],
            [1, -2, 2],
            [2, -2, 2],
            [-2, -1, 2],
            [-1, -1, 2],
            [0, -1, 2],
            [1, -1, 2],
            [2, -1, 2],
            [-2, 0, 2],
            [-1, 0, 2],
            [0, 0, 2],
            [1, 0, 2],
            [2, 0, 2],
            [-2, 1, 2],
            [-1, 1, 2],
            [0, 1, 2],
            [1, 1, 2],
            [2, 1, 2],
            [-2, 2, 2],
            [-1, 2, 2],
            [0, 2, 2],
            [1, 2, 2],
            [2, 2, 2]]),
    "R-3": numpy.array(
        [[1, 0, -2],
         [2, 0, -2],
            [1, 1, -2],
            [2, 1, -2],
            [2, 2, -2],
            [1, 0, -1],
            [2, 0, -1],
            [1, 1, -1],
            [2, 1, -1],
            [2, 2, -1]]),
    "m3m": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [1, 1, -2],
            [2, 1, -2],
            [2, 2, -2],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [1, 1, -1],
            [2, 1, -1],
            [2, 2, -1],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
            [2, 2, 0],
            [1, 1, 1],
            [2, 1, 1],
            [2, 2, 1],
            [2, 2, 2]]),
    "m3": numpy.array(
        [[-2, -2, -2],
         [-1, -2, -2],
            [0, -2, -2],
            [1, -2, -2],
            [2, -2, -2],
            [-1, -1, -2],
            [0, -1, -2],
            [1, -1, -2],
            [2, -1, -2],
            [-1, 0, -2],
            [0, 0, -2],
            [1, 0, -2],
            [2, 0, -2],
            [-1, 1, -2],
            [1, 1, -2],
            [2, 1, -2],
            [-1, 2, -2],
            [1, 2, -2],
            [2, 2, -2],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1],
            [2, -1, -1],
            [0, 0, -1],
            [1, 0, -1],
            [2, 0, -1],
            [1, 1, -1],
            [2, 1, -1],
            [1, 2, -1],
            [2, 2, -1],
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
            [1, 2, 0],
            [2, 2, 0],
            [1, 1, 1],
            [2, 1, 1],
            [2, 2, 1],
            [2, 2, 2]]),
}
