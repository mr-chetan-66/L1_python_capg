with open("data.txt","w") as f:
    f.write("Chetan")

with open("data.txt") as file:
    data=file.read()
    print(data)
    
