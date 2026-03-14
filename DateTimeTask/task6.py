from datetime import datetime,date,timedelta

def main():
    phonebook = {"Alice": "555-0100", "Bob": "555-0101"}
    name=input("Enter name: ")
    
    if name in phonebook.keys():
        print(phonebook[name])
    else:
        print("Not found")

if __name__=="__main__":
    main()