# =============================================================================
#  100 PYTHON INTERVIEW QUESTIONS — SOLUTIONS
#  Topics: Control Flow | Strings | Dates | Collections | Classes |
#          File Handling | Exception Handling | Database Connectivity
# =============================================================================

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 1: CONTROL FLOW STATEMENTS (Q1–Q14)
# ──────────────────────────────────────────────────────────────────────────────

# Q1 – FizzBuzz
def q1_fizzbuzz(n):
    """Print FizzBuzz for numbers 1 to n."""
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

# Q2 – Check if a number is prime
def q2_is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Q3 – Print multiplication table
def q3_multiplication_table(n):
    table = []
    for i in range(1, 11):
        table.append(f"{n} x {i} = {n * i}")
    return table

# Q4 – Fibonacci using while loop
def q4_fibonacci(n):
    a, b = 0, 1
    result = []
    while len(result) < n:
        result.append(a)
        a, b = b, a + b
    return result

# Q5 – Sum of digits
def q5_sum_of_digits(n):
    return sum(int(d) for d in str(abs(n)))

# Q6 – Reverse a number using loops
def q6_reverse_number(n):
    reversed_n = 0
    negative = n < 0
    n = abs(n)
    while n > 0:
        reversed_n = reversed_n * 10 + n % 10
        n //= 10
    return -reversed_n if negative else reversed_n

# Q7 – Pattern: right-angle triangle of stars
def q7_star_pattern(rows):
    pattern = []
    for i in range(1, rows + 1):
        pattern.append("* " * i)
    return pattern

# Q8 – Count vowels and consonants using loop
def q8_count_vowels_consonants(s):
    vowels = "aeiouAEIOU"
    v_count = sum(1 for c in s if c in vowels)
    c_count = sum(1 for c in s if c.isalpha() and c not in vowels)
    return v_count, c_count

# Q9 – GCD using loop
def q9_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Q10 – Check Armstrong number
def q10_is_armstrong(n):
    digits = str(n)
    power = len(digits)
    return n == sum(int(d) ** power for d in digits)

# Q11 – Find all prime numbers up to n (Sieve of Eratosthenes)
def q11_sieve(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]

# Q12 – break/continue: skip multiples of 3, stop at 20
def q12_break_continue():
    result = []
    for i in range(1, 50):
        if i > 20:
            break
        if i % 3 == 0:
            continue
        result.append(i)
    return result

# Q13 – Nested loop: print number pyramid
def q13_number_pyramid(rows):
    pattern = []
    for i in range(1, rows + 1):
        pattern.append(" ".join(str(j) for j in range(1, i + 1)))
    return pattern

# Q14 – Collatz conjecture steps
def q14_collatz(n):
    steps = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps.append(n)
    return steps


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2: STRINGS (Q15–Q29)
# ──────────────────────────────────────────────────────────────────────────────

# Q15 – Reverse a string
def q15_reverse_string(s):
    return s[::-1]

# Q16 – Check palindrome
def q16_is_palindrome(s):
    cleaned = s.replace(" ", "").lower()
    return cleaned == cleaned[::-1]

# Q17 – Count word frequency
def q17_word_frequency(sentence):
    freq = {}
    for word in sentence.lower().split():
        freq[word] = freq.get(word, 0) + 1
    return freq

# Q18 – Find longest word in a sentence
def q18_longest_word(sentence):
    words = sentence.split()
    return max(words, key=len)

# Q19 – Check anagram
def q19_is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

# Q20 – Remove duplicates from string (preserve order)
def q20_remove_duplicates(s):
    seen = set()
    result = []
    for c in s:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return "".join(result)

# Q21 – Title case without .title()
def q21_title_case(s):
    return " ".join(word.capitalize() for word in s.split())

# Q22 – Count occurrences of substring
def q22_count_substring(s, sub):
    return s.count(sub)

# Q23 – Check if string is pangram
def q23_is_pangram(s):
    return set("abcdefghijklmnopqrstuvwxyz").issubset(set(s.lower()))

