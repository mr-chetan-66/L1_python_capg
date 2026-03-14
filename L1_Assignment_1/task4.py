# ### Task 4 – `Write a function read_uppercase(file) that reads a file
# and returns a list of lines converted to uppercase.`
# - **File:** uppercase_source.txt

def read_uppercase(file):
    return [line.strip().upper() for line in file] #strip() remove /n

def main():
    with open("uppercase_source.txt","r") as f:
        lst=read_uppercase(f)
        for row in lst:
            print(row)
    return
            
if __name__=="__main__":
    main()