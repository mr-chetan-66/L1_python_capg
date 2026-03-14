# ### Task 6 – `Write a function word_count(file) that reads a file and 
# returns the total number of words in the file.`
# - **File:** words.txt

def word_count(file):
    return [line for line in file] #strip() remove /n

def main():
    with open("words.txt","r") as f:
        lst=word_count(f)
        count=sum(len(row.split()) for row in lst)
        print("Total word in file: "+str(count))   
    return
            
if __name__=="__main__":
    main()