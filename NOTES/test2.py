# def outer(func):
#     def inner(n):
#         print(n)
#         func(n)
#         print(n*n)
#     return inner

# @outer
# def sys(n):
#     print("-->")

# sys(5)
# import re
# def validate(s):
#     return re.fullmatch(r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$",s)
    
# def main():
#     flag=validate("chetanawari2002@gmail.com")
#     if flag:
#         print("Valid Email ID")
#     else:
#         print("Invalid")

# if __name__=="__main__":
#     main()

# d={1:2,2:3,3:4}

# new_d=sorted(d.items(),key=lambda x:x[0],reverse=True)
# print(dict(new_d))

name="Chetan"
name=name.lower()

ans={}

for ch in name:
    if ch in ans:
        ans[ch]+=1
    else:
        ans[ch]=1
        
print(dict(ans))