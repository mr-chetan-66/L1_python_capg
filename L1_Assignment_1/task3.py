# ### Task 3 – `Write a function read_non_empty_lines(file) that reads
# a file and returns a list of only the non-empty lines.`
# - **File:** non_empty_lines.txt


def read_non_empty_lines(file):
    return [line for line in file if line.strip()] # alternate of end is line.rstrip("\n") 

def main():
    with open("non_empty_lines.txt","r") as f:
        lst=read_non_empty_lines(f)
        for row in lst:
            print(row,end="")
    return
            
if __name__=="__main__":
    main()