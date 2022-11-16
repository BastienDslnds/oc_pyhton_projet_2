from models.tournament import Tournament


class Player:
    """Player."""

    def __init__(self, last_name, first_name, birth_date,
                 sexe, ranking, points=0):
        """Initialize a player.

        Args:
            last_name (str): last_name
            first_name (str): first_name
            birth_date (str): birth_date
            sexe (str): sexe
            ranking (int): ranking
            points (str): points
        """

        self.player_id = last_name + '-' + first_name + '-' + birth_date
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.sexe = sexe
        self.ranking = ranking
        self.points = points

    def __str__(self):
        """Display a player with the following format.

               Returns:
                   str: player description

        """

        return f"Player_id {self.player_id}: points={self.points} classement={self.ranking}"

    def serialize_player(self):
        """Serialize a player in order to add it in the database.

        Returns:
            serialized_player (dict): player serialized

        """

        serialized_player = {
            'player_id': self.player_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'sexe': self.sexe,
            'ranking': self.ranking,
            'points': self.points
        }

        return serialized_player

    def save_player(self):
        """Save player in the table "Players" of the database.
        Used when a player is created.
        """

        serialized_player = self.serialize_player()
        players_table = Tournament.DB.table("Players")
        players_table.insert(serialized_player)
