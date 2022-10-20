from random import *


class Player:
    """Joueur"""

    def __init__(self, last_name, first_name, birth_date, sexe, ranking, player_id=None,
                 points=0, opponents=None):
        """Initialise un joueur"""

        if player_id is None:
            self.player_id = randint(0, 100)
        else:
            self.player_id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.sexe = sexe
        self.ranking = ranking
        self.points = points
        if opponents is None:
            self.opponents = []
        else:
            self.opponents = opponents
        self.opponents = []

    def __str__(self):
        """Affiche un joueur avec le format suivant"""
        return f"{self.last_name} {self.first_name} points={self.points} ranking={self.ranking}"

    def serialize_player(self):
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
