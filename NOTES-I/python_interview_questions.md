# Python Interview Questions — Tricky & Ambiguous
### File Handling | Iterators, Generators, Closures & Decorators | Multithreading

---

> ⚠️ These questions are **deliberately ambiguous or misleading** — the kind that trip you up in real interviews. Each answer explains not just *what* but *why*.

---

# 📁 SECTION 1 — FILE HANDLING

---

### Q1. What happens when you open a file with `"w"` mode but never write anything to it?

**Trap:** Most people assume nothing changes. They're wrong.

**Answer:**
The file is **immediately truncated to zero bytes** the moment `open("file.txt", "w")` is called — even before any `write()`. If the file had existing content, it's gone.

```python
# file.txt has content: "important data"

f = open("file.txt", "w")
# At this point — file is already EMPTY
# No write was ever called!
f.close()

with open("file.txt", "r") as f:
    print(f.read())   # "" — content is gone!
```

**Safe alternative:** Use `"a"` mode if you only want to add, or check before writing.

---

### Q2. Is it possible for `file.read()` to return an empty string even if the file has content?

**Trap:** Sounds impossible. It isn't.

**Answer:**
Yes — if you call `read()` twice on the same file object, the second call returns `""` because the **file cursor is already at the end**.

```python
with open("data.txt", "r") as f:
    content1 = f.read()    # "Hello World"
    content2 = f.read()    # "" ← cursor already at EOF

    f.seek(0)              # Reset cursor to beginning
    content3 = f.read()    # "Hello World" ← works again
```

**Follow-up:** Same happens with `readline()` at EOF — returns `""` not `None`.

---

### Q3. What is the difference between `read()`, `readline()`, and `readlines()`? Which one should you use for a 50 GB log file?

**Answer:**

| Method | Returns | Loads entire file? |
|--------|---------|-------------------|
| `read()` | One big string | ✅ Yes |
| `readline()` | One line | ❌ No |
| `readlines()` | List of all lines | ✅ Yes |

For a 50 GB file: **none of the above**. Use direct iteration:

```python
# ✅ Memory-efficient — reads one line at a time
with open("huge.log", "r") as f:
    for line in f:               # Python handles buffering internally
        process(line)
```

Direct iteration is the most memory-efficient because Python uses **buffered I/O internally** — no full file load.

---

### Q4. Does `with open(...) as f:` guarantee the file is written to disk?

**Trap:** Everyone says `with` is safe. It is — but for the OS, not hardware.

**Answer:**
`with` guarantees `f.close()` is called, which **flushes Python's internal buffer to the OS**. But the OS may still cache it in its own buffer. The data may not reach physical disk until the OS decides to flush.

```python
with open("critical.txt", "w") as f:
    f.write("important data")
# File is closed — data is in OS buffer

# To GUARANTEE it hits disk:
import os
with open("critical.txt", "w") as f:
    f.write("important data")
    f.flush()          # Flush Python buffer → OS buffer
    os.fsync(f.fileno())  # Force OS buffer → physical disk
```

---

### Q5. Can two processes safely write to the same file at the same time?

**Answer:**
Not by default. Without coordination, writes **interleave unpredictably** and corrupt each other.

```python
# Process 1 writes "Hello"
# Process 2 writes "World"
# File might end up: "HWeorlllod" ← garbage
```

**Fix — Use file locking:**

```python
import fcntl  # Unix

with open("shared.txt", "a") as f:
    fcntl.flock(f, fcntl.LOCK_EX)   # Exclusive lock
    f.write("Safe line\n")
    fcntl.flock(f, fcntl.LOCK_UN)   # Release
```

---

### Q6. What is the difference between `"r"` and `"rb"` mode? When does it actually matter?

**Answer:**
In `"r"` (text) mode, Python performs **newline translation**:
- Windows: `\r\n` → `\n` on read, `\n` → `\r\n` on write
- Unix: no translation

In `"rb"` (binary) mode: **no translation — raw bytes**.

It matters when:
1. Reading binary files (images, ZIPs) — text mode corrupts them
2. Cross-platform text processing — binary mode gives you the raw `\r\n`
3. Checking exact file size or byte offsets

```python
# On Windows:
with open("file.txt", "r") as f:
    data = f.read()    # \r\n becomes \n — byte count changes!

with open("file.txt", "rb") as f:
    data = f.read()    # Raw bytes — \r\n preserved
```

---

