# print("\n".join("SUPERBUZZ" if i%15==0 else 'MIDBUZZ'if i%3==0 else 'BUZZ'if i%5==0 else str(i) for i in range(1,101)))


# from fastapi.response import HTMLResponse
# fastpi == library
# response == package 
# HTMLResponse == module

from collections import Counter
# print(Counter("chetanshrihariawari"))
# print("\n")
# print(Counter(sorted("chetanshrihariawari")))
# print("\n")
# print(dict(Counter(sorted("chetanshrihariawari"))))
# print("\n")
print(sorted(dict(Counter("chetanshrihariawari")).items()))


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