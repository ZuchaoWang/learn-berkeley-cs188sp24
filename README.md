# learn-berkeley-cs188sp24

This is my solutions to the projects for the Berkeley CS 188 course for Spring 2024.

## Code Reading Notes

### Shared utility file `util.py`

#### `FixedRandom` class

This is a random number generator that always produces the same sequence of numbers. It is useful for debugging and testing, as it allows for reproducible results.

Technically the fixed randomness can also be achieved by setting a random seed such as `random.seed(0)`, but that will affect the randomness globally, and all subsequent calls to random functions will be affected. The FixedRandom class does not change the global random state, and only affects the code that uses it, thus providing better isolation.

This class is not really used in tutorial and search projects. Maybe it is part of a legacy codebase.

#### `PriorityQueue` class

This is a standard priority queue implementation using a heap. It allows the same item to be added multiple times with different priorities. In such case, the item with the lowest priority value will stay in the queue.

In its `update` method, it uses the `for-else` construct to check if an item can be found in the queue. The `else` block is executed only if the `for` loop completes without hitting a `break` statement, which means the item was not found in the queue. If we change `break` to `return`, and remove the `else` block, the logic will still be correct, and even more readable.

#### `PriorityQueueWithFunction` class

This is the PriorityQueue that takes a priority function as an argument. In this way, it has the same interface as Stack and Queue classes, which allows it to be used interchangeably with them in search.

However, it inherits the `update` method from PriorityQueue, which does not use the priority function. This is a minor inconsistency, but hopefully this function won't be called in practice, since it is not part of the Stack/Queue interface.

#### `nSample` function

This is just a slightly faster implementation of sampling n items from a list. Compared to calling `sample` n times, it still need to call `random.random()` n times, but it avoids the overhead of normalizing distrbution probabilities n times, and scanning the probabilities all over again to find the right item n times.

#### `sampleFromCounter` function

This function seems redundant. Although it seems that it focuses on `Counter` input, it internally calls `sample` function, which can already handle `Counter` input. So this function does not provide any additional functionality. It is probably part of a legacy codebase.

#### `getProbability` function

Strange implementation. It seems to assume that the same value can appear multiple times in the `values` list, and in such case, the probabilities should be summed up. This is not a standard way to define discrete distributions. Normally, each value should appear only once in the `values` list.

#### `arrayInvert` function

This function does not really invert a matrix. It just transposes a matrix represented as a list of lists. The name is misleading.

#### `lookup` function

This function looks up a name in a given namespace (dictionary), and returns the corresponding object if found, otherwise returns None.

If the name is a qualified name such as `A.func`, it will first look up `A` in the namespace, and then look up `func` in the module `A`. This case is implemented correctly.

If the name is a simple name such as `func`, it will directly look up `func` in the namespace. It will also look up `func` in all modules found in the namespace. If multiple `func` are found, it will be considered as a name conflict. However this is a false "name conflict", because to call `func` in module `A` we must use `A.func`, while to call `func` in module `B` we must use `B.func`. There is no actual conflict here.

#### `TimeoutFunction` class

This class wraps a function and enforces a time limit on its execution. If the function takes longer than the specified timeout, a `TimeoutFunctionException` is raised.

If the system does not support the `SIGALRM` signal (e.g., Windows), the function will run to the end without interruption. After it finishes, if it took longer than the timeout, the exception will be raised. This means that on unsupported systems, the timeout is not enforced strictly.

If the system supports `SIGALRM`, the timeout is enforced strictly using alarms, which can interrupt the function. However, nested timeouts are not supported, because setting a new alarm will overwrite the previous one. Therefore, if a function wrapped with `TimeoutFunction` calls another function also wrapped with `TimeoutFunction`, the inner timeout will overwrite the outer timeout, leading to unexpected behavior. The recommended usage pattern is to create a new `TimeoutFunction` wrapper for each function call (with no nested `TimeoutFunction`), then immediately call it once and discard it after it finishes.
