# File Handling in Python
### From Zero to Expert — A Complete Guide

---

## 🟢 LEVEL 1 — Beginner: The Basics

### What is a File?
A file is a named location on disk that stores data. Python lets you read from and write to files using built-in functions — no extra libraries needed to get started.

---

### Opening and Closing a File

```python
# Open a file
file = open("hello.txt", "r")   # "r" = read mode
content = file.read()
print(content)
file.close()                     # Always close after use!
```

**Common File Modes:**

| Mode | Meaning |
|------|---------|
| `"r"` | Read (default) — file must exist |
| `"w"` | Write — creates file or overwrites existing |
| `"a"` | Append — adds to end of file |
| `"x"` | Create — fails if file already exists |
| `"b"` | Binary mode (combine: `"rb"`, `"wb"`) |

---

### Reading a File

```python
file = open("notes.txt", "r")

# Read entire content as one string
content = file.read()

# Read one line at a time
line = file.readline()

# Read all lines into a list
lines = file.readlines()

file.close()
```

---

### Writing to a File

```python
file = open("output.txt", "w")
file.write("Hello, Python!\n")
file.write("This is file handling.\n")
file.close()
```

> ⚠️ `"w"` mode **overwrites** the file if it already exists. Use `"a"` to append instead.

---

## 🟡 LEVEL 2 — Intermediate: Best Practices

### The `with` Statement (Recommended Way)

The `with` statement automatically closes the file — even if an error occurs. Always prefer this over manual `open/close`.

```python
with open("notes.txt", "r") as file:
    content = file.read()
    print(content)
# File is automatically closed here
```

---

### Iterating Over Lines

```python
with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())   # .strip() removes trailing newline
```

This is **memory-efficient** — it reads one line at a time instead of loading the whole file.

---

### Appending to a File

```python
with open("log.txt", "a") as file:
    file.write("New log entry\n")
```

---

### Writing Multiple Lines at Once

```python
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]

with open("output.txt", "w") as file:
    file.writelines(lines)
```

---

### Checking if a File Exists

```python
import os

if os.path.exists("data.txt"):
    print("File found!")
else:
    print("File not found.")
```

---

### Handling Exceptions

```python
try:
    with open("missing.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("Error: File does not exist.")
except PermissionError:
    print("Error: You don't have permission to read this file.")
```

---

## 🔵 LEVEL 3 — Advanced: Working with Real Data

### Working with CSV Files

```python
import csv

# Writing CSV
data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]

with open("people.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Reading CSV
with open("people.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

---

### Working with JSON Files

```python
import json

# Writing JSON
person = {"name": "Alice", "age": 30, "skills": ["Python", "SQL"]}

with open("person.json", "w") as file:
    json.dump(person, file, indent=4)

# Reading JSON
with open("person.json", "r") as file:
    data = json.load(file)
    print(data["name"])   # Alice
```

---

### File Seek and Tell (Cursor Control)

```python
with open("data.txt", "r") as file:
    print(file.read(5))    # Read first 5 characters
    print(file.tell())     # Show current cursor position

    file.seek(0)           # Move cursor back to beginning
    print(file.read())     # Read entire file again
```

---

### Reading and Writing Binary Files

```python
# Copy an image file (binary)
with open("photo.jpg", "rb") as source:
    data = source.read()

with open("photo_copy.jpg", "wb") as dest:
    dest.write(data)
```

---

### Using `pathlib` (Modern Way)

```python
from pathlib import Path

path = Path("notes.txt")

# Write
path.write_text("Hello from pathlib!")

# Read
content = path.read_text()
print(content)

# Check existence
print(path.exists())

# File metadata
print(path.suffix)    # .txt
print(path.stem)      # notes
print(path.parent)    # current directory
```

---

## 🔴 LEVEL 4 — Expert: Performance & Production Patterns

### Reading Large Files Efficiently (Chunking)

Never load a 10GB log file into memory all at once. Use chunked reading:

```python
CHUNK_SIZE = 1024 * 1024  # 1 MB

with open("huge_file.log", "r") as file:
    while chunk := file.read(CHUNK_SIZE):
        process(chunk)   # Replace with your processing logic
```

---

### Context Manager — Custom File Handler

Build your own context manager for advanced file workflows:

```python
class ManagedFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return False  # Don't suppress exceptions

with ManagedFile("data.txt", "r") as f:
    print(f.read())
```

---

### `io.StringIO` and `io.BytesIO` — In-Memory Files

Treat strings or bytes as file-like objects without touching the disk:

```python
import io

# StringIO — useful for testing or processing text in memory
buffer = io.StringIO()
buffer.write("Hello\nWorld\n")
buffer.seek(0)
print(buffer.read())

# BytesIO — for binary data in memory
image_buffer = io.BytesIO(b"\x89PNG\r\n...")
data = image_buffer.read()
```

---

### Atomic File Writes (Safe Production Pattern)

Avoid partial/corrupt writes on crashes by writing to a temp file first:

```python
import os
import tempfile

def atomic_write(filepath, content):
    dir_name = os.path.dirname(filepath) or "."
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    os.replace(tmp_path, filepath)  # Atomic on most OS
```

---

### File Locking (Concurrent Access)

Prevent race conditions when multiple processes access the same file:

```python
import fcntl  # Unix/Linux only

with open("shared.txt", "w") as file:
    fcntl.flock(file, fcntl.LOCK_EX)   # Exclusive lock
    file.write("Safe concurrent write\n")
    fcntl.flock(file, fcntl.LOCK_UN)   # Release lock
```

For cross-platform locking, use the `filelock` library:

```python
from filelock import FileLock

lock = FileLock("shared.txt.lock")

with lock:
    with open("shared.txt", "a") as file:
        file.write("Thread-safe write\n")
```

---

### Memory-Mapped Files (`mmap`)

Map a file directly into memory for ultra-fast random access — ideal for large binary files or databases:

```python
import mmap

with open("large_data.bin", "r+b") as file:
    mm = mmap.mmap(file.fileno(), 0)

    # Read bytes from a specific position
    mm.seek(1024)
    data = mm.read(256)

    # Write directly to mapped memory
    mm.seek(0)
    mm.write(b"HEADER")

    mm.close()
```

---

### Async File I/O with `aiofiles`

For async applications (FastAPI, async bots), avoid blocking the event loop:

```python
import asyncio
import aiofiles

async def read_file():
    async with aiofiles.open("data.txt", "r") as file:
        content = await file.read()
        print(content)

asyncio.run(read_file())
```

---

## 📊 Quick Reference Summary

| Task | Tool |
|------|------|
| Basic read/write | `open()` + `with` |
| Check file exists | `os.path.exists()` / `Path.exists()` |
| Modern path handling | `pathlib.Path` |
| CSV data | `csv` module |
| JSON data | `json` module |
| Large files | Chunked reading |
| In-memory files | `io.StringIO` / `io.BytesIO` |
| Safe writes | Atomic write with `tempfile` |
| Concurrent access | `filelock` / `fcntl` |
| High-performance access | `mmap` |
| Async I/O | `aiofiles` |

---

> 💡 **Golden Rule:** Always use `with open(...)` — it guarantees your file is closed properly, handles exceptions gracefully, and is the Pythonic standard.
