## various type input taken from user

# # string
name=str(input("Enter your name: "))
print(name)
print(input("Enter your name: "))  #this is also allowed

# # integer
age=int(input("Enter your age: "))
print(age)

# #float
grade=float(input("Enter yout CGPA"))
print(grade)

# #multiple input
a, b=int(input("Enter mark of subject 1 and 2").split())
a=int(a)
b=int(b)

# # or
a, b=map(int,input().split())

# #mixed
c,d,e=input("Enter roll number, CGPA, corse").split()
c=int(c)
d=float(d)

# #character
section=input("Enter your section")[0]
print(section)

# #boolean
flag=input().lower()=="true"
print(flag)

# ## LIST INPUT -> mutable
# #Integer list
arr=list(map(int,input("Enter list numbers:").split()))
#or 
arr=[1,2,3,4,5]
print(arr)

# #string list
names=input().split()
print(names)

# #set->Duplicates automatically removed, unordered
s=set(map(int, input().split()))
#or 
s={1,2,3,4,5}
print(s)

# #tuple-> ordered, immutable
t=tuple(map(int,input().split()))
#or 
t=(91,2,3,4,5)

# # only two method for tuple
t.count(2)  #Counts how many times 2 appears in the tuple
t.index(3)  #Returns the index (position) of the first occurrence of 3

t = (10, 20, 30)
print(t[1])   # 20


# #dictionary/map -> ordered, mutable

d={}
n=int(input("Enter number of key-value"))

for _ in range(n):
    k, v=input().split()
    d[k]=v

print(d)

d = {"name": "Chetan", "age": 22}
print(d["name"])   # Chetan
d["age"] = 23      # Allowed

# # list=[]
# # tuple=()
# # set={}
# # dict={}

# ##LOOPING OVER- list,tuple,set,dict

# #list
for x in arr:
    print(x)

# #set
for x in s:
    print(x)

# #tuple
for x in t:
    print(x)

# # dict -keys
for key in d:
    print(d)

# # dict -value
for v in d.values:
    print(v)

# # dict -both
for k,v in d.items:
    print(k, v)

#python as a calculator
#REPL-> read evaluate print loop(cmd::python)
# """ -> multi-line cmt
# ''' -> multi-line string printed as it is 


#while loop with else
# else will only exe when while run noramlly 

a=[1,2,3,4,5,6]
target=8
i=0
for i in range(len(a)):
    if a[i]==target:
        print("Target Found")
        break

else:
    print("Taregt Not Found")


# #FUNCTION
def add(a, b):
    return a + b

result = add(10, 20)
print(result)

# # Function with default argument
def greet(name="User"):
    print("Hello", name)

greet()
greet("Chetan")

def introduce(name, age):
    print(f"My name is {name} and I am {age} years old.")

introduce(age=22, name="Chetan")


def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3, 4, 5))


def show_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

show_info(name="Chetan", age=21, city="Wardha")

#BaseException
#    └── Exception
#         ├── ArithmeticError
#         │    ├── ZeroDivisionError
#         │    ├── OverflowError
#         │    └── FloatingPointError
#         ├── LookupError
#         │    ├── IndexError
#         │    └── KeyError
#         ├── ValueError
#         │    └── UnicodeError
        #  ├── OSError
        #  │    ├── FileNotFoundError
        #  │    ├── PermissionError
        #  │    └── IsADirectoryError
        #  └── … (many more)

##LIST==?[]

name=['C','H','E','T','A','N']
for pos,ele in enumerate(name):
    print(pos+" "+ele)

#list comprehension
cElemenet=[e for e in name if e=='c']

# remove element in list
name.pop() #remove elem from last pos
del name[2] # remove elem from that pos
#both dont return anything so dont assign


#sorting in list 
name.sort(reverse=True) # sort original list and return none

name2=sorted(name,reverse=True) #it return list so no in place sorting 

num=[1,2,3,4,5,6]
add=sum(num)
m=max(num)
mi=min(num)

#reverse a list
num.reverse() # in place no return 
r=num[::-1] # new list 


