from random import *


class Player:
    """Joueur"""

    def __init__(self, last_name, first_name, birth_date, sexe, ranking, points=0):
        """Initialise un joueur"""

        self.id_player = randint(0, 100)
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.sexe = sexe
        self.ranking = ranking
        self.points = points
        self.opponents = []

    def __str__(self):
        """Affiche un joueur avec le format suivant"""
        return f"{self.first_name} {self.last_name} points={self.points} ranking={self.ranking}"

    def serialize_player(self):
        serialized_player = {
            'id_player': self.id_player,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'sexe': self.sexe,
            'ranking': self.ranking,
            'points': self.points
        }
        return serialized_player
