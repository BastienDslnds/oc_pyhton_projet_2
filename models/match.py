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

    def __init__(self, player_un: Player, player_deux: Player, score_un='', score_deux=''):
        """Initialize a match"""

        self.match_stored = ([player_un, score_un], [player_deux, score_deux])

    def __str__(self):
        return f"{self.match_stored[0][0]} vs {self.match_stored[1][0]}\n" \
               f"Score: {self.match_stored[0][1]} - {self.match_stored[1][1]}"

    def serialize_match(self):
        serialized_match = {
            'player_un': self.match_stored[0][0].serialize_player(),
            'player_deux': self.match_stored[1][0].serialize_player(),
            'score_un': self.match_stored[0][1],
            'score_deux': self.match_stored[1][1]
        }

        return serialized_match
