# Multithreading in Python
### From Zero to Expert — A Complete Guide

---

## 🧠 Before We Begin: What is a Thread?

A **thread** is the smallest unit of execution within a program. Every Python program starts with one thread — the **main thread**. Multithreading lets you run multiple threads **concurrently** inside the same process, sharing the same memory space.

```
Process (your Python program)
├── Main Thread   → runs your main code
├── Thread-2      → runs task A concurrently
└── Thread-3      → runs task B concurrently
```

> ⚠️ **Python's GIL (Global Interpreter Lock):** Python only allows **one thread to execute Python bytecode at a time**. This means threads don't run in true parallel for CPU work — but they *do* overlap for I/O-bound tasks (network calls, file reads, sleep). More on this at the expert level.

---

# 🟢 LEVEL 1 — Beginner: Creating and Running Threads

---

### Your First Thread

```python
import threading

def greet(name):
    print(f"Hello, {name}!")

# Create a thread
t = threading.Thread(target=greet, args=("Alice",))

# Start the thread
t.start()

# Wait for it to finish
t.join()

print("Main thread done.")
```

```
Output:
Hello, Alice!
Main thread done.
```

---

### Running Multiple Threads

```python
import threading
import time

def task(name, delay):
    time.sleep(delay)
    print(f"{name} finished after {delay}s")

t1 = threading.Thread(target=task, args=("Task A", 2))
t2 = threading.Thread(target=task, args=("Task B", 1))
t3 = threading.Thread(target=task, args=("Task C", 3))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print("All tasks done.")
```

```
Output (order may vary):
Task B finished after 1s
Task A finished after 2s
Task C finished after 3s
All tasks done.
```

> 💡 Without threading, this would take 6 seconds total. With threads: only ~3 seconds (the longest task).

---

### Thread with Keyword Arguments

```python
import threading

def display(message, repeat=1):
    for _ in range(repeat):
        print(message)

t = threading.Thread(target=display, kwargs={"message": "Hi!", "repeat": 3})
t.start()
t.join()
```

---

### Checking Thread Info

```python
import threading

print(threading.current_thread().name)   # MainThread
print(threading.active_count())          # Number of active threads
print(threading.enumerate())             # List of all active threads
```

---

# 🟡 LEVEL 2 — Intermediate: Thread Class, Daemon Threads & Safety

---

### Subclassing `threading.Thread`

A cleaner, object-oriented way to define threads:

```python
import threading
import time

class WorkerThread(threading.Thread):
    def __init__(self, name, duration):
        super().__init__()
        self.name = name
        self.duration = duration

    def run(self):
        print(f"{self.name} started")
        time.sleep(self.duration)
        print(f"{self.name} completed")

workers = [WorkerThread(f"Worker-{i}", i) for i in range(1, 4)]

for w in workers:
    w.start()

for w in workers:
    w.join()

print("All workers done.")
```

---

### Daemon Threads

A **daemon thread** runs in the background and is **automatically killed** when the main program exits — ideal for background monitoring tasks.

```python
import threading
import time

def background_monitor():
    while True:
        print("💓 Heartbeat check...")
        time.sleep(1)

monitor = threading.Thread(target=background_monitor, daemon=True)
monitor.start()

print("Main program running...")
time.sleep(3)
print("Main program exiting. Daemon will be killed automatically.")
```

```
Output:
Main program running...
💓 Heartbeat check...
💓 Heartbeat check...
💓 Heartbeat check...
Main program exiting. Daemon will be killed automatically.
```

> ⚠️ Non-daemon threads prevent the program from exiting. Daemon threads do not.

---

### The Race Condition Problem

When multiple threads **read and modify shared data** at the same time, you get unpredictable results:

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1   # ← NOT thread-safe! Read-modify-write is 3 operations

