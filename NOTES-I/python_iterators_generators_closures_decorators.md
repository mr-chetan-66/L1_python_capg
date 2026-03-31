# Iterators, Generators, Closures & Decorators in Python
### From Zero to Expert — A Complete Guide

---

# PART 1 — ITERATORS

---

## 🟢 Level 1 — Beginner: What is an Iterator?

An **iterator** is any object you can loop over — one item at a time.

When you write `for x in something`, Python is secretly using an iterator behind the scenes.

```python
nums = [1, 2, 3]
for n in nums:
    print(n)
# Lists are iterable — Python converts them to iterators automatically
```

### `iter()` and `next()`

```python
nums = [10, 20, 30]
it = iter(nums)        # Create an iterator from a list

print(next(it))        # 10
print(next(it))        # 20
print(next(it))        # 30
# print(next(it))      # ❌ StopIteration — no more items
```

> 💡 Every `for` loop calls `iter()` once, then `next()` repeatedly until `StopIteration` is raised.

---

## 🟡 Level 2 — Intermediate: Building Your Own Iterator

Implement `__iter__` and `__next__` to make any class iterable.

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self          # The object itself is the iterator

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for n in Countdown(5):
    print(n)
# Output: 5 4 3 2 1
```

---

## 🔵 Level 3 — Advanced: Infinite Iterators & `itertools`

### Infinite Iterator

```python
class InfiniteCounter:
    def __init__(self, start=0):
        self.n = start

    def __iter__(self):
        return self

    def __next__(self):
        value = self.n
        self.n += 1
        return value

counter = InfiniteCounter()
for i, val in enumerate(counter):
    if i >= 5:
        break
    print(val)   # 0 1 2 3 4
```

### `itertools` — The Iterator Powerhouse

```python
import itertools

# Infinite counter
for n in itertools.count(10, 2):    # Start=10, step=2
    if n > 20: break
    print(n)   # 10 12 14 16 18 20

# Cycle through a list forever
colors = itertools.cycle(["red", "green", "blue"])
for _, c in zip(range(6), colors):
    print(c)   # red green blue red green blue

# Repeat a value
for x in itertools.repeat("hello", 3):
    print(x)   # hello hello hello

# Chain multiple iterables
combined = itertools.chain([1, 2], [3, 4], [5, 6])
print(list(combined))   # [1, 2, 3, 4, 5, 6]

# Combinations and permutations
print(list(itertools.combinations("ABC", 2)))
# [('A','B'), ('A','C'), ('B','C')]

print(list(itertools.permutations("AB", 2)))
# [('A','B'), ('B','A')]
```

---

## 🔴 Level 4 — Expert: Iterator Protocol Internals

### Separate Iterable vs Iterator

```python
class NumberRange:
    """Iterable — can produce multiple independent iterators"""
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        return NumberRangeIterator(self.start, self.end)  # New iterator each time


class NumberRangeIterator:
    """Iterator — tracks position for one traversal"""
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        val = self.current
        self.current += 1
        return val

r = NumberRange(1, 4)
print(list(r))   # [1, 2, 3]
print(list(r))   # [1, 2, 3] — works again! (fresh iterator each time)
```

> 🔑 **Key Insight:** An *iterable* has `__iter__`. An *iterator* has both `__iter__` and `__next__`. Separating them allows multiple independent loops over the same data.

---

# PART 2 — GENERATORS

---

## 🟢 Level 1 — Beginner: What is a Generator?

A **generator** is a special function that **yields** values one at a time, pausing and resuming execution — instead of returning everything at once.

```python
def count_up(n):
    for i in range(1, n + 1):
        yield i       # Pause here, send value out

gen = count_up(3)
print(next(gen))   # 1
print(next(gen))   # 2
print(next(gen))   # 3

# Or use in a loop
for val in count_up(5):
    print(val)
```

> 💡 `yield` turns a function into a generator. The function's state is **frozen** between yields.

---

## 🟡 Level 2 — Intermediate: Generator Expressions & Lazy Evaluation

### Generator Expression (one-liner)

```python
# List comprehension — computes all at once (eager)
squares_list = [x**2 for x in range(1000000)]   # 🐢 Uses lots of memory

# Generator expression — computes on demand (lazy)
squares_gen = (x**2 for x in range(1000000))    # ⚡ Almost no memory used

print(next(squares_gen))   # 0
print(next(squares_gen))   # 1
```

### Real-World Example: Reading a Large File

```python
def read_large_file(filepath):
    with open(filepath, "r") as file:
        for line in file:
            yield line.strip()   # One line at a time — never loads full file

for line in read_large_file("huge_log.txt"):
    if "ERROR" in line:
        print(line)
