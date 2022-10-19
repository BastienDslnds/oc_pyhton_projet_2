from tinydb import TinyDB
from pathlib import Path
from random import *


class Tournament:
    """Tournament"""

    DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4)

    def __init__(self, name, place, date):
        """initialize a tournament. """

        self.id_tournament = randint()
        self.name = name
        self.place = place
        self.date = date
        self.nb_rounds = 4
        self.rounds = []  # rounds list of the tournament
        self.players = []  # players list of the tournament
        self.pairs = []
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

    def save_tournament(self):
        serialized_rounds = {}
        for round in self.rounds:
            index = self.rounds.index(round)
            key = index+1
            serialized_rounds[key] = round.serialized_round()

        serialized_tournament = {
            'name': self.name,
            'place': self.place,
            'date': self.date,
            'description': self.description,
            'rounds': serialized_rounds
        }

        tournaments_table = Tournament.DB.table("Tournaments")
        tournaments_table.truncate()
        tournaments_table.insert(serialized_tournament)

    def save_players(self):
        serialized_players = []
        for player in self.players:
            serialized_players.append(player.serialize_player())  # ajout d'un dictionnaire d'instance de joueur
        players_table = Tournament.DB.table("Players")
        players_table.truncate()
        players_table.insert_multiple(serialized_players)

