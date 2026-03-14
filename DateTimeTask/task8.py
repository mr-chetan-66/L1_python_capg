def firstWay(d):
    i={}
    for k,v in d.items():
        if v in i.keys():
            raise ValueError(f"Duplicate value detected: {v!r}")
        i[v]=k
    return i

def secondWay(d):
    if len(set(d.values())) != len(d):
        raise ValueError(f"Duplicate value detected")
    return {v:k for k,v in d.items()}

def main():
    d={"a": 1, "b": 2}
    print(firstWay(d))
    print(secondWay(d))

if __name__=="__main__":
    main()