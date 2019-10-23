"""
Mastering Object Oriented Design, 4ed.

A hello world to be sure all our tools work.
"""

from dataclasses import dataclass


@dataclass
class Greeting:
    greeting: str
    audience: str

    def __str__(self) -> str:
        return f"{self.greeting} {self.audience}"


def main() -> None:
    g = Greeting("hello", "world")
    print(g)


if __name__ == "__main__":
    main()
