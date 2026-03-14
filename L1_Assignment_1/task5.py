# ### Task 5 – `Write a function read_csv(file) that reads a CSV file and 
# returns a list of lists, where each inner list represents a row split by commas.`
# - **File:** sample.csv

import csv

def read_csv(file):
    return [line for line in file] #strip() remove /n

def main():
    with open("sample.csv","r") as f:
        reader=csv.reader(f)
        lst=read_csv(reader)
        for row in lst:
            print(row)
    return
            
if __name__=="__main__":
    main()