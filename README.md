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

### Proj1: search

#### Game intialization

The entrypoint of the game is in `pacman.py` file, specifically the `runGames` function. It is called by the command line interface in the same file. This function initializes the `Game` class and call its `run` method.

The `Game` class is defined in `game.py` file. Its `run` method first call `agent.registerInitialState` method for all agents to let them initialize their internal states. Then it enters the main game loop, where it first calls `observationFunction` to get the current game state, then calls each agent's `agent.getAction` method to get their actions, then applies the actions to the game state using `state.generateSuccessor` method. This loop continues until the game is over (win or lose).

#### Game state

The game state is represented by the `GameState` class defined in `pacman.py` file. This class contains all the information about the current state of the game, including the following:

- `explored` class attribute: all the game state instances in the history
- `data` instance attribute: the underlying `GameStateData` data structure that holds the real game state information

The `GameStateData` class is defined in `game.py` file. It contains the following important attributes:

- `layout`: the `Layout` object that represents the maze layout
- `food`: a `Grid` object representing food positions in the maze (list of list of booleans)
- `capsules`: a list of remaining capsule (power pellets) positions (x,y)
- `agentStates`: a list of `AgentState` objects representing the state of each agent (position, direction, etc.)
- `score`: the current game score
- `_eaten`: whether each agent is eaten in the current transition, represented as a boolean list for all agents
- `_foodEaten`: position (x,y) of food eaten in the current transition, or None if no food eaten in the current transition
- `_foodAdded`: Not used
- `_capsuleEaten`: position (x,y) of capsule eaten in the current transition, or None if no capsule eaten in the current transition
- `_agentMoved`: which agent moved in the current transition
- `_lose`: boolean flag indicating if the game is lost
- `_win`: boolean flag indicating if the game is won
- `scoreChange`: the change in score during the current transition

**When a ghost is eaten (Pacman eats a scared ghost):**

- The ghost immediately revives at its starting position in the same time step (via `GhostRules.placeGhost`)
- The ghost's `scaredTimer` is reset to 0 (no longer scared)
- Pacman gains +200 points
- The `state.data._eaten[agentIndex]` flag is set to `True` for that ghost

**When Pacman is eaten (touched by a non-scared ghost):**

- Pacman does NOT revive - the game ends immediately
- The `state.data._lose` flag is set to `True`
- The score decreases by 500 points

#### `SearchAgent` class

This is the pacman agent in question 1 defined in `search.py`. Its `registerInitialState` method determines all actions before any action is taken. It uses the search algorithms implemented in `search.py` file to find a path to the goal, and store the actions in `self.actions` list. Then its `getAction` method simply returns the next action from `self.actions` list. The current action is tracked by `self.actionIndex` attribute.

#### `PositionSearchProblem` class

This is the input to the search algorithms used by `SearchAgent`. It assumes there is only one agent (one pacman, no ghost), and one single food to reach.