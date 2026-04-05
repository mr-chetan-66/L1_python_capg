
import calendar
from collections import Counter, deque, namedtuple
from datetime import date,datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta
import re



def q1():
    print("\n".join("FizzBuzz" if i%15==0 else "Buzz"if i%5==0 else "Fizz" if i%3==0 else str(i) for i in range(1,101)))
    
def q2():
    num=int(input("Enter number to check prime or not: "))
    if num<2: 
        print("Not a Prime Number")
        return 
    for i in range(2,int(num**0.5)+1):
        if num%i==0:
            print("Not a Prime Number")
            return 
    print(num,"is prime number")
    
def q3():
    num=int(input("Enter the number: "))
    print("\t".join(str(num*i) for i in range(1,11)))

def q4():
    num=int(input("Enter the number: ")) 
    i,j=0,1
    if num<0:
        print("Invalid Number")
    elif(num==1):
        print(i)
        
    fib=[0,1]    
    for i in range(2,num):
        fib.append(fib[i-1]+fib[i-2])
        
    print(*fib[:num])
    
def q5():
    num=abs(int(input("Enter the number: ")))
    sum=0
    while(num>0):
        sum+=(num%10)
        num//=10
        
    print(sum)
    
def q6():
    num=int(input("Enter the number: "))
    flag=False
    if num<0:
        flag=True
        num=abs(num)
    sum=0
    while(num>0):
        sum=(sum*10)+(num%10)
        num//=10
        
    if flag:
        print(0-sum)
    else:
        print(sum)

def q7():
    num=int(input("Enter the number: "))
    # 
    for i in range(num):
        print(f"{" "*(num-i)}{"*"*((i*2)+1)}")

def q8():
    s=input("Enter String: ")
    v,cn=0,0
    for c in s:
        c=str(c)
        if c.isalpha():
            if "aeiouAEIOU".find(c)!=-1:
                v+=1
            else:
                cn+=1
    print(v,cn)

def q9():
    a,b=map(int,input("Enter two number: ").split())
    while(b!=0):
        a,b=b,a%b
        
    print(a)
    
def q10():
    num=int(input("Enter the number: "))
    n=num
    sum=0
    while(n>0):
        sum+=((n%10)**3)
        n//=10
    
    if sum==num:
        print("Armstrong number")
    else:
        print("Not a Armstrong number")
    
def q11():
    num=int(input("Enter the number: "))    
    li=[False]*num # false means prime and true means non-prime

    for i in range(2,num+1):
        for j in range(2,int(i**0.5)+1):
            if i%j==0:
                li[i-1]=True
                break
        
    print(" ".join(str(i+1) for i,flag in enumerate(li) if not flag))
    
def q12():
    ans=[]
    for i in range(1,51):
        if i>20:
            break
        if i%3!=0:
            ans.append(i)
            
    print(ans)

def q13():
    num=int(input("Enter the number: "))
    for i in range(1,num+1):
        print(" ".join(str(j) for j in range(1,i+1)))
        
def q14():
    num=int(input("Enter the number: "))
    ans=[]
    while(num!=1):
        if num%2==0:
            num/=2
        else:
            num=(3*num)+1
        ans.append(int(num))
        
    print(str(ans))
    
def q15():
    s=input("Enter string: ")
    print(s[::-1])
    
def q16():
    s=input("Enter string: ")
    if s==s[::-1]:
        print("Pallindrome")
    else:
        print('Not a Pallindrome String')

def q17():
    s=input("Enter string: ")
    print(dict(Counter(s.split())))
    
def q18():
    s=input("Enter string: ").split()
    print(max(s,key=len))
    
def q19():
    str1,str2=input("Enter two string: ").lower().split()
    if sorted(str1)==sorted(str2):
        print("Anagram")
    else:
        print('Not a anagram')
        
def q20():
    s=input("Enter string: ")
    ans=''
    for c in s:
        if not ans.__contains__(c):
            ans=ans+str(c)
            
    print(ans)
    
