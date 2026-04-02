class MyList:
    def __init__(self, data):
        self.data = list(data)   # constructor

    def __str__(self):
        return f"MyList: {self.data}"   # human-readable

    def __repr__(self):
        return f"MyList({self.data})"   # debug readable

    def __len__(self):
        return len(self.data)           # len(obj)

    def __getitem__(self, key):
        return self.data[key]           # obj[key]

    def __setitem__(self, key, value):
        self.data[key] = value          # obj[key] = value

    def __contains__(self, item):
        return item in self.data        # x in obj

    def __eq__(self, other):
        return self.data == other.data  # obj1 == obj2

    def __lt__(self, other):
        return len(self) < len(other)   # obj1 < obj2

    def __add__(self, other):
        return MyList(self.data + other.data)  # obj1 + obj2

    # context manager methods
    def __enter__(self):
        print("Entering context...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context...")
        return False   # Do NOT suppress exceptions
    
    
a = MyList([1, 2, 3])
b = MyList([4, 5])

print(a)          # __str__
print(repr(a))    # __repr__

print(len(a))     # __len__

print(a[0])       # __getitem__
a[1] = 20         # __setitem__
print(a)

print(2 in a)     # __contains__
print(99 in a)

print(a == b)     # __eq__
print(a < b)      # __lt__

c = a + b         # __add__
print(c)

# Context manager
with MyList([10, 20]) as ml:
    print("Inside context:", ml)
    
    
# ✅ Output (What You Will See)
# MyList: [1, 2, 3]
# MyList([1, 2, 3])
# 3
# 1
# MyList: [1, 20, 3]
# True
# False
# False
# False
# MyList: [1, 20, 3, 4, 5]
# Entering context...
# Inside context: MyList: [10, 20]
# Exiting context...







