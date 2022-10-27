from tinydb import TinyDB, where
from pathlib import Path
from random import *


class Tournament:
    """Tournament"""

    DB = TinyDB(Path(__file__).resolve().parent.parent / 'db.json', indent=4)

    def __init__(self, name, place, date, description=""):
        """initialize a tournament. """

        self.tournament_id = name + '-' + date
        self.name = name
        self.place = place
        self.date = date
        self.nb_rounds = 4
        self.rounds = []  # rounds list of the tournament
        self.players = []  # players list of the tournament
        self.description = description

    def __str__(self):
        """Display the tournament with the following format.

        Returns:
            str: tournament description

        """

        return f"Id du tournoi: {self.tournament_id}\n" \
               f"{self.name} à {self.place} le {self.date}\n"

    def sort_players_by_ranking(self):
        """Sort tournament players by ranking. """

        self.players.sort(key=lambda player: player.ranking)

    def sort_players_by_point(self):
        """First, sort players tournament by points.
        if players have the same number of points, then sort them by ranking. """

        self.players.sort(key=lambda player: player.points, reverse=True)

    def save_tournament(self):
        """Save a tournament after an initialisation."""

        serialized_tournament = {
            'tournament_id': self.tournament_id,
            'name': self.name,
            'place': self.place,
            'date': self.date,
            'description': self.description,
            'rounds': {},
            'players': {}
        }

        tournaments_table = Tournament.DB.table("Tournaments")
        tournaments_table.insert(serialized_tournament)

    def save_tournament_players(self):
        """Update on players' tournament on the database. """

        tournament_id = self.tournament_id

        serialized_players = {}
        for player in self.players:
            index = self.players.index(player)
            key = index + 1
            serialized_players[key] = player.serialize_player()

        tournaments_table = Tournament.DB.table("Tournaments")
        tournaments_table.update({'players': serialized_players}, where('tournament_id') == tournament_id)

    def save_tournament_rounds(self):
        """Update on rounds' tournament on the database. """

        tournament_id = self.tournament_id

        serialized_rounds = {}
        for round in self.rounds:
            index = self.rounds.index(round)
            key = index + 1
            serialized_rounds[key] = round.serialize_round()

        tournaments_table = Tournament.DB.table("Tournaments")
        tournaments_table.update({'rounds': serialized_rounds}, where('tournament_id') == tournament_id)

    def update_player_point(self, player, points):
        player_id = player.player_id
        players_table = Tournament.DB.table("Players")
        players_table.update({'points': points}, where('player_id') == player_id)

    def update_player_ranking(self, player, ranking):
        player_id = player.player_id
        players_table = Tournament.DB.table("Players")
        players_table.update({'points': ranking}, where('player_id') == player_id)