# Q24 – Compress string (Run-length encoding)
def q24_compress_string(s):
    if not s:
        return ""
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            result.append(s[i-1] + (str(count) if count > 1 else ""))
            count = 1
    result.append(s[-1] + (str(count) if count > 1 else ""))
    return "".join(result)

# Q25 – Caesar cipher
def q25_caesar_cipher(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return "".join(result)

# Q26 – Extract numbers from string
def q26_extract_numbers(s):
    import re
    return list(map(int, re.findall(r'\d+', s)))

# Q27 – Check balanced brackets
def q27_balanced_brackets(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in '([{':
            stack.append(c)
        elif c in ')]}':
            if not stack or stack[-1] != pairs[c]:
                return False
            stack.pop()
    return len(stack) == 0

# Q28 – Rotate string by k positions
def q28_rotate_string(s, k):
    k = k % len(s) if s else 0
    return s[k:] + s[:k]

# Q29 – Find all permutations of a string
def q29_permutations(s):
    from itertools import permutations
    return sorted(set("".join(p) for p in permutations(s)))


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3: DATE FUNCTIONS (Q30–Q37)
# ──────────────────────────────────────────────────────────────────────────────

from datetime import datetime, date, timedelta
import calendar

# Q30 – Get today's date and format it
def q30_today_formatted():
    return datetime.now().strftime("%d-%B-%Y")

# Q31 – Days between two dates
def q31_days_between(date1_str, date2_str):
    d1 = datetime.strptime(date1_str, "%Y-%m-%d")
    d2 = datetime.strptime(date2_str, "%Y-%m-%d")
    return abs((d2 - d1).days)

# Q32 – Find day of the week for a given date
def q32_day_of_week(date_str):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%A")

# Q33 – Add N days to a date
def q33_add_days(date_str, n):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return (d + timedelta(days=n)).strftime("%Y-%m-%d")

# Q34 – Check if a year is a leap year
def q34_is_leap(year):
    return calendar.isleap(year)

# Q35 – Get first and last day of current month
def q35_first_last_day():
    today = date.today()
    first = today.replace(day=1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    last = today.replace(day=last_day)
    return first.isoformat(), last.isoformat()

# Q36 – Convert Unix timestamp to readable date
def q36_unix_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

# Q37 – Find age from date of birth
def q37_calculate_age(dob_str):
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 4: COLLECTION FRAMEWORK (Q38–Q57)
# ──────────────────────────────────────────────────────────────────────────────

# Q38 – Remove duplicates from list preserving order
def q38_remove_list_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# Q39 – Flatten a nested list
def q39_flatten(nested):
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(q39_flatten(item))
        else:
            flat.append(item)
    return flat

# Q40 – List comprehension: squares of even numbers
def q40_even_squares(n):
    return [x**2 for x in range(1, n+1) if x % 2 == 0]

# Q41 – Second largest element in list
def q41_second_largest(lst):
    unique = list(set(lst))
    if len(unique) < 2:
        return None
    unique.sort()
    return unique[-2]

# Q42 – Rotate list by k positions
def q42_rotate_list(lst, k):
    if not lst:
        return lst
    k = k % len(lst)
    return lst[k:] + lst[:k]

# Q43 – Merge two sorted lists
def q43_merge_sorted(l1, l2):
    result = []
    i = j = 0
    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            result.append(l1[i]); i += 1
        else:
            result.append(l2[j]); j += 1
    result.extend(l1[i:])
    result.extend(l2[j:])
    return result

# Q44 – Tuple: swap without temp variable
def q44_swap(a, b):
    a, b = b, a
    return a, b

# Q45 – Named tuple for student record
def q45_named_tuple_demo():
    from collections import namedtuple
    Student = namedtuple("Student", ["name", "age", "grade"])
    s = Student("Chetan", 22, "A")
    return s

# Q46 – Zip two lists into a dictionary
def q46_zip_to_dict(keys, values):
    return dict(zip(keys, values))

# Q47 – Set operations: union, intersection, difference
def q47_set_operations(s1, s2):
    return {
        "union": s1 | s2,
        "intersection": s1 & s2,
        "difference": s1 - s2,
        "symmetric_difference": s1 ^ s2
    }

# Q48 – Find common elements in two lists
def q48_common_elements(l1, l2):
    return list(set(l1) & set(l2))

# Q49 – Word count using Counter
def q49_word_count(text):
    from collections import Counter
    return Counter(text.lower().split())

# Q50 – Group list elements by type
def q50_group_by_type(lst):
    from collections import defaultdict
    groups = defaultdict(list)
    for item in lst:
        groups[type(item).__name__].append(item)
    return dict(groups)

# Q51 – Dictionary: invert keys and values
def q51_invert_dict(d):
    return {v: k for k, v in d.items()}

# Q52 – Merge two dictionaries (Python 3.9+)
def q52_merge_dicts(d1, d2):
    return {**d1, **d2}

# Q53 – Sort dictionary by value
def q53_sort_by_value(d, reverse=False):
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=reverse))

# Q54 – Stack using list
def q54_stack_demo():
    stack = []
    stack.append(10)
    stack.append(20)
    stack.append(30)
    top = stack.pop()
    return top, stack

# Q55 – Queue using deque
def q55_queue_demo():
    from collections import deque
    queue = deque()
    queue.append("A")
    queue.append("B")
    queue.append("C")
    front = queue.popleft()
    return front, list(queue)

# Q56 – Sliding window maximum (size k)
def q56_sliding_window_max(nums, k):
    from collections import deque
    dq = deque()
    result = []
    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

# Q57 – Matrix transpose using list comprehension
def q57_transpose(matrix):
    return [list(row) for row in zip(*matrix)]


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 5: CLASSES AND OBJECTS (Q58–Q70)
# ──────────────────────────────────────────────────────────────────────────────

# Q58 – Basic class: BankAccount
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # private

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

    def get_balance(self):
        return self.__balance

    def __str__(self):
        return f"Account({self.owner}, Balance: {self.__balance})"

# Q59 – Class method and static method
class Circle:
    PI = 3.14159

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return Circle.PI * self.radius ** 2

    @classmethod
    def from_diameter(cls, diameter):
        return cls(diameter / 2)

    @staticmethod
    def is_valid_radius(r):
        return r > 0

# Q60 – Inheritance: Animal -> Dog
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def __str__(self):
        return f"Animal({self.name})"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says: Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says: Meow!"

# Q61 – Multiple inheritance + MRO demo
class A:
    def greet(self): return "Hello from A"

class B(A):
    def greet(self): return "Hello from B"

class C(A):
    def greet(self): return "Hello from C"

class D(B, C):
    pass
# D().greet() -> "Hello from B" (MRO: D -> B -> C -> A)

# Q62 – Dunder methods: __add__, __len__, __repr__
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __len__(self):
        return int((self.x**2 + self.y**2) ** 0.5)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Q63 – Property decorator (getter/setter)
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

# Q64 – Abstract base class
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): pass

    @abstractmethod
    def perimeter(self): pass

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)