def q21():
    s_list=input("Enter string: ").split()
    ans=[]
    for s in s_list:
        ans.append(f"{s[:1].upper()}{s[1:]}")
    
    ans=" ".join(ans)    
    print(ans)
    
def q22():
    s,sub=input("Enter string: ").split()
    print(s.count(sub)) #non overlapping that is aaaa - aa ==2 
    #for overlapping aaaa- aa== 3
    count=0
    for i in range(len(s)):
        if s.startswith(sub,i):
            count+=1
    
    print(count)
    
def q23():
    s=set(input("Enter string: ").lower())
    if len(s)==26:
        print("Pangram")
    else:
        print("Not a Pangram")
        
def q24():
    s=list(input("Enter string: "))
    count=1
    ans=''
    for i in range(1,len(s)):
        if s[i]==s[i-1]:
            count+=1
        else:
            ans+=s[i-1]+ (str(count) if count>1 else "")
            count=1
    ans+=s[-1]+ (str(count) if count>1 else "")
    print(ans)

def q25():
    s=input("Enter string: ")
    ans=''
    for c in s:
        if c.islower():
            ascii=(ord(c)-ord('a'))+3
            if (ascii+3)>ord('z'):
                ascii%=26
            ans+=(chr(ord('a')+ascii))
        elif c.isupper():
            ascii=(ord(c)-ord('A'))+3
            if ascii>ord('Z'):
                ascii%=26
            ans+=(chr(ord('A')+ascii))
        else:
            ans+=str(c)
            
    print(ans)
    
def q26():
    s=input("Enter string: ")
    print(" ".join(re.findall(r"\d+",s)))
    
def q27():
    s=input("Enter string: ")
    b=[]
    for c in s:
        if c in "{[(":
            b.append(c)
        elif c in ")]}":
            if not b:
                print(False)
                return 

            if c=='}' and b[-1]=='{':
                b.pop()
            elif c==']' and b[-1]=='[':
                b.pop()
            elif c==')' and b[-1]=='(':
                b.pop()
            else:
                print(False)
                return 
            
    print("True" if len(b)==0 else "False")        
    
def q28():
    s=input("Enter string: ")
    r=int(input("Enter rotate number: "))
    s2=s+s
    print(s2[r:(r+len(s))])

def q29():
    s=input("Enter string: ")
    ans=[]
    used=[False]*len(s)
    
    def backstrack(cur):
        if len(cur)==len(s):
            ans.append("".join(cur))
            return
        
        for i in range(len(s)):
            if not used[i]:
                cur.append(s[i])
                used[i]=True
                backstrack(cur)
                cur.pop()
                used[i]=False
                
    backstrack([])
    print(ans)

def q30():
    print(date.today().strftime("%d-%B-%Y"))
    
def q31():
    d1=datetime.strptime(input("Enter first date :"),"%Y-%m-%d")
    d2=datetime.strptime(input("Enter second date :"),"%Y-%m-%d")
    print((d2-d1).days)
    
def q32():
    d=datetime.strptime(input("Enter first date :"),"%Y-%m-%d")
    print(d.strftime("%A")) #d.weekday() m=0 and d.isoweekday() m=1
    
def q33():
    d=datetime.strptime(input("Enter first date :"),"%Y-%m-%d")
    d_add=int(input("Dates to be added: "))
    
    print((d+timedelta(days=d_add)).strftime("%d-%B-%Y"))

def q34():
    d=int(input("Enter year :"))
    print(calendar.isleap(d))
    print(calendar.month(2026,4))

def q35():
    print(f"First date: {date.today().replace(day=1):%d-%m-%Y}")
    info=calendar.monthrange(2026,4)
    print(f"Last date: {date.today().replace(day=info[1]):%d-%m-%Y}")
    
def q36():
    sec=int(input("Enter the seconds: "))
    print(date.fromtimestamp(sec).strftime("%d-%m-%Y"))
    
def q37():
    d=parser.parse(input("Enter first date :"))
    dob=relativedelta(date.today(),d)
    print(f"{dob.years}Y-{dob.months}M-{dob.days}D")
    
