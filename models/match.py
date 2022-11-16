from .player import Player


class Match:
    """Match"""

    def __init__(self, player_one: Player, player_two: Player,
                 score_one='', score_two=''):
        """Initialize a match.

        Args:
            player_one (player): first player of the match
            player_two (player): second player of the match
            score one (int): score of the first player
            score two (int): score of the second player
        """

        self.match_stored = ([player_one, score_one], [player_two, score_two])

    def __str__(self):
        """Display a match with the following format.

               Returns:
                   str: match description
        """

        return f"{str(self.match_stored[0][0])} vs {self.match_stored[1][0]}\n" \
            f"Score: {self.match_stored[0][1]} - {self.match_stored[1][1]}\n"

    def serialize_match(self):
        """Serialize a match in order to add it in the database.

        Returns:
            serialized_match (dict): match serialized

        """

        serialized_match = {
            'player_one': self.match_stored[0][0].serialize_player(),
            'player_two': self.match_stored[1][0].serialize_player(),
            'score_one': self.match_stored[0][1],
            'score_two': self.match_stored[1][1]
        }

        return serialized_match