### Q7. You have a generator that yields lines from a file. The file is opened inside the generator. What happens if you never exhaust the generator?

**Trap:** Sounds like a theoretical concern — it's a real production bug.

**Answer:**
If you don't fully consume the generator, the `with` block inside never exits, and **the file stays open** until the generator is garbage collected. In CPython (reference counting GC) this may close quickly — but in PyPy or if there are reference cycles, it could leak for a long time.

```python
def read_lines(path):
    with open(path, "r") as f:     # File opened here
        for line in f:
            yield line
    # File closes here — only when generator is exhausted OR garbage collected

gen = read_lines("data.txt")
first = next(gen)   # File is open
# Never call next() again...
# File may stay open until 'gen' is garbage collected
```

**Fix:** Use `try/finally` or call `gen.close()` explicitly when done early.

---

# 🔁 SECTION 2 — ITERATORS, GENERATORS, CLOSURES & DECORATORS

---

### Q8. What is the difference between an *iterable* and an *iterator*? Is a list an iterator?

**Trap:** People confuse these constantly.

**Answer:**

- **Iterable:** Has `__iter__()` — can produce an iterator. E.g., list, tuple, string, dict.
- **Iterator:** Has both `__iter__()` AND `__next__()` — tracks position, yields one item at a time.

A **list is iterable but NOT an iterator**:

```python
lst = [1, 2, 3]

# List is iterable
iter_obj = iter(lst)    # Creates an iterator FROM the list

# List has no __next__
next(lst)               # ❌ TypeError: 'list' object is not an iterator
next(iter_obj)          # ✅ 1
```

**Key difference:** You can loop over a list multiple times. An iterator is **one-use only** — once exhausted, it's done.

```python
it = iter([1, 2, 3])
print(list(it))   # [1, 2, 3]
print(list(it))   # [] ← exhausted!
```

---

### Q9. What does this code output? (Generator + loop trap)

```python
def gen():
    for i in range(3):
        yield i * 2

g = gen()
print(list(g))
print(list(g))
```

**Answer:**
```
[0, 2, 4]
[]
```

**Why:** Generators are **single-use**. After `list(g)` exhausts it, the generator is at EOF. The second `list(g)` gets nothing. This is a very common interview trap.

---

### Q10. What is the output of this closure code?

```python
funcs = []
for i in range(4):
    funcs.append(lambda: i)

print([f() for f in funcs])
```

**Trap:** Many expect `[0, 1, 2, 3]`.

**Answer:**
```
[3, 3, 3, 3]
```

**Why:** All lambdas close over the **same variable `i`** — not its value at time of creation. When called, they all read the **current value of `i`**, which is `3` after the loop finishes.

**Fix:**
```python
funcs = [lambda i=i: i for i in range(4)]
print([f() for f in funcs])   # [0, 1, 2, 3] ✅
```

By using a **default argument**, each lambda captures the *value* of `i` at definition time.

---

### Q11. What is the difference between `return` and `yield` in a function? Can they coexist?

**Answer:**
- `return` exits the function and returns a value (once).
- `yield` pauses the function, returns a value, and **resumes from that point** on the next call.

Yes, they **can coexist** in Python 3 — but `return` in a generator signals `StopIteration`:

```python
def limited_gen(n):
    for i in range(n):
        if i == 3:
            return "early stop"   # Raises StopIteration with value "early stop"
        yield i

g = limited_gen(10)
print(list(g))     # [0, 1, 2]

# To capture return value:
try:
    while True:
        next(g)
except StopIteration as e:
    print(e.value)   # "early stop"
```

---

### Q12. Can a decorator break `functools.wraps`? What metadata does `wraps` actually preserve?

**Answer:**
`@functools.wraps(func)` copies these attributes from `func` to `wrapper`:

- `__name__` — function name
- `__doc__` — docstring
- `__module__` — module name
- `__qualname__` — qualified name
- `__annotations__` — type hints
- `__dict__` — user-defined attributes
- `__wrapped__` — reference to the original function

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name: str) -> str:
    """Returns a greeting."""
    return f"Hello, {name}"

print(greet.__name__)          # greet ✅ (not 'wrapper')
print(greet.__doc__)           # Returns a greeting. ✅
print(greet.__wrapped__)       # <function greet> — original!
print(greet.__annotations__)   # {'name': str, 'return': str} ✅
```

**What wraps does NOT fix:** The actual function signature visible to `inspect.signature()` may still show `(*args, **kwargs)` unless you use `inspect` tricks.

---

### Q13. What is the output of this stacked decorator code?

```python
def decorator_a(func):
    print("A applied")
    def wrapper():
        print("A before")
        func()
        print("A after")
    return wrapper