# [[]] * 5
# [ same_list, same_list, same_list, same_list, same_list ]
# lst = [[]] * 5
# lst[0].append(10)

# print(lst)
# [[10], [10], [10], [10], [10]]

# lst = [[] for _ in range(5)]
# lst[0].append(10)
# print(lst)
# [[10], [], [], [], []]




##TUPLES and SET ==>() {}

# we can also create tuple withput using paranthesis like when we return multiple elem in side fuction its a tuppe which is immutable 

# almost all the method pply to list are applicable in tuples liek sum and max

#set in mutable but elem arent which means they are immutable # what this means is that once element is add in list then we can modify or chaneg that elem instaed that elem get replaced 

my_set={1,1,1,2,3,4,5,5} #set= 1,2,3,4,5

# we cant access set elem using index like list or tuple
# for that we need for loop


##DICT ==> {K:V}

#alos known as associate array
# after the py 3.7 insertion order is maintained

# Nested dictionary: School Database

school = {
    "S101": {
        "name": "Aarav",
        "age": 20,
        "course": "Computer Science",
        "marks": {
            "Math": 88,
            "Python": 92,
            "Data Structures": 85
        }
    },
    "S102": {
        "name": "Meera",
        "age": 21,
        "course": "Information Technology",
        "marks": {
            "Math": 78,
            "Python": 81,
            "Data Structures": 89
        }
    }
}

# Accessing Data
print("Student Name:", school["S101"]["name"])
print("Python Marks:", school["S101"]["marks"]["Python"])

# Calculating Average Marks
def calculate_average(student_id):
    marks = school[student_id]["marks"]
    average = sum(marks.values()) / len(marks)
    return average

print("Average Marks of S101:", calculate_average("S101"))

# Adding a new subject for a student
school["S101"]["marks"]["AI"] = 95

print("Updated Marks:", school["S101"]["marks"])

# len() , .keys(), value() 

#as previous there is no insertion order we cant access through index so it access by key 

# to chcek any key exist in doict we can use 'in' like 'chetan' in name return boolean

# del name['chetan] return nan 
# remove can through keyError to stop this we can use pop('chetan',none) this will remove or doesnt throw error

data = {
    "a": 1,
    "b": 2,
    "c": 3
}

reversed_dict = dict(reversed(data.items()))
print(reversed_dict)



## DOC STRING
# pyhton doc strings are used to documents functions. Doc strings should foloow immediately after defining function

#scope of variables
def square(a):
    ans=a*a
    return a

print(square(5)) # Error type because scope of variable is in functions

import sys

max_int = sys.maxsize
min_int = -sys.maxsize - 1

print(max_int)
print(min_int)

min_value = float('-inf')
max_value = float('inf')


max_float = float('inf')
min_float = float('-inf')


num1=1.9991
num2=1.9999
num1=round(num1,3) #1.999
num2=round(num2,3) #2.0

import numpy as np
arr=np.array([1,2],[3,4]) #2x2
#sort
print(np.sort(arr)) #flatten array with sort elem

print(np.sort(arr,axis=1)) #row wise sorting
 

#FILE HANDALING
with open("file_name.txt","w") as file:
    data=file.read() #write("")
    print(data)

#mode
# csv.DictReader() reads each row as a dictionary.
# Column names become the keys (Country, Player, Runs, etc.).
# newline=""
# Prevents extra blank lines (important for CSV files)
# Especially needed on Windows

# reader = csv.DictReader(file)
# 📂 1️⃣ "r" → READ MODE
# 🔹 Meaning

# Opens file for reading only

# File must exist

# Cannot write inside it

# 🔹 Example
# file = open("data.txt", "r")
# content = file.read()
# print(content)
# file.close()

# 🔹 If file does NOT exist

# ❌ Error: FileNotFoundError

# ✏️ 2️⃣ "w" → WRITE MODE
# 🔹 Meaning

# Opens file for writing

# Creates file if not exists

# ⚠️ Deletes old content if file already exists

# 🔹 Example
# file = open("data.txt", "w")
# file.write("Hello World")
# file.close()

# Result
# data.txt → Hello World


