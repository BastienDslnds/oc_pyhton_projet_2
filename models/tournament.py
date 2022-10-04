class Tournament:
    """Tournament"""

    def __init__(self, name, place, date):
        """initialize a tournament. """

        self.name = name
        self.place = place
        self.date = date
        self.nb_rounds = 4
        self.rounds = []  # rounds list of the tournament
        self.players = []  # players list of the tournament
        self.description = ""

    def __str__(self):
        """Display the tounament with the following format. """

        return f"{self.name} à {self.place} le {self.date}"

    def sort_players_by_ranking(self):
        """Sort tournament players by ranking. """

        self.players.sort(key=lambda player: player.ranking)

    def sort_players_by_point(self):
        """First, sort players tournament by points.
        if players have the same number of points, then sort them by ranking. """

        self.players.sort(key=lambda player: player.points, reverse=True)