# Q65 – Singleton pattern
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Q66 – Iterator class
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

# Q67 – Context manager using __enter__ / __exit__
class ManagedFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return False  # don't suppress exceptions

# Q68 – Dataclass
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    age: int
    grades: list = field(default_factory=list)

    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0

# Q69 – Method overloading simulation using *args
class Calculator:
    def add(self, *args):
        return sum(args)

# Q70 – Class with __slots__ for memory efficiency
class Point:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6: FILE HANDLING (Q71–Q80)
# ──────────────────────────────────────────────────────────────────────────────

import os
import json
import csv

# Q71 – Write and read a text file
def q71_write_read_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
    with open(filename, 'r') as f:
        return f.read()

# Q72 – Append to a file
def q72_append_to_file(filename, line):
    with open(filename, 'a') as f:
        f.write(line + '\n')

# Q73 – Count lines, words, characters in a file
def q73_file_stats(filename):
    with open(filename, 'r') as f:
        content = f.read()
    lines = content.splitlines()
    words = content.split()
    return len(lines), len(words), len(content)

# Q74 – Read file line by line and number each line
def q74_number_lines(filename):
    with open(filename, 'r') as f:
        return [f"{i+1}: {line.rstrip()}" for i, line in enumerate(f)]

# Q75 – Write and read CSV file
def q75_csv_write_read(filename, data, headers):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    with open(filename, 'r') as f:
        return list(csv.DictReader(f))

