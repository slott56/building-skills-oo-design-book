"""
Building Skills in Object-Oriented Design V4

Expected number of throws until a seven.
"""
from typing import Iterator, Iterable, Tuple

def game_durations() -> Iterator[Tuple[int, float]]:
    p_7 = 1 / 6
    throws = 0
    while True:
        yield throws+1, p_7*(1-p_7)**(throws)
        throws += 1

def until_small(e: float, sequence: Iterable[Tuple[int, float]]) -> Iterator[Tuple[int, float]]:
    for throws, prob in sequence:
        if prob*throws < e:
            break
        yield throws, prob

print(f"Throws,P(7),Sum(P(7))")
expected = 0.0
total = 0.0
for t, p_7 in until_small(0.01, game_durations()):
    expected += t * p_7
    total += p_7
    print(f"{t},{p_7:.1%},{total:.0%}")

print(f"Expected game duration until 7: {float(expected)}")
