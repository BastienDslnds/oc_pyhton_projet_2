"""Define the main controller."""

from models.tournament import Tournament
from models.round import Round
from models.match import PairPlayers, Match
from models.player import Player
from views.player import PlayerView

import datetime


class Controller:
    """Main controller."""

    def __init__(self, view):
        """Has a view. """

        # models

        # views
        self.view = view

    def get_tournament(self):
        """Create the tournament. """

        tournament_informations = self.view.prompt_for_tournament
        tournament = Tournament(tournament_informations[0], tournament_informations[1], tournament_informations[2])
        return tournament

    def get_players(self, tournament):
        """Add players in the tournament.

        Need to ask for players information to create it and add it to the tournament. """

        for player in range(8):
            player_information = self.view.prompt_for_player()
            player = Player(player_information[0],
                            player_information[1],
                            player_information[2],
                            player_information[3],
                            player_information[4])
            tournament.players.append(player)

    def open_round(self, tournament):
        """Add a round to the tournament.

        Automatically created with name et start time. """

        if len(tournament.rounds) == 0:
            tour = Round("Round 1")
        elif len(tournament.rounds) == 1:
            tour = Round("Round 2")
        else:
            tour = Round("Round 3")
        tour.start_date = datetime.datetime.today()
        tour.start_hour = datetime.datetime.now().time()
        tournament.rounds.append(tour)

    def get_matchs_pairs(self, tournament: Tournament, tour: Round):
        """Generate pairs of each round.

        Round 1: player 1 with player 5, player 2 with player 6 adn so on.

        Round 2: player 1 with player 2, plauyer 3 with player 4 and so on.
        Si player 1 already played player 2, then player 1 with player 3. """

        if len(tournament.rounds) == 1:
            tournament.sort_players_by_ranking()
            for i in range(int(len(tournament.players)/2)):
                pair_players = PairPlayers()  # pair_players = []
                pair_players.append(tournament.players[i])  # pair_players = [joueur 0]
                pair_players.append(tournament.players[i+4])  # pair_players = [joueur 0, joueur 1]
                match = Match()
                match.pair = pair_players
                tour.matchs.append(match)
        else:
            tournament.sort_players_by_point()
            pairs_list = []
            for tour in tournament.rounds:
                for match in tour.matchs:
                    pairs_list.append(match.pair)
            players_copy = []
            for player in tournament.players:
                players_copy.append(player)
            print(f"players_copy={players_copy}")
            while len(players_copy) != 0:
                print(len(players_copy))
                print(f"tournament_players={tournament.players}")
                for i in range(int(len(players_copy)-1)):
                    print(i)
                    new_paire = PairPlayers()
                    new_paire.append(players_copy[0])
                    new_paire.append(players_copy[i+1])
                    if new_paire or list(reversed(new_paire)) not in pairs_list:
                        new_match = Match()
                        new_match.pair = new_paire
                        tour.matchs.append(new_match)
                        for match in tour.matchs:
                            print(match)
                        del players_copy[i + 1]
                        del players_copy[0]
                        print(f"players_copy={players_copy}")
                        break
                    else:
                        i += 1
                        continue

    def get_matchs_results(self, tour: Round):
        """Save players points by asking for matchs information of the round. """

        for match in tour.matchs:
            result = self.view.prompt_for_match_result(match)
            if result == str(1):
                match.score_un = 1
                match.score_deux = 0
                match.pair[0].points += 1
            elif result == str(2):
                match.score_un = 0
                match.score_deux = 1
                match.pair[1].points += 1
            else:
                match.score_un = 0.5
                match.score_deux = 0.5
                match.pair[0].points += 0.5
                match.pair[1].points += 0.5

    def close_round(self, tour: Round):
        """Save end-date and end-hour of the round. """

        tour.end_date = datetime.datetime.today()
        tour.end_hour = datetime.datetime.now().time()

    def run(self):
        """List actions for the progress of a tournament. """

        tournament = self.get_tournament()
        self.get_players(tournament)

        # Loop to handle 4 tournament rounds
        for tour in range(tournament.nb_rounds):
            print(tour)
            self.open_round(tournament)
            self.get_matchs_pairs(tournament, tournament.rounds[tour])
            self.get_matchs_results(tournament.rounds[tour])
            self.close_round(tournament.rounds[tour])