# Q76 – Write and read JSON file
def q76_json_write_read(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    with open(filename, 'r') as f:
        return json.load(f)

# Q77 – Copy file content
def q77_copy_file(src, dest):
    with open(src, 'r') as f:
        content = f.read()
    with open(dest, 'w') as f:
        f.write(content)

# Q78 – Search for a keyword in file
def q78_search_in_file(filename, keyword):
    matches = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f, 1):
            if keyword.lower() in line.lower():
                matches.append((i, line.rstrip()))
    return matches

# Q79 – List all files in a directory with extension filter
def q79_list_files(directory, ext=None):
    files = os.listdir(directory)
    if ext:
        files = [f for f in files if f.endswith(ext)]
    return sorted(files)

# Q80 – Binary file read/write
def q80_binary_file(filename, data_bytes):
    with open(filename, 'wb') as f:
        f.write(data_bytes)
    with open(filename, 'rb') as f:
        return f.read()


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 7: EXCEPTION HANDLING (Q81–Q90)
# ──────────────────────────────────────────────────────────────────────────────

# Q81 – Basic try/except/else/finally
def q81_safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid types"
    else:
        return result
    finally:
        pass  # Always runs (cleanup goes here)

# Q82 – Custom exception class
class InsufficientFundsError(Exception):
    def __init__(self, amount, balance):
        self.amount = amount
        self.balance = balance
        super().__init__(f"Cannot withdraw {amount}. Balance is {balance}.")

def q82_withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(amount, balance)
    return balance - amount

# Q83 – Catch multiple exceptions
def q83_risky_op(lst, idx):
    try:
        return int(lst[idx]) * 2
    except IndexError:
        return "Error: Index out of range"
    except ValueError:
        return "Error: Cannot convert to int"

# Q84 – Re-raise exception after logging
def q84_reraise(value):
    try:
        result = 100 / value
    except ZeroDivisionError as e:
        print(f"[LOG] ZeroDivisionError caught: {e}")
        raise
    return result

# Q85 – Exception chaining with 'raise from'
def q85_exception_chaining(filename):
    try:
        with open(filename) as f:
            data = f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Config load failed: {filename}") from e

# Q86 – Validate input with custom exceptions
class ValidationError(Exception):
    pass

def q86_validate_age(age):
    if not isinstance(age, int):
        raise ValidationError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValidationError(f"Age {age} is out of valid range (0-150)")
    return True

# Q87 – Using contextlib.suppress
def q87_suppress_demo(d, key):
    from contextlib import suppress
    with suppress(KeyError):
        return d[key]
    return None

# Q88 – Retry logic with exception handling
def q88_retry(func, retries=3, *args):
    for attempt in range(retries):
        try:
            return func(*args)
        except Exception as e:
            if attempt == retries - 1:
                raise
            print(f"Attempt {attempt+1} failed: {e}. Retrying...")

# Q89 – Exception in list comprehension via generator
def q89_safe_convert(lst):
    def try_int(x):
        try:
            return int(x)
        except (ValueError, TypeError):
            return None
    return [try_int(x) for x in lst]

# Q90 – Nested try-except
def q90_nested_exception(data):
    results = []
    for item in data:
        try:
            try:
                val = int(item)
                result = 100 // val
            except ZeroDivisionError:
                result = "inf"
        except ValueError:
            result = "invalid"
        results.append(result)
    return results


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 8: DATABASE CONNECTIVITY (Q91–Q100)
# ──────────────────────────────────────────────────────────────────────────────

import sqlite3

