from tinydb import TinyDB, where
from constants import DATABASE_PATH


class Tournament:
    """Tournament"""

    DB = TinyDB(DATABASE_PATH, indent=4)

    def __init__(self, name, place, time_control, date, description=""):
        """_summary_

        Args:
            name (string): name of the tournament
            place (string): place of the tournament
            date (string): start date of the tournament
            time_control (string): time control of the tournament
            description (str, optional): tournament director remarks.
        """

        self.tournament_id = name + '-' + date
        self.name = name
        self.place = place
        self.time_control = time_control
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
        """

        self.players.sort(key=lambda player: player.points, reverse=True)

    def save_tournament(self):
        """Save a tournament after a creation."""

        serialized_tournament = {
            'tournament_id': self.tournament_id,
            'name': self.name,
            'place': self.place,
            'time_control': self.time_control,
            'date': self.date,
            'description': self.description,
            'rounds': {},
            'players': {}
        }

        tournaments_table = Tournament.DB.table("Tournaments")
        tournaments_table.insert(serialized_tournament)

    def save_tournament_players(self):
        """Save players tournament
        in "Tournaments" table of the database.
        Used when:
        - players are loaded in a tournament ;
        - matchs results are completed = update of points."""

        id = self.tournament_id

        serialized_players = {}
        for player in self.players:
            index = self.players.index(player)
            key = index + 1
            serialized_players[key] = player.serialize_player()

        table = Tournament.DB.table("Tournaments")
        table.update({'players': serialized_players}, where('tournament_id') == id)

    def save_tournament_rounds(self):
        """Save rounds tournament
        in "Tournaments" table of the database.
        Used when:
        - round is created ;
        - matchs are created ;
        - matchs results are completed.
        """

        id = self.tournament_id

        serialized_rounds = {}
        for round in self.rounds:
            index = self.rounds.index(round)
            key = index + 1
            serialized_rounds[key] = round.serialize_round()

        table = Tournament.DB.table("Tournaments")
        table.update({'rounds': serialized_rounds}, where('tournament_id') == id)

    def update_player_point(self, player, points):
        """Update player points in players table.
        Used when:
        - Matchs results are completed

        Args:
            player (Player): player
            points (int): points of the player
        """

        player_id = player.player_id
        table = Tournament.DB.table("Players")
        table.update({'points': points}, where('player_id') == player_id)
