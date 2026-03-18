import train_management as tm


s=input("Enter the source")
d=input("Enter the destination")
ct=input("Enter the coach type")

VALID_COACH=["ac1","ac2","ac3","sleeper","seater"]

if ct.lower() not in VALID_COACH:
    print("Invalid Coach Type")
    exit()

obj=tm.TrainManagementSystem()
train=obj.retrieve_train_details(ct.lower(),s,d)

if not train:
    print("No trains found")
else:
    obj.view_train_details(train)