# Q91 – Create database and table
def q91_create_table():
    conn = sqlite3.connect(":memory:")  # in-memory for demo
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            grade TEXT
        )
    """)
    conn.commit()
    return conn

# Q92 – Insert single and multiple records
def q92_insert_records(conn):
    cursor = conn.cursor()
    # Single insert
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
                   ("Alice", 20, "A"))
    # Multiple inserts
    students = [("Bob", 21, "B"), ("Charlie", 22, "A+"), ("Diana", 19, "A")]
    cursor.executemany("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", students)
    conn.commit()

# Q93 – Fetch all records
def q93_fetch_all(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

# Q94 – Fetch with WHERE clause
def q94_fetch_filtered(conn, grade):
    cursor = conn.cursor()
    cursor.execute("SELECT name, age FROM students WHERE grade = ?", (grade,))
    return cursor.fetchall()

# Q95 – Update a record
def q95_update_record(conn, student_id, new_grade):
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET grade = ? WHERE id = ?", (new_grade, student_id))
    conn.commit()
    return cursor.rowcount  # number of rows affected

# Q96 – Delete a record
def q96_delete_record(conn, name):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE name = ?", (name,))
    conn.commit()
    return cursor.rowcount

# Q97 – Aggregate queries: COUNT, AVG, MAX, MIN
def q97_aggregates(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(age), MAX(age), MIN(age) FROM students")
    return cursor.fetchone()

# Q98 – Use Row factory for dict-like access
def q98_row_factory(conn):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

# Q99 – Transaction with rollback on error
def q99_transaction_demo(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Eve", 23, "B+"))
        # Simulate error
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Eve", None, None))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"Transaction rolled back: {e}"
    return "Transaction committed"

# Q100 – Full CRUD demo (Create, Read, Update, Delete)
def q100_full_crud():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Create
    cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?)",
                       [(1, "Laptop", 50000), (2, "Mouse", 500), (3, "Keyboard", 1500)])
    conn.commit()
    # Read
    cursor.execute("SELECT * FROM products ORDER BY price DESC")
    rows = cursor.fetchall()
    # Update
    cursor.execute("UPDATE products SET price = ? WHERE name = ?", (45000, "Laptop"))
    conn.commit()
    # Delete
    cursor.execute("DELETE FROM products WHERE price < ?", (600,))
    conn.commit()
    cursor.execute("SELECT * FROM products")
    final = cursor.fetchall()
    conn.close()
    return {"initial": rows, "final": final}


# ──────────────────────────────────────────────────────────────────────────────
# QUICK TEST RUNNER
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING SOLUTIONS")
    print("=" * 60)
    print(f"Q1  FizzBuzz(15):       {q1_fizzbuzz(15)}")
    print(f"Q2  is_prime(17):       {q2_is_prime(17)}")
    print(f"Q4  fibonacci(8):       {q4_fibonacci(8)}")
    print(f"Q10 armstrong(153):     {q10_is_armstrong(153)}")
    print(f"Q15 reverse('python'):  {q15_reverse_string('python')}")
    print(f"Q16 palindrome('racecar'): {q16_is_palindrome('racecar')}")
    print(f"Q19 anagram:            {q19_is_anagram('listen', 'silent')}")
    print(f"Q24 compress('aaabbc'): {q24_compress_string('aaabbc')}")
    print(f"Q25 caesar('abc',3):    {q25_caesar_cipher('abc', 3)}")
    print(f"Q30 today:              {q30_today_formatted()}")
    print(f"Q31 days_between:       {q31_days_between('2024-01-01','2025-01-01')}")
    print(f"Q40 even_squares(10):   {q40_even_squares(10)}")
    print(f"Q47 set_ops:            {q47_set_operations({1,2,3},{2,3,4})}")
    v1 = Vector(1, 2); v2 = Vector(3, 4)
    print(f"Q62 Vector add:         {v1 + v2}")
    conn = q91_create_table()
    q92_insert_records(conn)
    print(f"Q93 DB fetch all:       {q93_fetch_all(conn)}")
    print(f"Q100 CRUD demo:         {q100_full_crud()}")
    print("=" * 60)
    print("All solutions loaded successfully!")
