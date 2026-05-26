"""
Pattern Searching Algorithms — DAA Project
==========================================
Algorithms : Naive | Rabin-Karp | Knuth-Morris-Pratt (KMP)
Same sample text and same pattern are used for all three.

Time Complexity Summary
-----------------------
Algorithm    Best       Average    Worst      Preprocessing  Space
-----------  ---------  ---------  ---------  -------------  -----
Naive        O(n)       O(n*m)     O(n*m)     None           O(1)
Rabin-Karp   O(n+m)     O(n+m)     O(n*m)*    O(m)           O(1)
KMP          O(n)       O(n+m)     O(n+m)     O(m)           O(m)

* Rabin-Karp worst case is O(n*m) only when hash collisions (spurious hits) occur for
  every window — rare with a good prime modulus.
"""

import time

# ──────────────────────────────────────────────
# SAMPLE DATA  (same for all three algorithms)
# ──────────────────────────────────────────────
TEXT    = "AABAACAADAABAABA"
PATTERN = "AABA"

# ══════════════════════════════════════════════════════════
# 1. NAIVE / BRUTE-FORCE ALGORITHM
# ══════════════════════════════════════════════════════════
# Idea:
#   Slide the pattern over the text one position at a time.
#   At each position compare character by character.
#   If all m characters match, record the position.
#
# Time Complexity:
#   Best  : O(n)   — first char of pattern never matches (only 1 cmp per window)
#   Avg   : O(n*m)
#   Worst : O(n*m) — all chars same, e.g. text="AAAA..A", pattern="AAAB"
# Space   : O(1)   — no extra data structure
# ══════════════════════════════════════════════════════════

def naive_search(text: str, pattern: str) -> dict:
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0

    for i in range(n - m + 1):          # slide window
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)

    return {"algorithm": "Naive (Brute Force)",
            "matches": matches,
            "comparisons": comparisons}


# ══════════════════════════════════════════════════════════
# 2. RABIN-KARP ALGORITHM
# ══════════════════════════════════════════════════════════
# Idea:
#   Compute a hash of the pattern and of every window of length m.
#   A rolling (sliding) hash lets you compute the next window's hash
#   in O(1) instead of O(m).
#   Only when hashes match do we verify character by character.
#
# Rolling hash formula:
#   hash(s[i+1..i+m]) = (d * (hash(s[i..i+m-1]) - s[i]*h) + s[i+m]) % q
#   where d = alphabet size, q = prime, h = d^(m-1) % q
#
# Time Complexity:
#   Best  : O(n+m)   — no spurious hits
#   Avg   : O(n+m)
#   Worst : O(n*m)   — every window is a spurious hit (hash collision)
# Space   : O(1)
# ══════════════════════════════════════════════════════════

def rabin_karp_search(text: str, pattern: str,
                      d: int = 256, q: int = 101) -> dict:
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0
    spurious = 0

    h   = pow(d, m - 1, q)   # d^(m-1) mod q
    p_hash = 0                # pattern hash
    t_hash = 0                # current window hash

    # Initial hash for pattern and first window
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        if p_hash == t_hash:                 # possible match
            # Verify character by character
            match = True
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    match = False
                    spurious += 1
                    break
            if match:
                matches.append(i)
        else:
            comparisons += 1                 # hash comparison counts too

        # Roll the hash to the next window
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if t_hash < 0:
                t_hash += q

    return {"algorithm": "Rabin-Karp (Rolling Hash)",
            "matches": matches,
            "comparisons": comparisons,
            "spurious_hits": spurious,
            "d": d, "q": q}


# ══════════════════════════════════════════════════════════
# 3. KNUTH-MORRIS-PRATT (KMP) ALGORITHM
# ══════════════════════════════════════════════════════════
# Idea:
#   Pre-process the pattern to build an LPS (Longest Proper
#   Prefix which is also a Suffix) array.
#   On a mismatch, instead of restarting from scratch, use the
#   LPS value to skip already-matched characters.
#
# LPS array:
#   lps[i] = length of the longest proper prefix of pattern[0..i]
#             that is also a suffix of pattern[0..i]
#   e.g. pattern = "AABA"
#        lps     = [0, 1, 0, 1]
#
# Time Complexity:
#   Best       : O(n)     — no backtracking needed
#   Avg / Worst: O(n+m)   — guaranteed linear (no O(n*m) worst case)
# Space        : O(m)     — for the LPS array
# ══════════════════════════════════════════════════════════

def compute_lps(pattern: str) -> list:
    """Compute the Longest Proper Prefix-Suffix (LPS) array."""
    m   = len(pattern)
    lps = [0] * m
    length = 0   # length of previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i]  = length
            i += 1
        else:
            if length:
                length = lps[length - 1]   # fall back — don't increment i
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text: str, pattern: str) -> dict:
    n, m    = len(text), len(pattern)
    lps     = compute_lps(pattern)
    matches, comparisons = [], 0

    i = j = 0          # i → text index, j → pattern index
    while i < n:
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]             # continue search
        else:
            if j:
                j = lps[j - 1]             # use LPS to skip
            else:
                i += 1

    return {"algorithm": "Knuth-Morris-Pratt (KMP)",
            "matches": matches,
            "comparisons": comparisons,
            "lps_array": lps}


