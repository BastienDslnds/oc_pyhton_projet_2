class Player:
    """Joueur"""

    def __init__(self, last_name, first_name, birth_date, sexe, ranking):
        """Initialise un joueur"""
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.sexe = sexe
        self.ranking = ranking
        self.points = 0

    def __str__(self):
        """Affiche un joueur avec le format suivant"""
        return f"{self.first_name} {self.last_name} points={self.points} ranking={self.ranking}"
