"""
Building Skills in Object-Oriented Design V4

Preface Example
"""

from collections import defaultdict

combo = defaultdict(int)
for i in range(1, 7):
    for j in range(1, 7):
        roll = i + j
        combo[roll] += 1
for n in range(2, 13):
    print(f"{n:2d} {combo[n] / 36:6.2%}")