def decorator_b(func):
    print("B applied")
    def wrapper():
        print("B before")
        func()
        print("B after")
    return wrapper

@decorator_a
@decorator_b
def hello():
    print("Hello!")

hello()
```

**Answer:**
```
B applied
A applied
B before
A before
Hello!
A after
B after
```

**Why:** Decorators are applied **bottom-up** at definition time (`B` first, then `A`). But they execute **top-down** (outer first) at call time.

`@decorator_a @decorator_b def hello` → `hello = decorator_a(decorator_b(hello))`

---

### Q14. What's the difference between `yield` and `yield from`?

**Answer:**

`yield` yields one value from the current generator.
`yield from` **delegates entirely** to a sub-iterable — passing values, `send()` calls, and exceptions through:

```python
# With yield:
def gen_a():
    for x in [1, 2, 3]:
        yield x          # Must manually iterate

# With yield from:
def gen_b():
    yield from [1, 2, 3]  # Delegates completely

# Both produce same output, but yield from also:
# - Passes send() values into the sub-generator
# - Forwards throw() and close()
# - Returns the sub-generator's return value
```

```python
def sub():
    x = yield "ready"
    yield f"got: {x}"

def main():
    result = yield from sub()   # Transparent delegation

g = main()
print(next(g))        # "ready"
print(g.send("hi"))   # "got: hi"
```

---

### Q15. Can `__next__` raise something other than `StopIteration` to stop iteration?

**Trap:** Most say no.

**Answer:**
`StopIteration` is the **only signal** that tells a `for` loop to stop cleanly. Any other exception propagates up and crashes the loop:

```python
class WeirdIter:
    def __init__(self):
        self.n = 3

    def __iter__(self):
        return self

    def __next__(self):
        if self.n == 0:
            raise ValueError("done")   # ❌ NOT StopIteration
        self.n -= 1
        return self.n

for x in WeirdIter():
    print(x)
# Prints 2, 1, 0... then raises ValueError — does NOT stop silently!
```

---

### Q16. What is a `nonlocal` variable? How is it different from `global`?

**Answer:**

| Keyword | Scope modified |
|---------|---------------|
| `global` | Top-level module scope |
| `nonlocal` | Nearest enclosing *function* scope (not module) |

```python
x = "global"

def outer():
    x = "outer"

    def inner():
        nonlocal x         # Refers to outer's x
        x = "modified"
        print(x)           # "modified"

    inner()
    print(x)               # "modified" ← outer's x changed

outer()
print(x)                   # "global" ← module x unchanged
```

`nonlocal` cannot refer to global variables — only to enclosing *function* scopes.

---

# 🧵 SECTION 3 — MULTITHREADING

---

### Q17. If Python has the GIL, what's the point of multithreading at all?

**Trap:** Many candidates dismiss threads entirely because of the GIL.

**Answer:**
The GIL only blocks **CPU-bound** parallelism. For **I/O-bound** tasks, the GIL is **released** while waiting — so threads do run concurrently during I/O.

```
Thread 1: [CPU]─wait for network──[CPU]─wait for disk──[CPU]
Thread 2:        [CPU]────────────[CPU]────────────────[CPU]
                   ↑ GIL released during waits — real concurrency!
```

**Use threads for:** Network requests, DB queries, file reads, sleep, HTTP calls.
**Use multiprocessing for:** Math-heavy code, image processing, ML model inference.

---

### Q18. What happens if you don't call `t.join()` on a non-daemon thread?

**Trap:** People think the thread is just "lost." That's not quite right.

**Answer:**
The main program will **wait for all non-daemon threads** to finish before exiting — even without `join()`. But `join()` is still important for:

1. **Knowing when a thread is done** in your code flow
2. **Catching exceptions** (thread exceptions don't propagate to main automatically)
3. **Ordered cleanup**

```python
import threading, time

def task():
    time.sleep(2)
    print("Thread done")

t = threading.Thread(target=task)
t.start()
print("Main done")
# Output:
# Main done
# Thread done  ← program waited 2s because t is non-daemon!
```

With `daemon=True`, main exits immediately and kills the thread.

---

### Q19. What is a race condition? Write a minimal example and its fix.

**Answer:**
A race condition occurs when the **outcome depends on the unpredictable order** in which threads execute.

```python
import threading

