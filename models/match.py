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

    """def __init__(self, score_un='', score_deux=''):
        Initialize a match

        self.pair: List[Player] = PairPlayers()
        self.score_un = score_un
        self.score_deux = score_deux"""

    def __init__(self, player_un: Player, player_deux: Player, score_un='', score_deux=''):
        """Initialize a match"""

        self.match_stored = ([player_un, score_un], [player_deux, score_deux])

    def __str__(self):
        return f"([{self.pair[0]}, {self.score_un}], [{self.pair[1]}, {self.score_deux}])"

    def serialize_match(self):
        """serialized_players = {}

        for player in self.pair:
            index = self.pair.index(player)
            key = index + 1
            serialized_players[key] = player.serialize_player()

        serialized_match = {
            'players': serialized_players,
            'score_un': self.score_un,
            'score_deux': self.score_deux
        }"""

        """serialized_match = {
            'player_un': self.player_un.serialize_player(),
            'player_deux': self.player_deux.serialize_player(),
            'score_un': self.score_un,
            'score_deux': self.score_deux
        }"""

        serialized_match = {
            'player_un': self.match_stored[0][0].serialize_player(),
            'player_deux': self.match_stored[1][0].serialize_player(),
            'score_un': self.match_stored[0][1],
            'score_deux': self.match_stored[1][1]
        }

        return serialized_match
