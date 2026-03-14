### Task 2 – `Write a function read_and_strip(file) that reads a file and 
# returns a list of lines with leading and trailing whitespace removed.`
# - **File:** whitespace.txt



def read_and_strip(file):
    return [line.strip() for line in file]

def main():
    with open("whitespace.txt","r") as f:
        lst=read_and_strip(f)
        for row in lst:
            print(row)
    return
            
if __name__=="__main__":
    main()