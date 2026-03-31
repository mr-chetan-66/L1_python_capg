# Regular Expressions in Python

Regular expressions (regex) are patterns used to match, search, and manipulate strings. Python provides the built-in `re` module for working with regex.

---

## Importing the Module

```python
import re
```

---

## Core Functions

| Function | Description |
|---|---|
| `re.match()` | Matches pattern at the **beginning** of a string |
| `re.search()` | Searches for the **first** occurrence anywhere in a string |
| `re.findall()` | Returns a **list** of all matches |
| `re.finditer()` | Returns an **iterator** of match objects |
| `re.sub()` | **Replaces** matches with a string |
| `re.split()` | **Splits** a string at each match |
| `re.compile()` | **Compiles** a pattern for reuse |

---

## Common Pattern Syntax

### Character Classes
| Pattern | Matches |
|---|---|
| `.` | Any character except newline |
| `\d` | Any digit `[0-9]` |
| `\D` | Any non-digit |
| `\w` | Any word character `[a-zA-Z0-9_]` |
| `\W` | Any non-word character |
| `\s` | Any whitespace `[ \t\n\r]` |
| `\S` | Any non-whitespace |
| `[abc]` | Any of `a`, `b`, or `c` |
| `[^abc]` | Anything except `a`, `b`, or `c` |
| `[a-z]` | Any lowercase letter |

### Anchors
| Pattern | Matches |
|---|---|
| `^` | Start of string (or line) |
| `$` | End of string (or line) |
| `\b` | Word boundary |
| `\B` | Non-word boundary |

### Quantifiers
| Pattern | Matches |
|---|---|
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 (optional) |
| `{n}` | Exactly n times |
| `{n,}` | n or more times |
| `{n,m}` | Between n and m times |
| `*?`, `+?` | Non-greedy (lazy) versions |

### Groups & Alternation
| Pattern | Matches |
|---|---|
| `(abc)` | Capturing group |
| `(?:abc)` | Non-capturing group |
| `a\|b` | Either `a` or `b` |
| `(?P<name>...)` | Named capturing group |

---

## Examples

### 1. `re.match()` — Match at the start
```python
result = re.match(r'\d+', '123abc')
print(result.group())  # '123'

result = re.match(r'\d+', 'abc123')
print(result)  # None — no match at start
```

### 2. `re.search()` — Search anywhere
```python
result = re.search(r'\d+', 'abc123xyz')
print(result.group())  # '123'
```

### 3. `re.findall()` — Find all matches
```python
matches = re.findall(r'\d+', 'I have 2 cats and 3 dogs')
print(matches)  # ['2', '3']
```

### 4. `re.sub()` — Replace matches
```python
result = re.sub(r'\s+', '-', 'hello world foo')
print(result)  # 'hello-world-foo'
```

### 5. `re.split()` — Split on pattern
```python
parts = re.split(r'[,;\s]+', 'one, two; three four')
print(parts)  # ['one', 'two', 'three', 'four']
```

### 6. Named Groups
```python
pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
match = re.search(pattern, 'Date: 2024-03-15')
print(match.group('year'))   # '2024'
print(match.group('month'))  # '03'
print(match.group('day'))    # '15'
```

### 7. Compiled Patterns (for reuse)
```python
email_pattern = re.compile(r'[\w.-]+@[\w.-]+\.\w+')
emails = email_pattern.findall('Contact alice@example.com or bob@mail.org')
print(emails)  # ['alice@example.com', 'bob@mail.org']
```

---

## Flags

Flags modify how the pattern is applied.

```python
re.search(r'hello', 'HELLO WORLD', re.IGNORECASE)   # Case-insensitive
re.findall(r'^\d+', text, re.MULTILINE)              # ^ matches each line start
re.match(r'.+', text, re.DOTALL)                     # . matches newlines too
re.search(r'\d +', '1 2 3', re.VERBOSE)              # Allow whitespace/comments in pattern
```

| Flag | Shorthand | Effect |
|---|---|---|
| `re.IGNORECASE` | `re.I` | Case-insensitive matching |
| `re.MULTILINE` | `re.M` | `^`/`$` match per line |
| `re.DOTALL` | `re.S` | `.` matches newlines |
| `re.VERBOSE` | `re.X` | Allows comments in pattern |

---

## Practical Patterns

```python
# Email validation
r'[\w.-]+@[\w.-]+\.\w{2,}'

# URL
r'https?://[\w./-]+'

# Phone number (US)
r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

# IPv4 address
r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

# Date (YYYY-MM-DD)
r'\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])'

# Hex color code
r'#(?:[0-9a-fA-F]{3}){1,2}\b'
```

---

## Tips

- Use **raw strings** (`r'...'`) to avoid issues with backslashes.
- Prefer `re.compile()` when using the same pattern multiple times.
- Use **non-greedy** quantifiers (`*?`, `+?`) when you want the shortest possible match.
- Always check if a match is `None` before calling `.group()` to avoid errors.

```python
match = re.search(r'\d+', text)
if match:
    print(match.group())
```