threads = [threading.Thread(target=increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Expected: 500000, Got: {counter}")
# Got: 387432  ← Different every run! Race condition!
```

---

### Fixing Race Conditions with `Lock`

```python
import threading

counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    for _ in range(100_000):
        with lock:          # Only one thread can be here at a time
            counter += 1

threads = [threading.Thread(target=safe_increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Expected: 500000, Got: {counter}")
# Got: 500000 ✅ Always correct!
```

> 💡 `with lock:` automatically acquires and releases the lock — even if an exception occurs.

---

# 🔵 LEVEL 3 — Advanced: Synchronization Primitives

---

### `RLock` — Reentrant Lock

A regular `Lock` will **deadlock** if the same thread tries to acquire it twice. `RLock` (Reentrant Lock) allows the same thread to acquire it multiple times:

```python
import threading

rlock = threading.RLock()

def outer():
    with rlock:
        print("Outer acquired")
        inner()   # Same thread acquires again — safe with RLock!

def inner():
    with rlock:
        print("Inner acquired")

t = threading.Thread(target=outer)
t.start()
t.join()
# Outer acquired
# Inner acquired
```

---

### `Semaphore` — Limit Concurrent Access

A `Semaphore` controls how many threads can access a resource simultaneously:

```python
import threading
import time

# Only 3 threads can download at the same time
semaphore = threading.Semaphore(3)

def download(file_id):
    with semaphore:
        print(f"Downloading file {file_id}...")
        time.sleep(2)
        print(f"File {file_id} done.")

threads = [threading.Thread(target=download, args=(i,)) for i in range(8)]
for t in threads: t.start()
for t in threads: t.join()
```

---

### `Event` — Signal Between Threads

An `Event` lets one thread **signal** others to proceed:

```python
import threading
import time

ready_event = threading.Event()

def worker():
    print("Worker: waiting for signal...")
    ready_event.wait()     # Block until event is set
    print("Worker: signal received! Starting work.")

def controller():
    time.sleep(2)
    print("Controller: sending start signal!")
    ready_event.set()      # Unblocks all waiting threads

t1 = threading.Thread(target=worker)
t2 = threading.Thread(target=worker)
t3 = threading.Thread(target=controller)

t1.start()
t2.start()
t3.start()

t1.join(); t2.join(); t3.join()
```

```
Output:
Worker: waiting for signal...
Worker: waiting for signal...
Controller: sending start signal!
Worker: signal received! Starting work.
Worker: signal received! Starting work.
```

---

### `Condition` — Advanced Wait/Notify

A `Condition` combines a Lock with the ability to **wait for a specific condition** to be true:

```python
import threading
import time
from collections import deque

queue = deque()
condition = threading.Condition()

def producer():
    for i in range(5):
        time.sleep(0.5)
        with condition:
            queue.append(f"item-{i}")
            print(f"Produced: item-{i}")
            condition.notify()      # Wake up one waiting consumer

def consumer():
    consumed = 0
    while consumed < 5:
        with condition:
            while not queue:
                condition.wait()    # Release lock and wait for notify
            item = queue.popleft()
            print(f"  Consumed: {item}")
            consumed += 1

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start(); t2.start()
t1.join(); t2.join()
```

---

### `Barrier` — Synchronize a Group of Threads

A `Barrier` makes all threads **wait until everyone has reached the checkpoint**, then releases them together:

```python
import threading
import time
import random

barrier = threading.Barrier(4)   # Wait for 4 threads

def racer(name):
    prep_time = random.uniform(0.5, 2)
    time.sleep(prep_time)
    print(f"{name} is ready! (prep took {prep_time:.2f}s)")
    barrier.wait()               # Wait until all 4 are ready
    print(f"🏁 {name} starts racing!")

racers = ["Alice", "Bob", "Carol", "Dave"]
threads = [threading.Thread(target=racer, args=(name,)) for name in racers]
for t in threads: t.start()
for t in threads: t.join()
```

---

### `ThreadLocal` — Per-Thread Private Storage

`threading.local()` gives each thread its **own isolated copy** of a variable:

```python
import threading

local_data = threading.local()

def process_request(user_id):
    local_data.user = user_id     # Each thread stores its own user
    print(f"Thread {threading.current_thread().name}: user = {local_data.user}")

threads = [
    threading.Thread(target=process_request, args=(f"user_{i}",), name=f"T{i}")
    for i in range(5)
]
for t in threads: t.start()
for t in threads: t.join()
# Each thread sees only its own user — no cross-contamination
```

---

# 🔴 LEVEL 4 — Expert: ThreadPoolExecutor, Queues & the GIL

---

### `ThreadPoolExecutor` — The Modern Standard

`concurrent.futures.ThreadPoolExecutor` manages a pool of worker threads for you — no manual `start()` or `join()`:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_data(url_id):
    time.sleep(1)    # Simulate network call
    return f"Data from URL-{url_id}"

# Submit all tasks, collect as they complete
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_data, i): i for i in range(10)}

    for future in as_completed(futures):
        url_id = futures[future]
        result = future.result()
        print(f"URL-{url_id} → {result}")
```

### `map()` for Simpler Batch Work

```python
from concurrent.futures import ThreadPoolExecutor

def square(n):
    return n * n

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(square, range(10)))

print(results)   # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

---

### Thread-Safe Queue (`queue.Queue`)

`queue.Queue` is the correct way to pass data between threads — it handles all locking internally:

```python
import threading
import queue
import time

task_queue = queue.Queue()

def producer():
    for i in range(10):
        task_queue.put(f"task-{i}")
        print(f"Queued: task-{i}")
        time.sleep(0.2)
    task_queue.put(None)   # Sentinel to stop consumer

def consumer():
    while True:
        item = task_queue.get()
        if item is None:
            break
        print(f"  Processing: {item}")
        time.sleep(0.4)
        task_queue.task_done()

p = threading.Thread(target=producer)
c = threading.Thread(target=consumer)
p.start(); c.start()
p.join(); c.join()
```

### Priority Queue

```python
import queue

pq = queue.PriorityQueue()
pq.put((3, "low priority task"))
pq.put((1, "urgent task"))
pq.put((2, "medium task"))

while not pq.empty():
    priority, task = pq.get()
    print(f"[{priority}] {task}")

# Output (sorted by priority):
# [1] urgent task
# [2] medium task
# [3] low priority task
```

---

### The GIL — Deep Dive

The **Global Interpreter Lock (GIL)** is a mutex inside CPython that ensures only one thread runs Python bytecode at a time.

```
WITHOUT GIL (ideal):          WITH GIL (reality for CPU work):
Thread 1: ████████            Thread 1: ██__██__██
Thread 2: ████████            Thread 2: __██__██__
Result:   Truly parallel      Result:   Interleaved (not parallel)
```

**When threads HELP despite the GIL:**
```python
# ✅ I/O-bound tasks — GIL is released during I/O waits
import threading, requests

urls = ["https://example.com"] * 10

def fetch(url):
    requests.get(url)   # GIL released during network wait!

threads = [threading.Thread(target=fetch, args=(u,)) for u in urls]
for t in threads: t.start()
for t in threads: t.join()
# ~5x faster than sequential
```

**When threads DON'T help (use multiprocessing instead):**
```python
# ❌ CPU-bound tasks — GIL prevents true parallelism
import threading

def crunch(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

# Two threads crunching: NOT faster than sequential!
# Use multiprocessing.Pool instead for CPU work.
```

---

### Avoiding Deadlocks

A **deadlock** occurs when two threads each hold a lock the other needs:

```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

# ❌ Deadlock: Thread 1 holds A, waits for B
#              Thread 2 holds B, waits for A
def thread1():
    with lock_a:
        import time; time.sleep(0.1)
        with lock_b:     # ← Waits forever
            print("Thread 1 done")

def thread2():
    with lock_b:
        with lock_a:     # ← Waits forever
            print("Thread 2 done")

# ✅ Fix: Always acquire locks in the same order
def thread1_safe():
    with lock_a:
        with lock_b:
            print("Thread 1 done")

def thread2_safe():
    with lock_a:     # Same order as thread1!
        with lock_b:
            print("Thread 2 done")
```

---

### Real-World Pattern: Web Scraper with Thread Pool

```python
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

# Simulate scraping
def scrape_page(url):
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    return {"url": url, "status": 200, "time": round(delay, 2)}

urls = [f"https://example.com/page/{i}" for i in range(20)]

results = []
lock = threading.Lock()

def scrape_and_collect(url):
    data = scrape_page(url)
    with lock:
        results.append(data)
    return data

print(f"Scraping {len(urls)} pages with 5 workers...\n")
start = time.time()

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(scrape_and_collect, url) for url in urls]
    for future in as_completed(futures):
        r = future.result()
        print(f"✅ {r['url']} — {r['time']}s")

elapsed = time.time() - start
print(f"\nDone! Scraped {len(results)} pages in {elapsed:.2f}s")
```

---

### Thread-Safe Singleton Pattern

```python
import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:   # Double-checked locking
                    cls._instance = super().__new__(cls)
                    print("Creating DB connection...")
        return cls._instance

# Multiple threads getting the "same" connection
def get_connection():
    db = DatabaseConnection()
    print(f"Got instance: {id(db)}")

threads = [threading.Thread(target=get_connection) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
# "Creating DB connection..." printed only ONCE ✅
```

---

### Monitoring Thread Health with Watchdog

```python
import threading
import time

class WatchdogThread(threading.Thread):
    def __init__(self, workers, check_interval=2):
        super().__init__(daemon=True)
        self.workers = workers
        self.check_interval = check_interval

    def run(self):
        while True:
            alive = [w.name for w in self.workers if w.is_alive()]
            dead  = [w.name for w in self.workers if not w.is_alive()]
            print(f"[Watchdog] Alive: {alive} | Dead: {dead}")
            time.sleep(self.check_interval)

def worker(name, duration):
    time.sleep(duration)

workers = [
    threading.Thread(target=worker, args=(f"W{i}", i * 1.5), name=f"W{i}")
    for i in range(1, 5)
]

watchdog = WatchdogThread(workers)
watchdog.start()

for w in workers: w.start()
for w in workers: w.join()
```

---

## 📊 Quick Reference Summary

### Threading Basics
| Tool | Use Case |
|------|----------|
| `threading.Thread` | Create and run a thread |
| `t.start()` | Begin thread execution |
| `t.join()` | Wait for thread to finish |
| `daemon=True` | Background thread, killed with main program |
| `threading.local()` | Per-thread isolated storage |

### Synchronization Primitives
| Primitive | Purpose |
|-----------|---------|
| `Lock` | Mutual exclusion — one thread at a time |
| `RLock` | Re-entrant lock — same thread can acquire multiple times |
| `Semaphore` | Limit N concurrent threads in a section |
| `Event` | One thread signals others to proceed |
| `Condition` | Wait for a specific condition (producer-consumer) |
| `Barrier` | Synchronize N threads at a checkpoint |

### Higher-Level Tools
| Tool | Use Case |
|------|----------|
| `ThreadPoolExecutor` | Managed pool of worker threads |
| `as_completed()` | Process futures as they finish |
| `queue.Queue` | Thread-safe data passing between threads |
| `queue.PriorityQueue` | Process tasks by priority |

### GIL Decision Guide
| Workload Type | Best Tool |
|---------------|-----------|
| I/O-bound (network, files, DB) | `threading` ✅ |
| CPU-bound (math, parsing, ML) | `multiprocessing` ✅ |
| Async I/O (many connections) | `asyncio` ✅ |
| Mix of CPU + I/O | `ProcessPoolExecutor` + `ThreadPoolExecutor` |

---

> 💡 **Golden Rules of Multithreading:**
> 1. **Use threads for I/O-bound work** — network calls, file reads, DB queries.
> 2. **Use `ThreadPoolExecutor`** over raw threads for production code.
> 3. **Always use `with lock:`** — never `lock.acquire()` without a guaranteed `release()`.
> 4. **Acquire locks in a consistent order** to prevent deadlocks.
> 5. **Use `queue.Queue`** to share data between threads — avoid raw shared globals.
> 6. **For CPU-bound tasks**, switch to `multiprocessing` — the GIL will limit you otherwise.
