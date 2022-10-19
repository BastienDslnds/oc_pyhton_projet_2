"""Define the main controller."""

from models.tournament import Tournament
from models.round import Round
from models.match import PairPlayers, Match
from models.player import Player

from tinydb import Query
from operator import itemgetter

import datetime


class Controller:
    """Main controller."""

    def __init__(self, manager_view):
        """Has a manager view. """

        # models
        self.tournament = None

        # views
        self.manager_view = manager_view

    def display_menu_controller(self):
        manager_choice = self.manager_view.prompt_for_choice()
        return manager_choice

    def create_tournament_controller(self):
        """Create the tournament by asking tournament information to the player. """

        tournament_informations = self.manager_view.prompt_to_create_tournament
        self.tournament = Tournament(tournament_informations[0], tournament_informations[1], tournament_informations[2])

    def create_players_controller(self):
        """Add players in the tournament.

        Need to ask for players information to create it and add it to the tournament. """

        nb_players = self.manager_view.prompt_for_number_players_to_create()

        for player in range(nb_players):
            player_information = self.manager_view.prompt_to_create_player
            player = Player(player_information[0],
                            player_information[1],
                            player_information[2],
                            player_information[3],
                            player_information[4])
            self.tournament.players.append(player)

    def select_players_controller(self):
        """Select one or several player(s) from the database and add them to the current tournament."""

        print(self.tournament.DB.table('Players').all())
        ids_player = self.manager_view.prompt_to_select_players()
        ids_player = ids_player.split(',')
        User = Query()
        for id in ids_player:
            player_researched = self.tournament.DB.table("Players").search(User.last_name == id)
            player_researched = Player(player_researched['id_player'],
                                       player_researched['last_name'],
                                       player_researched['first_name'],
                                       player_researched['birth_date'],
                                       player_researched['sexe'],
                                       player_researched['ranking'],
                                       player_researched['points'])
            self.tournament.players.append(player_researched)


    def create_round_controller(self):
        """Add a round to the tournament.

        Automatically created with name et start time. """

        if len(self.tournament.rounds) == 0:
            tour = Round("Round 1")
            print(tour)
        elif len(self.tournament.rounds) == 1:
            tour = Round("Round 2")
            print(tour)
        else:
            tour = Round("Round 3")
            print(tour)
        tour.start_date = datetime.datetime.today().strftime("%d/%m/%Y")
        tour.start_hour = datetime.datetime.now().time().strftime("%H:%M:%S")
        self.tournament.rounds.append(tour)

    def create_matchs_pairs_controller(self):
        """Generate pairs of each round.

        Round 1: player 1 with player 5, player 2 with player 6 adn so on.

        Round 2: player 1 with player 2, plauyer 3 with player 4 and so on.
        Si player 1 already played player 2, then player 1 with player 3. """

        tour_number = len(self.tournament.rounds)
        if tour_number == 1:
            self.tournament.sort_players_by_ranking()
            for i in range(int(len(self.tournament.players)/2)):
                player_un = self.tournament.players[i]
                player_deux = self.tournament.players[i+4]
                match = Match(player_un, player_deux)
                self.tournament.rounds[tour_number-1].matchs.append(match)
        else:
            self.tournament.sort_players_by_point()
            players_available = self.tournament.players
            i = 0
            while len(self.tournament.rounds[tour_number-1].matchs) < 8:
                player_init = self.tournament.players[i]
                if player_init in players_available:
                    for player in self.tournament.players[i+1:8]:
                        if player not in player_init.opponents:
                            new_match = Match(player_init, player)
                            self.tournament.rounds[tour_number-1].matchs.append(new_match)
                            i += 1
                            del players_available[player_init]
                            del players_available[player]
                            break
                        else:
                            continue
                else:
                    i += 1

    def create_matchs_results_controller(self):
        """Save players points by asking for matchs information of the round. """

        round_number = len(self.tournament.rounds)
        for match in self.tournament.rounds[round_number-1].matchs:
            result = self.manager_view.prompt_for_match_result(match)
            if result == str(1):
                match.match_stored[0][1] = 1
                match.match_stored[1][1] = 0
                match.match_stored[0][0].points += 1
            elif result == str(2):
                match.match_stored[0][1] = 0
                match.match_stored[1][1] = 1
                match.match_stored[1][0].points += 1
            else:
                match.match_stored[0][1] = 0.5
                match.match_stored[1][1] = 0.5
                match.match_stored[0][0].points += 0.5
                match.match_stored[1][0].points += 0.5

    def display_report_all_players_by_alpha_order(self):
        serialized_players = self.tournament.DB.table('Players').all()  # liste avec chaque dictionnaire de joueur
        serialized_players_ordered = sorted(serialized_players, key=itemgetter('last_name'))
        for player in serialized_players_ordered:
            player_displayed = Player(player['last_name'],
                                      player['first_name'],
                                      player['birth_date'],
                                      player['sexe'],
                                      player['ranking'])
            print(player_displayed)
        return serialized_players_ordered

    def display_report_all_players_by_ranking_order(self):
        serialized_players = self.tournament.DB.table('Players').all()  # liste avec chaque dictionnaire de joueur
        serialized_players_ordered = sorted(serialized_players, key=itemgetter('ranking'))
        for player in serialized_players_ordered:
            player_displayed = Player(player['last_name'],
                                      player['first_name'],
                                      player['birth_date'],
                                      player['sexe'],
                                      player['ranking'])
            print(player_displayed)
        return serialized_players_ordered

    def display_report_tournament_players_by_alpha_order(self):
        pass

    def display_report_tournament_players_by_ranking_order(self):
        pass

    def display_report_tournaments(self):
        serialized_tournaments = self.tournament.DB.table('Tournaments').all()
        for tournament in serialized_tournaments:
            tournament_displayed = Tournament(tournament['id_tournament'],
                                          tournament['name'],
                                          tournament['place'],
                                          tournament['date'])
            print(tournament_displayed)

    def display_report_rounds_tournament(self):
        tournaments_available = self.tournament.DB.table('Tournaments').all()
        print(tournaments_available)
        id_tournament = self.manager_view.prompt_for_to_select_one_tournament()
        for tournament in tournaments_available:
            if tournament['id_tournament'] == id_tournament:
                print(tournament.rounds)
            else:
                continue
        pass

    def display_report_matchs_tournament(self):
        pass

    def update_tournament_controller(self):
        pass

    def update_matchs_results_controller(self):
        pass

    def update_round_controller(self):
        """Save end-date and end-hour of the round. """

        round_number = len(self.tournament.rounds)
        self.tournament.rounds[round_number-1].end_date = datetime.datetime.today().strftime("%d/%m/%Y")
        self.tournament.rounds[round_number-1].end_hour = datetime.datetime.now().time().strftime("%H:%M:%S")
        print(f"Tour {round_number} terminé")
        print(self.tournament.rounds[round_number-1])

    def update_ranking_end_tournament_controller(self):
        """Update the ranking of each player manually. """

        for player in self.tournament.players:
            ranking = self.manager_view.prompt_for_update_ranking(player)
            player.ranking = ranking

    def update_ranking_player_controller(self):
        """Update the ranking of a selected player.

        It also modifies players ranking impacted by the new ranking of the selected player. """

        players_available = self.tournament.DB.table('Players').all()
        print(players_available)
        player_information = self.manager_view.prompt_for_one_player_ranking_update()
        ranking_init = 0
        for player in players_available:
            if player['id_player'] == player_information[0]:
                ranking_init = player['ranking']
                player['ranking'] = player_information[1]
                break
            else:
                continue

        for player in players_available:
            if player['id_player'] != player_information[0]:
                if ranking_init < player['ranking'] < player_information[1]:
                    player['ranking'] -= 1
                elif player['ranking'] > player_information[1]:
                    player['ranking'] += 1
                else:
                    continue
            else:
                continue

        players_table = Tournament.DB.table("Players")
        players_table.truncate()
        players_table.insert_multiple(players_available)

    def delete_tournament_controller(self):
        pass

    def delete_round_controller(self):
        pass

    def run(self):
        """List actions for the progress of a tournament. """

        while True:
            manager_choice = self.display_menu_controller()

            functions = {"A": self.create_tournament_controller,
                         "B": self.create_players_controller,
                         "C": self.create_round_controller,
                         "D": self.create_matchs_pairs_controller,
                         "E": self.create_matchs_results_controller,
                         "F": self.update_round_controller,
                         "G": self.update_ranking_player_controller,
                         "H": self.update_ranking_end_tournament_controller,
                         "I": self.display_report_all_players_by_alpha_order,
                         "J": self.display_report_tournaments,
                         "K": self.select_players_controller}

            if manager_choice == "Q":
                break
            else:
                functions[manager_choice]()

            if manager_choice != "G":
                self.tournament.save_players()
            else:
                continue

            self.tournament.save_tournament()








