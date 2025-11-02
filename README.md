# learn-berkeley-cs188sp24

This is my solutions to the projects for the Berkeley CS 188 course for Spring 2024.

## Code Reading Notes

### Shared utility file `util.py`

#### FixedRandom class

This is a random number generator that always produces the same sequence of numbers. It is useful for debugging and testing, as it allows for reproducible results.

Technically the fixed randomness can also be achieved by setting a random seed such as `random.seed(0)`, but that will affect the randomness globally, and all subsequent calls to random functions will be affected. The FixedRandom class does not change the global random state, and only affects the code that uses it, thus providing better isolation.

This class is not really used in tutorial and search projects. Maybe it is part of a legacy codebase.

#### PriorityQueue class

This is a standard priority queue implementation using a heap. It allows the same item to be added multiple times with different priorities. In such case, the item with the lowest priority value will stay in the queue.

In its `update` method, it uses the `for-else` construct to check if an item can be found in the queue. The `else` block is executed only if the `for` loop completes without hitting a `break` statement, which means the item was not found in the queue. If we change `break` to `return`, and remove the `else` block, the logic will still be correct, and even more readable.
