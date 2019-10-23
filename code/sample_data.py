"""
Building Skills in Object-Oriented Design V4

Extract sample data from Anscombe's Quartet.
"""

raw = """\
10.0	8.04	10.0	9.14	10.0	7.46	8.0	6.58
8.0	6.95	8.0	8.14	8.0	6.77	8.0	5.76
13.0	7.58	13.0	8.74	13.0	12.74	8.0	7.71
9.0	8.81	9.0	8.77	9.0	7.11	8.0	8.84
11.0	8.33	11.0	9.26	11.0	7.81	8.0	8.47
14.0	9.96	14.0	8.10	14.0	8.84	8.0	7.04
6.0	7.24	6.0	6.13	6.0	6.08	8.0	5.25
4.0	4.26	4.0	3.10	4.0	5.39	19.0	12.50
12.0	10.84	12.0	9.13	12.0	8.15	8.0	5.56
7.0	4.82	7.0	7.26	7.0	6.42	8.0	7.91
5.0	5.68	5.0	4.74	5.0	5.73	8.0	6.89
"""

import math

data = [tuple(map(float, row)) for row in (r.split() for r in raw.splitlines())]
x0 = [int(d[0]) for d in data]
print(x0)

print(sum(x0))
print(len(x0))
print(sum(x0) / len(x0))
print(sum((x - 9) ** 2 for x in x0))
print(math.sqrt(sum((x - 9) ** 2 for x in x0) / (len(x0) - 1)))

import statistics

print("mean = ", statistics.mean(x0))
print("stdev = ", statistics.stdev(x0))

from collections import Counter

freq = Counter((d1 + d2 + 2) for d1 in range(6) for d2 in range(6))

print(freq)
