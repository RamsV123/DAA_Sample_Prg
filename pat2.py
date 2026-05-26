import time 
def function1(txt,pat,m,n):
    for i in range(m):
        if txt[i:n+i] == pat:
            return i
    return -1
f = open("input1.txt", "r")
f2 = open("pattern.txt", "r")
txt = f.read().strip()
pat = f2.read().strip()
stime =time.time()
time.sleep(1)
print(function1(txt,pat,len(txt),len(pat)))
etime =time.time()
print(len(txt))
print(len(pat))      
print(etime-stime+1)