# ❌ Race condition
balance = 1000

def withdraw(amount):
    global balance
    if balance >= amount:           # Thread A checks: 1000 >= 800 ✅
                                    # Thread B checks: 1000 >= 800 ✅ (same time!)
        balance -= amount           # Thread A: 1000 - 800 = 200
                                    # Thread B: 200 - 800 = -600 ❌

t1 = threading.Thread(target=withdraw, args=(800,))
t2 = threading.Thread(target=withdraw, args=(800,))
t1.start(); t2.start()
t1.join(); t2.join()
print(balance)   # Could be -600 !
```

```python
# ✅ Fix with Lock
lock = threading.Lock()
balance = 1000

def safe_withdraw(amount):
    global balance
    with lock:                  # Only one thread enters at a time
        if balance >= amount:
            balance -= amount

t1 = threading.Thread(target=safe_withdraw, args=(800,))
t2 = threading.Thread(target=safe_withdraw, args=(800,))
t1.start(); t2.start()
t1.join(); t2.join()
print(balance)   # Always 200 ✅
```

---

### Q20. What is a deadlock? Give an interview-ready example.

**Answer:**
A deadlock is when two (or more) threads each **hold a lock the other needs** — and both wait forever.

```python
import threading
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread1():
    with lock_a:
        import time; time.sleep(0.1)   # Pause, giving Thread 2 time to grab B
        with lock_b:                   # ← WAITS FOREVER for lock_b
            print("Thread 1 done")

def thread2():
    with lock_b:
        with lock_a:                   # ← WAITS FOREVER for lock_a
            print("Thread 2 done")

# Both threads freeze — program hangs forever
```

**Four conditions for deadlock (all must be true):**
1. Mutual exclusion — resource held by one thread at a time
2. Hold and wait — thread holds one lock while waiting for another
3. No preemption — locks can't be forcibly taken
4. Circular wait — Thread 1 waits for Thread 2, Thread 2 waits for Thread 1

**Fix — always acquire locks in the same order:**
```python
def thread1_safe():
    with lock_a:
        with lock_b:
            print("T1 done")

def thread2_safe():
    with lock_a:    # Same order as thread1!
        with lock_b:
            print("T2 done")
```

---

### Q21. What is the difference between `Lock` and `RLock`?

**Answer:**

| | `Lock` | `RLock` |
|--|--------|---------|
| Same thread acquires twice | 🔴 Deadlock | ✅ Allowed |
| Different thread releases | ✅ Allowed | 🔴 Not allowed |
| Use case | Simple mutual exclusion | Recursive functions sharing a lock |

```python
import threading

lock = threading.Lock()
rlock = threading.RLock()

def recursive_with_lock(n):
    with lock:         # ❌ Deadlocks on second call — same thread!
        if n > 0:
            recursive_with_lock(n - 1)

def recursive_with_rlock(n):
    with rlock:        # ✅ Same thread can acquire multiple times
        if n > 0:
            recursive_with_rlock(n - 1)
```

---

### Q22. You launch 100 threads to call an API. Some fail with exceptions. How do you catch them?

**Trap:** Many candidates don't realize thread exceptions are swallowed silently.

**Answer:**
Exceptions inside threads **do NOT propagate** to the main thread. You must capture them explicitly.

```python
import threading

results = {}
errors = {}
lock = threading.Lock()

def call_api(endpoint_id):
    try:
        # Simulate: odd IDs fail
        if endpoint_id % 2 != 0:
            raise ValueError(f"Endpoint {endpoint_id} failed")
        result = f"Data from {endpoint_id}"
        with lock:
            results[endpoint_id] = result
    except Exception as e:
        with lock:
            errors[endpoint_id] = str(e)

