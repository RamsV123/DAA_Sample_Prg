import time

def rabin_karp(text, pattern, d=256, q=101):  # d = number of characters in input alphabet, q = a prime number
    
    n = len(text)
    m = len(pattern)
    h = pow(d, m-1) % q  # value of d^(m-1)
    p = 0  # hash value for pattern
    t = 0  # hash value for text
    result = []

    # Preprocessing: calculate hash value for pattern and first window of text
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Slide the pattern over text one by one
    for s in range(n - m + 1):
        if p == t:
            # Check for characters one by one (spurious hits are possible)
            if text[s:s+m] == pattern:
                result.append(s)
        
        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q
            if t < 0:
                t += q

    return result
text="hasdjhad ajhdsasdjhadha dsjfsjdfshdf " \
"ashdjahdhsd asjdhasdd ahsdajdjahda zxcxzczxczczc " \
"etwerwrwerwewr rwerw"
pattern ="as"
start_time = time.time()
matches = rabin_karp(text, pattern)
end_time = time.time()

print("Pattern found at positions:", matches)
print("Time taken: {:.6f} seconds".format(end_time - start_time))