# ──────────────────────────────────────────────
# RUNNER & PRETTY PRINTER
# ──────────────────────────────────────────────

def highlight_matches(text: str, matches: list, pat_len: int) -> str:
    """Return the text with [MATCH] markers around found positions."""
    result = list(text)
    offset = 0
    for m in matches:
        s = m + offset
        result.insert(s, "[")
        result.insert(s + pat_len + 1, "]")
        offset += 2
    return "".join(result)


def print_separator(char="═", width=62):
    print(char * width)


def print_result(res: dict, text: str, pattern: str):
    print_separator()
    print(f"  {res['algorithm']}")
    print_separator()
    print(f"  Text         : {text}")
    print(f"  Pattern      : {pattern}")
    print(f"  Match count  : {len(res['matches'])}")
    print(f"  Positions    : {res['matches']}")
    print(f"  Comparisons  : {res['comparisons']}")
    if "spurious_hits" in res:
        print(f"  Spurious hits: {res['spurious_hits']}  (d={res['d']}, q={res['q']})")
    if "lps_array" in res:
        print(f"  LPS array    : {res['lps_array']}")
    print(f"  Highlighted  : {highlight_matches(text, res['matches'], len(pattern))}")


def print_comparison(results: list, text: str, pattern: str):
    print_separator("─")
    print("  COMPARISON  (n={}, m={})".format(len(text), len(pattern)))
    print_separator("─")
    max_cmp = max(r["comparisons"] for r in results)
    for r in results:
        bar_len = int(30 * r["comparisons"] / max_cmp)
        bar     = "█" * bar_len + "░" * (30 - bar_len)
        print(f"  {r['algorithm'][:24]:<24} {bar} {r['comparisons']:>4}")
    print_separator("─")


def print_complexity_table():
    print_separator("═")
    print("  TIME COMPLEXITY ANALYSIS")
    print_separator("═")
    rows = [
        ("Naive",       "O(n)",    "O(n·m)",  "O(n·m)",  "O(1)",  "O(1)"),
        ("Rabin-Karp",  "O(n+m)",  "O(n+m)",  "O(n·m)*", "O(m)",  "O(1)"),
        ("KMP",         "O(n)",    "O(n+m)",  "O(n+m)",  "O(m)",  "O(m)"),
    ]
    hdr = f"  {'Algorithm':<14} {'Best':<10} {'Average':<10} {'Worst':<10} {'Preprocess':<12} {'Space'}"
    print(hdr)
    print("  " + "─" * 58)
    for r in rows:
        print(f"  {r[0]:<14} {r[1]:<10} {r[2]:<10} {r[3]:<10} {r[4]:<12} {r[5]}")
    print()
    print("  * Rabin-Karp worst case only when every window is a spurious hash hit.")
    print_separator("═")


def benchmark(func, text, pattern, runs=100_000):
    """Return average execution time in microseconds."""
    start = time.perf_counter()
    for _ in range(runs):
        func(text, pattern)
    elapsed = (time.perf_counter() - start) / runs * 1e6
    return round(elapsed, 4)


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 62)
    print("    PATTERN SEARCHING ALGORITHMS — DAA PROJECT")
    print("=" * 62)
    print(f"  Text    : {TEXT!r}")
    print(f"  Pattern : {PATTERN!r}")
    print()

    # Run algorithms
    r_naive = naive_search(TEXT, PATTERN)
    r_rk    = rabin_karp_search(TEXT, PATTERN)
    r_kmp   = kmp_search(TEXT, PATTERN)

    # Print individual results
    for r in (r_naive, r_rk, r_kmp):
        print_result(r, TEXT, PATTERN)
        print()

    # Comparison bar chart
    print_comparison([r_naive, r_rk, r_kmp], TEXT, PATTERN)

    # Time complexity table
    print()
    print_complexity_table()

    # Micro-benchmark
    print()
    print("  RUNTIME BENCHMARK  (avg over 100 000 runs)")
    print("  " + "─" * 44)
    for name, fn in [("Naive", naive_search),
                     ("Rabin-Karp", rabin_karp_search),
                     ("KMP", kmp_search)]:
        t = benchmark(fn, TEXT, PATTERN)
        print(f"  {name:<14} {t:>8.4f} µs/call")
    print_separator("─")
    print()
    print("  KEY TAKEAWAYS")
    print("  ─────────────────────────────────────────────")
    print("  • Naive    : simplest; fine for short text/pattern.")
    print("  • Rabin-Karp : great for multiple-pattern search (hash all).")
    print("  • KMP      : best guaranteed O(n+m) for single-pattern search.")
    print()
