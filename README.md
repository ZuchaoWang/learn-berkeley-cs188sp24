# learn-berkeley-cs188sp24

This is my solutions to the projects for the Berkeley CS 188 course for Spring 2024.

## Code Reading Notes

### Shared utility file `util.py`

FixedRandom class is a random number generator that always produces the same sequence of numbers. It is useful for debugging and testing, as it allows for reproducible results.

Technically the fixed randomness can also be achieved by setting a random seed such as `random.seed(0)`, but that will affect the randomness globally, and all subsequent calls to random functions will be affected. The FixedRandom class does not change the global random state, and only affects the code that uses it, thus providing better isolation.

This class is not really used in tutorial and search projects. Maybe it is part of a legacy codebase.
