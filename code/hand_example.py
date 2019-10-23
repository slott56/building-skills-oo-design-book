"""
Building Skills in Object-Oriented Design V4
"""
class Bet:
    def __init__(self, outcome: str, amount: int) -> None:
        self.outcome = outcome
        self.amount = amount

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(outcome={self.outcome}, amount={self.amount})"


class Hand:
    @property
    def bet(self) -> Bet:
        return self.ante

    @bet.setter
    def bet(self, bet: Bet) -> Bet:
        self.ante = bet

__test___ = {
    "ex1": """
>>> h = Hand()
>>> h.bet = Bet("Ante", 1)
>>> print(h.bet)
"""
}
