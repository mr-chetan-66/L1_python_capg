### Task 1 – `Write a function count_lines(file) that reads a file and returns the number of lines in it.`
# - **File:** lines.txt


def line_count(file):
    return sum(1 for _ in file)
    # 1 for _ in f is a generator expression (not a list comprehension).
    # It yields the number 1 for each line in the file—without creating a list in memory.

def main():
    with open("lines.txt","r") as f:
        num=line_count(f)
        if num==0:
            print("File is empty")
        else:
            print(f"Total line in file: {num}")
            
if __name__=="__main__":
    main()
    
# Count only non-empty lines
# sum(1 for line in f if line.strip())
# Count lines that start with # (e.g., comments):
# sum(1 for line in f if line.lstrip().startswith("#"))