```

---

## 🔵 Level 3 — Advanced: `send()`, `throw()`, `close()`

Generators are two-way channels — you can also **send data back into** them.

### `send()` — Push data into a generator

```python
def accumulator():
    total = 0
    while True:
        value = yield total    # Yield total OUT, receive new value IN
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)           # Prime the generator (required first step)
print(gen.send(10)) # 10
print(gen.send(20)) # 30
print(gen.send(5))  # 35
```

### `throw()` — Inject an exception into the generator

```python
def safe_gen():
    try:
        yield 1
        yield 2
        yield 3
    except ValueError as e:
        print(f"Caught inside generator: {e}")
        yield -1

gen = safe_gen()
print(next(gen))              # 1
print(gen.throw(ValueError, "bad input"))   # Caught inside generator: bad input → -1
```

### `close()` — Terminate a generator early

```python
def infinite():
    n = 0
    try:
        while True:
            yield n
            n += 1
    except GeneratorExit:
        print("Generator was closed!")

gen = infinite()
print(next(gen))   # 0
print(next(gen))   # 1
gen.close()        # Generator was closed!
```

---

## 🔴 Level 4 — Expert: `yield from` & Coroutines

### `yield from` — Delegate to Sub-Generators

```python
def inner():
    yield 1
    yield 2

def outer():
    yield 0
    yield from inner()   # Delegates to inner generator
    yield 3

print(list(outer()))   # [0, 1, 2, 3]
```

### Chaining Pipelines with Generators

```python
def integers(n):
    yield from range(n)

def squared(seq):
    for x in seq:
        yield x ** 2

def evens_only(seq):
    for x in seq:
        if x % 2 == 0:
            yield x

# Build a lazy pipeline
pipeline = evens_only(squared(integers(10)))
print(list(pipeline))   # [0, 4, 16, 36, 64]
```

### Generator-Based Coroutine Pattern

```python
import asyncio

async def fetch_data(name, delay):
    print(f"{name}: fetching...")
    await asyncio.sleep(delay)
    print(f"{name}: done!")
    return f"{name} result"

async def main():
    results = await asyncio.gather(
        fetch_data("Task A", 2),
        fetch_data("Task B", 1),
    )
    print(results)

asyncio.run(main())
# Task A: fetching...
# Task B: fetching...
# Task B: done!
# Task A: done!
```

---

# PART 3 — CLOSURES

---

## 🟢 Level 1 — Beginner: What is a Closure?

A **closure** is a function that **remembers variables from its enclosing scope**, even after that outer function has finished executing.

```python
def outer():
    message = "Hello from outer!"

    def inner():
        print(message)    # inner() "closes over" message

    return inner

greet = outer()
greet()   # Hello from outer!  — outer() is gone, but message lives on!
```

---

## 🟡 Level 2 — Intermediate: Closures as Function Factories

Use closures to **generate customized functions** at runtime.

```python
def multiplier(factor):
    def multiply(number):
        return number * factor    # factor is captured from outer scope
    return multiply

double = multiplier(2)
triple = multiplier(3)

print(double(5))    # 10
print(triple(5))    # 15
print(double(7))    # 14
```

```python
def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}!"
    return greet

hello = make_greeter("Hello")
hi    = make_greeter("Hi")

print(hello("Alice"))   # Hello, Alice!
print(hi("Bob"))        # Hi, Bob!
```

---

## 🔵 Level 3 — Advanced: `nonlocal`, Mutable State in Closures

### `nonlocal` — Modify Outer Variables

Without `nonlocal`, you can only **read** outer variables. To **modify** them, use `nonlocal`.

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count    # Tell Python to use the outer 'count'
        count += 1
        return count

    return increment

counter = make_counter()
print(counter())   # 1
print(counter())   # 2
print(counter())   # 3
```

### Inspecting a Closure

```python
def outer(x):
    def inner(y):
        return x + y
    return inner

add5 = outer(5)
print(add5.__closure__)                          # (<cell at 0x...>,)
print(add5.__closure__[0].cell_contents)         # 5  ← the captured value
print(add5.__code__.co_freevars)                 # ('x',) ← names of free variables
```

---

## 🔴 Level 4 — Expert: Closures vs Classes & The Cell Object Model

### Closure with Multiple Functions Sharing State

```python
def bank_account(initial_balance):
    balance = initial_balance

    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return "Insufficient funds"
        balance -= amount
        return balance

    def get_balance():
        return balance

    return deposit, withdraw, get_balance

deposit, withdraw, get_balance = bank_account(100)

print(deposit(50))      # 150
print(withdraw(30))     # 120
print(get_balance())    # 120
```

### Classic Closure Trap — Loop Variable Capture

```python
# ❌ Bug: all functions capture the SAME variable 'i'
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])   # [2, 2, 2]  ← NOT what you expect!

# ✅ Fix: use default argument to capture current value
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])   # [0, 1, 2]  ← correct!
```

---

# PART 4 — DECORATORS

---

## 🟢 Level 1 — Beginner: What is a Decorator?

A **decorator** is a function that **wraps another function** to extend or change its behavior — without modifying the original.

