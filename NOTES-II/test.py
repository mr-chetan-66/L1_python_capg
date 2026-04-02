# print("\n".join("SUPERBUZZ" if i%15==0 else 'MIDBUZZ'if i%3==0 else 'BUZZ'if i%5==0 else str(i) for i in range(1,101)))


# from fastapi.response import HTMLResponse
# fastpi == library
# response == package 
# HTMLResponse == module

# from collections import Counter
# print(Counter("chetanshrihariawari"))
# print("\n")
# print(Counter(sorted("chetanshrihariawari")))
# print("\n")
# print(dict(Counter(sorted("chetanshrihariawari"))))
# print("\n")
# print(sorted(dict(Counter("chetanshrihariawari")).items()))


# def is_rotate(s1,s2):
#     if (len(s1)!=len(s2)):
#         return False
#     return s2 in (s1+s1)

# print(is_rotate("Chetan".lower(),"TanChe".lower()))

# s="nayan"

# for c in s:
#     if s.count(c)==1:
#         print(c)
#         break

# from os import name
# import py_compile
# import sys

# # print(sys.argv)
# # print(sys.argv[0])
# # print(sys.argv[1])
# # ==> python test.py 10 20
# # ==> [test.py, 10, 20]
# # ==> test.py
# # ==> '10'
# # print(sys.version_info)

# class Entity:
#     def __init__(this,name:str,age:int):
#         this.__name=name
#         this.__age=age
        
#     def get_name(this):
#         return this.__name
#     def get_age(this):
#         return this.__age
#     def set_name(this,name):
#         this.__name=name
#     def set_age(this,age):
#         this.__name=age

# class Company(Entity):
#     pass
        

# ent=Entity("Chetan",22)
# ent2=Entity("Test",99)
# ent.address='hinganghat'
# print(ent.address)

# c=Company("test2", 24)
# c.address="Bangalore"
# print(c.address)

# print(ent.get_name())
# print(ent2.get_age())


# By default, Python stores instance attributes in a __dict__
# This is flexible but uses extra memory

# # __slots__ restricts attributes and saves memory
# class Point:
#     __slots__ = ['x', 'y','z']   # ONLY x and y allowed

#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# p = Point(1, 2)
# p.z = 3        # AttributeError! z not in __slots__
# #p.__dict__     # AttributeError! no __dict__ with __slots__

# # Benefits: ~40-50% less memory for large numbers of objects
# # Cost: cannot add new attributes dynamically

# print(p.x,p.y,p.z)

# class Countdown:
#     def __init__(self, start):
#         self.start = start
#         self.current = start

#     def __iter__(self):      # returns iterator object (self here)
#         self.current = self.start
#         return self

#     def __next__(self):      # returns next value
#         if self.current < 0:
#             raise StopIteration  # signals end of iteration
#         val = self.current
#         self.current -= 1
#         return val

# cd = Countdown(5)
# for n in cd:
#     print(n, end=' ')    # 5 4 3 2 1 0

# # Can also use next() manually
# cd2 = Countdown(3)
# it = iter(cd2)
# print(next(it))  # 3
# print(next(it))  # 2

# ---- or -----------
# def countdown(start):
#     current = start
#     while current >= 0:
#         yield current
#         current -= 1
        
# for n in countdown(5):
#     print(n, end=' ')   # 5 4 3 2 1 0



class Count:
    def __init__(self,end):
        self.current=1
        self.end=end
    
    def __iter__(self):
        self.current=1 #reset
        return self
    
    def __next__(self):
        if self.current>self.end:
            raise StopIteration()
        
        val=self.current
        self.current+=1
        return val
    
c=Count(10)

for ele in c:
    print(ele)
    
def counter(end):
    start=1
    
    while(start<=end):
        yield start
        start+=1
        
for ele in counter(10):
    print(ele)
    

    #     X
    #    / \
    #   A   B
    #  / \ / \
    # C   D   E
    #  \  |  /
    #     F
    #     |
    #     G
    
class X:
    def m(self): print("X")

class A(X):
    def m(self): print("A")

class B(X):
    def m(self): print("B")

class C(A):
    def m(self): print("C")

class D(A, B):
    def m(self): print("D")

class E(B):
    def m(self): print("E")

class F(C, D, E):
    def m(self): print("F")

class G(F):
    pass

# G, F, C, D, A, B, E, X
#  C3 MRO algorithm 