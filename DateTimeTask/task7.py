def main():
    d1={"a":1,"b":2}
    d2={"b":20,"c":3}
    # merged=d2|d1
    # print(merged)
    d3=d1
    
    for k in d2.keys():
        if k not in d3.keys():
            d3[k]=d2[k]
            
    print(d3)
    

if __name__=="__main__":
    main()