```python
def shout(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@shout
def greet():
    return "hello world"

print(greet())   # HELLO WORLD
```

> `@shout` is just syntactic sugar for `greet = shout(greet)`

---

## 🟡 Level 2 — Intermediate: Decorators with Arguments & `functools.wraps`

### Handling Function Arguments

```python
def logger(func):
    def wrapper(*args, **kwargs):       # Accept any arguments
        print(f"Calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(3, 4)
# Calling add with (3, 4) {}
# add returned 7
```

### `functools.wraps` — Preserve Function Identity

```python
import functools

def logger(func):
    @functools.wraps(func)       # ← Preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def multiply(a, b):
    """Multiplies two numbers."""
    return a * b

print(multiply.__name__)   # multiply (not 'wrapper'!)
print(multiply.__doc__)    # Multiplies two numbers.
```

> ⚠️ Always use `@functools.wraps` in production decorators — otherwise debugging becomes painful.

---

## 🔵 Level 3 — Advanced: Decorators with Parameters & Stacking

### Decorator That Accepts Arguments

```python
import functools

def repeat(n):
    """Run the decorated function n times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

say_hello()
# Hello!
# Hello!
# Hello!
```

### Stacking Multiple Decorators

```python
def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return "<b>" + func(*args, **kwargs) + "</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return "<i>" + func(*args, **kwargs) + "</i>"
    return wrapper

@bold
@italic
def text():
    return "Hello"

print(text())   # <b><i>Hello</i></b>
# Applied bottom-up: italic first, then bold wraps around it
```

### Class-Based Decorator

```python
import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call #{self.num_calls} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")   # Call #1 to greet → Hello, Alice!
greet("Bob")     # Call #2 to greet → Hello, Bob!
print(greet.num_calls)   # 2
```

---

## 🔴 Level 4 — Expert: Real-World Production Decorators

### Memoization / Caching

```python
import functools

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))   # Instant! Without memoize: takes forever

# Python ships a built-in version:
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
```

### Retry Decorator

```python
import functools
import time

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise RuntimeError(f"All {max_attempts} attempts failed.")
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
def connect_to_api():
    raise ConnectionError("Network unavailable")

# connect_to_api()
# Attempt 1 failed: Network unavailable
# Attempt 2 failed: Network unavailable
# Attempt 3 failed: Network unavailable
# RuntimeError: All 3 attempts failed.
```

### Timing / Profiling Decorator

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__!r} ran in {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.5)
    return "done"

slow_function()   # 'slow_function' ran in 0.5002s
```

### Type Validation Decorator

```python
import functools
import inspect

def validate_types(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        hints = func.__annotations__
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, value in bound.arguments.items():
            if name in hints:
                expected = hints[name]
                if not isinstance(value, expected):
                    raise TypeError(
                        f"Argument '{name}' must be {expected.__name__}, "
                        f"got {type(value).__name__}"
                    )
        return func(*args, **kwargs)
    return wrapper

@validate_types
def add(a: int, b: int) -> int:
    return a + b

print(add(3, 4))       # 7
# add(3, "four")       # ❌ TypeError: Argument 'b' must be int, got str
```

---

## 📊 Quick Reference Summary

### Iterators
| Concept | Key Points |
|---------|-----------|
| `iter()` / `next()` | Core protocol behind every `for` loop |
| `__iter__` + `__next__` | Make any class iterable |
| `itertools` | `count`, `cycle`, `chain`, `combinations`, `permutations` |
| Iterable vs Iterator | Iterable produces fresh iterators; iterator tracks one traversal |

### Generators
| Concept | Key Points |
|---------|-----------|
| `yield` | Pauses function, returns value, resumes later |
| Generator expression | `(x for x in ...)` — lazy, memory-efficient |
| `send()` | Push data INTO a running generator |
| `yield from` | Delegate to sub-generator, chain pipelines |

### Closures
| Concept | Key Points |
|---------|-----------|
| Free variable | Variable from outer scope captured by inner function |
| `nonlocal` | Allows mutation of outer variable inside closure |
| Function factory | Closures generate customized functions at runtime |
| Loop trap | Default argument `lambda i=i` captures value, not reference |

### Decorators
| Concept | Key Points |
|---------|-----------|
| `@decorator` | Sugar for `func = decorator(func)` |
| `*args, **kwargs` | Makes wrapper accept any function signature |
| `@functools.wraps` | Preserves `__name__`, `__doc__`, metadata |
| Class decorator | Use `__call__` for stateful decorators |
| Parametrized decorator | Three levels of nesting needed |

---

> 💡 **The Bigger Picture:** These four concepts are deeply connected.
> - **Iterators** are the protocol that powers `for` loops.
> - **Generators** are lazy iterators written as functions using `yield`.
> - **Closures** let inner functions remember and use outer state.
> - **Decorators** are closures that wrap functions to add behavior.
>
> Master these four and you'll write Python that is clean, efficient, and truly Pythonic.
