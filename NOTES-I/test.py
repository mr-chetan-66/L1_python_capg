# class Addition:
#     def __init__(self,real,img):
#         self.__real=real
#         self.__img=img
    
#     def set_real(self,real):
#         self.__real=real

#     def set_img(self,img):
#         self.__img=img

#     def get_real(self):
#         return self.__real

#     def get_img(self):
#         return self.__img

#     def addRealPart(self,o1,o2):
#         return o1.get_real()+o2.get_real()

#     def addImaginaryPart(self,o1,o2):
#         return o1.get_img()+o2.get_img()
    
#     def __add__(self,o1):
#         img=self.get_img()+o1.get_img()
#         real=self.get_real()+o1.get_real()
#         return Addition(real,img)
    
#     def __str__(self):
#         return f"{self.__real} + {self.__img}i"


# def main():
#     print("Enter the real and imaginary parts of the first complex number:")
#     real1=int(input())
#     img1=int(input())
#     o1=Addition(real1,img1)

#     print("Enter the real and imaginary parts of the second complex number:")
#     real2=int(input())
#     img2=int(input())

#     o2=Addition(real2,img2)

#     print(f"Real part addition: {o1.addRealPart(o1,o2)}")
#     print(f"Imaginary part addition: {o1.addImaginaryPart(o1,o2)}")
#     total=o1+o2
#     print(total)

# if __name__=="__main__":
#     main()

# def lucky(num):
#     sum=0
#     while(num>0):
#         sum+=(num%10)
#         num//=10
    
#     if sum%2==0:
#         return 1
#     else:
#         return 0

# def main():
#     num=int(input("Enter the Number:"))
#     if num<0:
#         print("Invaldi Number")
#         return

#     if lucky(num)==1:
#         print(f"{num} is lucky ")
#     else:
#         print(f"{num} is not lucky")

# if __name__=="__main__":
#      main()

# def armnum(n):
#     num=n
#     sum=0
#     while(num>0):
#         d=num%10
#         sum+=(d**3)
#         num//=10
    
#     return n==sum

# def arm(s,e):
#     if e>999:
#         e=999
    
#     lst=[]
#     for i in range(s,e+1):
#         if armnum(i):
#             lst.append(i)
            
#     return lst


# def main():
#     print("Enter the starting and ending numbers:")
#     s,e=map(int,input().split())

#     if s<0 or e<0:
#         print("Starting and ending numbers must be greater than or equal to zero")
#         return 
    
#     if e<s:
#         print("Invalid input!! Ending number should be greater than starting number")
#         return
    
#     lst=arm(s,e)
#     print(f"Armstrong numbers between {s} and {e} are:")
#     if not lst:
#         print("There is no Armstrong number between these numbers")
#     else:
#         for x in lst:
#             print(x)
    
#     return

# if __name__=="__main__":
#      main()

# def funny(s):
#     revs=s[::-1]
#     for i in range(1,len(s)):
#         sub1=abs(ord(s[i])-ord(s[i-1]))
#         sub2=abs(ord(revs[i])-ord(revs[i-1]))
#         if sub1!=sub2:
#             return False
#     return True

# def main():
#     s=input("Enter the string:")
    
#     if len(s)<2 or len(s)>50:
#         print("Invalid String")
#         return 
    
#     if funny(s):
#         print("Funny")
#     else:
#         print("Not funny")

# if __name__=="__main__":
#      main()

# def main():
#     n=int(input("No of Residents: "))
    
#     if n<0:
#         print("Invalid")
#         return
    
#     r=[]
#     b=['A','B','C','D']
    
#     for i in range(n):
#         print(f"Resident {i+1}:")
#         name=input("Name : ")
#         age=int(input("Age : "))
        
#         if age<21 or age>58:
#             print("Invalid")
#             return
        
#         dnt=input("Designation : ")
#         band=input("Band : ").upper()
#         if band not in b:
#             print("Invalid")
#             return 
        
#         r.insert(i,(name,age,dnt,band))
        
#     header=('NAME', 'AGE', 'DESIGNATION', 'BAND')
#     print(header)
#     for x in r:
#         print(x)
    
#     bnd=input("Enter your band of interest : ").upper()

#     if bnd not in b:
#         print("Invalid")
#         return
    
#     lst=[x for x in r if x[3]==bnd]

#     print(header)
    
#     if not lst:
#         print("No resident under this band")
#     else:
#         for x in lst:
#             print(x)

# if __name__=="__main__":
#      main()

# import re

# def validate(id,zone):
#     if not (len(id)==6 and id[:3]=="ICC" and re.match(r"^\d{3}$",id[3:])):
#         return False
#     elif zone not in ("North", "South", "East", "West"):
#         return False

#     return True

# def display(lst):
#     print("PLAYER DETAILS:")
#     for i,x in enumerate(lst):
#         print(f"Player {i+1}:")
#         print(f"Player Id: {x["Id"]}")
#         print(f"Player Name: {x["Name"]}")
#         print(f"No. of Matches Played: {x["Matches_Played"]}")
#         print(f"Total Runs Scored: {x["Run_Scored"]}")
#         print(f"Playing Zone: {x["Playing_Zone"]}\n")

# def main():
#     player_details=[]
    
#     while True:
#         print("1. Create Player\n2. Display Player Details\n3. Exit")
    
#         print("Enter your choice")
#         choice=int(input())
    
#         if choice==1:
#             id=input("Enter the player Id\n")
#             name=input("Enter the player name\n")
#             matches=int(input("Enter the number of matches played\n"))
#             runs=int(input("Enter the total runs scored\n"))
#             zone=input("Enter the playing zone\n")
#             if not validate(id,zone):
#                 print("Invalid Data")
#                 break
#             else:
#                 player={"Id":id,
#                         "Name":name,
#                         "Matches_Played":matches,
#                         "Run_Scored":runs,
#                         "Playing_Zone":zone}
                
#                 player_details.append(player)
#                 print("Player details are created successfully")
            
#         elif choice==2:
#             if not player_details:
#                 print("No player details available")
#             else:
#                 display(player_details)
            
#         elif choice==3:
#             print("Thank you for using the SBCC application")
#             break
#         else:
#             print("Invalid choice")
#             break
        
# if __name__=="__main__":
#      main()


from dateutil import parser
dt1 = parser.parse('March 15, 2024').month
dt2 = parser.parse('15/03/2024').day
dt3 = parser.parse('2024-03-15T10:30:00').year
#dt4 = parser.parse('next Friday')

print(dt1)
print(dt2)
print(dt3)
#print(dt4)