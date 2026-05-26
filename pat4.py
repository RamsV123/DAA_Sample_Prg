import time
def KMPSearch(pat, txt):
    m = len(pat)
    n = len(txt)
    lps = [0] * m
    print(lps)
    j = 0
    computeLPSArray(pat, m, lps)
 
    i = 0
    while i < n:
        if pat[j] == txt[i]:
            i += 1
            j += 1
 
        if j == m:
            print("Found pattern at index " + str(i-j))
            j = lps[j-1]
 
        elif i < n and pat[j] != txt[i]:
            if j != 0:
               j = lps[j-1]
            else:
                i += 1

def computeLPSArray(pat, m, lps):
    len = 0
    lps[0] = 0
    i = 1
 
    while i < m:
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len-1]
            else:
                lps[i] = 0
                i += 1
    #For printing the frequency pattern table
    #print(list(pat))
    #print(lps)

txt = input("Enter text: ")
pat = input("Enter pattern: ")
stime =time.time()
time.sleep(1)
KMPSearch(pat, txt)
etime =time.time()
print(len(txt))
print(len(pat))      
print(etime-stime+1)