# If file had old data → it is erased.

# ➕ 3️⃣ "a" → APPEND MODE
# 🔹 Meaning

# Adds data at the end of file

# Does NOT delete old content

# Creates file if not exists

# 🔹 Example
# file = open("data.txt", "a")
# file.write("\nNew Line Added")
# file.close()

# Result

# Old data remains + new line added.

# 🔄 4️⃣ "r+" → READ + WRITE MODE
# 🔹 Meaning

# Can read and write both

# File must exist

# Writing starts from current cursor position

# 🔹 Example
# file = open("data.txt", "r+")
# print(file.read())   # read file
# file.write("\nExtra data")
# file.close()

# ⭐ Extra Important Modes (Very Useful)
# 5️⃣ "w+" → WRITE + READ

# Creates file if not exists

# Deletes old content

# Can read & write

# file = open("data.txt", "w+")
# file.write("Python")
# file.seek(0)
# print(file.read())
# file.close()

# 6️⃣ "a+" → APPEND + READ

# Can read and append

# Old data preserved

# file = open("data.txt", "a+")
# file.write("\nNew record")
# file.seek(0)
# print(file.read())
# file.close()

# seek() is used to move the file pointer (cursor) to a specific position inside a file.
# ✅ Move 10 bytes before the end of the file
# .seek(-10, 2)
# (Negative offset works only with binary mode 'rb' or 'wb'.)

# ITERATOR 
for i in [1, 2, 3]:
    print(i)

# How Iterator Works Internally

# Python uses two magic methods:

# __iter__() → returns iterator object

# __next__() → returns next value

# When values finish → it raises StopIteration

class CountUpTo:
    def __init__(self, max_value):
        # Store the maximum value
        self.max_value = max_value
        
        # Start counting from 1
        self.current = 1

    def __iter__(self):
        # This returns the iterator object itself
        self.current=1
        return self

    def __next__(self):
        # If current value is less than or equal to max_value
        if self.current <= self.max_value:
            
            # Store current value to return
            number = self.current
            
            # Increase current value for next call
            self.current += 1
            
            return number
        
        else:
            # No more values left
            raise StopIteration


# Using the iterator
counter = CountUpTo(5)

for num in counter:
    print(num)


# GENERATOR
# A generator is a simpler way to create iterators.

# Instead of writing __iter__() and __next__(),
# we use the keyword:

# yield


# yield pauses the function and remembers state.

def count_up_to(max_value):
    
    # Start counting from 1
    current = 1
    
    while current <= max_value:
        
        # yield returns value and pauses here
        yield current
        
        # This runs when next() is called again
        current += 1


# Using the generator
counter = count_up_to(5)

for num in counter:
    print(num)


# CLOSURE
# A closure happens when:

# A function is inside another function

# Inner function remembers outer function variables

# Even after outer function finishes

# Yes. It remembers. That’s the magic.

def outer_function(message):
    
    # This is outer variable
    
    def inner_function():
        # Inner function uses outer variable
        print(message)
    
    return inner_function


# outer_function finishes here
my_function = outer_function("Hello Charlie 👋")

# But inner function still remembers 'message'
my_function()


# DECODER

# A decorator is a function that:

# Takes another function

# Adds extra behavior

# Returns a new function

# Without changing original code.

def my_decorator(func):
    
    def wrapper():
        print("Something before function runs")
        
        func()
        
        print("Something after function runs")
    
    return wrapper


@my_decorator
def say_hello():
    print("Hello!")

# Calling function
say_hello()

# Something before function runs
# Hello!
# Something after function runs


def decorator(func):
    
    def wrapper(*args, **kwargs):
        
        print("Before function")
        
        result = func(*args, **kwargs)
        
        print("After function")
        
        return result
    
    return wrapper


@decorator
def add(a, b):
    return a + b


print(add(5, 3))

# Before function
# After function
# 8

# def add(a, b):
#     return a + b

# add = decorator(add)

import re

pattern = r"[a-z]+\d+"
text = "abc123"

match = re.fullmatch(pattern, text)

if match:
    print("Matched!")