threads = [threading.Thread(target=call_api, args=(i,)) for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()

print("Results:", results)
print("Errors:", errors)
```

**Better approach — use `ThreadPoolExecutor` which surfaces exceptions via `future.result()`:**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def call_api(endpoint_id):
    if endpoint_id % 2 != 0:
        raise ValueError(f"Endpoint {endpoint_id} failed")
    return f"Data from {endpoint_id}"

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(call_api, i): i for i in range(10)}
    for future in as_completed(futures):
        eid = futures[future]
        try:
            print(f"{eid}: {future.result()}")
        except ValueError as e:
            print(f"{eid}: ERROR — {e}")
```

---

### Q23. What is `threading.local()` and when is it essential?

**Answer:**
`threading.local()` creates a storage object where each thread has its **own independent copy** of attributes. Changes in one thread are invisible to others.

**Classic use case — database connections per thread:**

```python
import threading

_thread_local = threading.local()

def get_db_connection():
    if not hasattr(_thread_local, "connection"):
        _thread_local.connection = create_new_connection()   # One per thread
    return _thread_local.connection

def handle_request(request_id):
    conn = get_db_connection()
    # Each thread uses its own connection — no sharing, no locking needed
```

**Without `threading.local()`:** All threads share the same connection object — concurrent queries corrupt each other.

---

### Q24. What is the difference between `Semaphore` and `BoundedSemaphore`?

**Answer:**
Both limit concurrent access. The difference is in `release()`:

- `Semaphore`: `release()` can be called **more times than `acquire()`** — counter goes above initial value (potential bug)
- `BoundedSemaphore`: raises `ValueError` if released more than the initial count — **catches accidental over-releasing**

```python
import threading

sem = threading.Semaphore(2)
sem.acquire()
sem.release()
sem.release()   # ← Now counter is 3 (above initial 2!) — silent bug

bsem = threading.BoundedSemaphore(2)
bsem.acquire()
bsem.release()
bsem.release()   # ← ValueError: Semaphore released too many times ✅ caught!
```

**Rule:** Prefer `BoundedSemaphore` in production — it exposes logic errors.

---

### Q25. Is `+=` on a list thread-safe? What about `append()`?

**Trap:** Many think operations on Python built-ins are always safe.

**Answer:**

`list.append()` — **thread-safe** in CPython (single opcode, GIL not released mid-operation).

`list += [item]` — **NOT thread-safe** — it's a compound read-modify-write operation.

```python
import threading

lst = []

def add_items():
    for _ in range(1000):
        lst.append("x")   # ✅ Safe in CPython

# But this is NOT safe:
shared = []
def unsafe_extend():
    for _ in range(1000):
        shared += ["x"]   # ❌ Not atomic — race condition possible
```

> ⚠️ This is CPython-specific. Never rely on GIL for thread safety — it's an implementation detail, not a guarantee.

---

### Q26. When should you use `asyncio` instead of `threading`?

**Answer:**

| | `threading` | `asyncio` |
|--|------------|----------|
| Model | Preemptive (OS switches) | Cooperative (you yield control) |
| Overhead | ~1MB per thread (stack) | ~few KB per coroutine |
| Scale | Hundreds of threads | Tens of thousands of coroutines |
| Best for | Blocking I/O, legacy libs | High-concurrency I/O (web servers, bots) |
| Shared state | Needs locks | Single-threaded — no data races |

```python
# Threading — 1000 concurrent requests hits OS limits
# asyncio — 100,000 concurrent requests is routine

import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, f"https://api.example.com/{i}") for i in range(1000)]
        results = await asyncio.gather(*tasks)   # 1000 concurrent, one thread!
```

---

## 📊 MASTER QUICK REFERENCE

### Ambiguity Cheat Sheet

| Question | Surprising Answer |
|----------|-----------------|
| Does `with open("f","w")` truncate immediately? | **Yes** — even before `write()` |
| Does `read()` always return content? | **No** — returns `""` if cursor at EOF |
| Is a list an iterator? | **No** — iterable only, not iterator |
| Does `list(gen)` twice work? | **No** — generators are single-use |
| Do stacked decorators apply top-down? | **No** — bottom-up at definition, top-down at call |
| Does `+=` in a loop closure capture value or reference? | **Reference** — all share same variable |
| Does the GIL make threading useless? | **No** — GIL released during I/O |
| Do thread exceptions propagate to main? | **No** — silently swallowed |
| Is `list.append()` thread-safe? | **Yes** in CPython — but don't rely on it |
| Can a Lock deadlock with itself? | **Yes** — use RLock for recursive use |
| Does `with open()` guarantee disk write? | **No** — use `flush()` + `os.fsync()` for that |
| Can `yield` and `return` coexist? | **Yes** — `return` signals StopIteration in generators |

---

> 💡 **Interview Tip:** When you see a question about threads, always ask: *"Is this I/O-bound or CPU-bound?"* — that one question unlocks the entire design decision tree.