def q38():
    l=[1,1,1,2,3,4,3,2,1,2]
    print(" ".join(str(x) for x in set(l)))

def q39():
    l=[1,[2,[3,4]],5,9]
    ans=[]
    def helper(arr):
        for x in arr:
            if isinstance(x,list):
                helper(x)
            else:
                ans.append(x)
                
    helper(l)
    print(" ".join(str(x) for x in ans))

def q40():
    l=[i*i for i in range(1,11) if i%2==0]
    print(" ".join(str(x) for x in l))
    
def q41():
    l=[3,1,4,1,5,9,2]
    s=sorted(set(l),reverse=True)
    print(s[1])
    
def q42():
    l=[3,1,4,1,5,9,2]
    r=int(input("Enter rotate: "))
    l=l[r:]+l[:r]
    print(l)
    
def q43():
    l1=[1,3,5]
    l2=[2,4,6]
    print(sorted(l1+l2))
    
def q44():
    a,b=10,20
    a,b=b,a
    print(a,b)
    
def q45():
    student=namedtuple('student',['name','age','grade'])
    print(student('Chetan',22,'A'))
    
def q46():
    l1=['a','b','c']
    l2=[1,2,3]
    
    print(dict(zip(l1,l2)))
    
def q47():
    s1={1,2,3}
    s2={2,3,4}
    d={}
    d['Union']=s1.union(s2)
    d['Intersection']=s1.intersection(s2)
    d['Difference']=s1-s2
    d['Symmentric Difference']=s1^s2
    print(d)
    
def q48():
    l1=set([1,2,3,4])
    l2=set([3,4,5,6])
    print(l1&l2)
    
def q49():
    s=input("Enter string: ").split()
    print(dict(Counter(s)))
    
def q50():
    l=[1,'a',2,'b',3.0]
    d={}
    for x in l:
        key=type(x).__name__
        if key in d:
            d[key].append(x)
        else:
            d[key]=[x]
    print(d)

def q51():
    d={'a':1,'b':2,'c':3}
    ans={}
    for k,v in d.items():
        ans[v]=k
    print(ans)
    
def q52():
    d1={'a':1}
    d2={'b':2,'a':10}
    print(d1|d2)
    
def q53():
    d={'b':3,'a':1,'c':2}
    d=sorted(d.items(),key=lambda x:x[1])
    print(d)
    
def q54():
    l=[]
    l.extend([10,20,30])
    t=l.pop(),l
    print(t)
    
def q55():
    q=deque()
    q.append('A')
    q.append('B')
    q.append('C')
    print((q.popleft(),list(q)))
    
def q56():
    q=[1,3,-1,-3,5,3,6,7]
    ans=[]
    for i in range(0,len(q)-2):
        ans.append(max(q[i:(i+3)]))
        
    print(ans)

def q57():
    l1=[1,2,3]
    l2=[4,5,6]
    ans=[[x,y] for x,y in zip(l1,l2)]
    
    print(ans)
    
def q58():
    pass
    
def main():
    # q1()
    # q2()
    # q3()
    # q4()
    # q5()
    # q6()
    # q7()
    # q8()
    # q9()
    # q10()
    # q11()
    # q12()
    # q13()
    # q14()
    # q15()
    # q16()
    # q17()
    # q18()
    # q19()
    # q20()
    # q21()
    # q22()
    # q23()
    # q24()
    # q25()
    # q26()
    # q27()
    # q28()
    # q29()
    # q30()
    # q31()
    # q32()
    # q33()
    # q34()
    # q35()
    # q36()
    # q37()
    # q38()
    # q39()
    # q40()
    # q41()
    # q42()
    # q43()
    # q44()
    # q45()
    # q46()
    # q47()
    # q48()
    # q49()
    # q50()
    # q51()
    # q52()
    # q53()
    # q54()
    # q55()
    # q56()
    q57()
    
    
if __name__=="__main__":
    main()