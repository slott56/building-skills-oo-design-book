"""
Building Skills in Object-Oriented Design V4

Preface Examples
"""
from collections import defaultdict

freq = defaultdict(int)
for d1 in range(6):
    for d2 in range(6):
        n = d1 + d2 + 2
        freq[n] += 1
print(freq)

from collections import Counter

freq = Counter((d1 + d2 + 2) for d1 in range(6) for d2 in range(6))
print(freq)
