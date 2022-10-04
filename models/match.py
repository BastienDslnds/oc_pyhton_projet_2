from typing import List

from .player import Player


class PairPlayers(List):
    """Paire de joueurs"""

    def append(self, object):
        """Append a card."""
        if not isinstance(object, Player):
            return ValueError("Vous ne pouvez ajouter que des joueurs !")
        return super().append(object)


class Match:
    """Match"""

    def __init__(self, score_un='', score_deux=''):
        """Initialise un match"""
        self.pair: List[Player] = PairPlayers()
        self.score_un = score_un
        self.score_deux = score_deux

    def __str__(self):
        return f"([{self.pair[0]}, {self.score_un}], [{self.pair[1]}, {self.score_deux}])"