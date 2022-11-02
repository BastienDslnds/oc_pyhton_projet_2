"""Module to define the main controller."""

import datetime
import os
from operator import itemgetter
from pathlib import Path

from tinydb import Query, where

from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament


class Controller:
    """Main controller."""

    def __init__(self, manager_view):
        """Generate a controller to handle a tournament.

        Args:
            manager_view : view of the manager
        """

        # models
        self.tournament = None

        # views
        self.manager_view = manager_view

    def display_menu(self, menu):
        """Display actions menu.

        Args:
            menu[string]:  possible actions

        Returns:
            manager_choice (str): action choice of the manager

        """

        manager_choice = self.manager_view.prompt_for_choice(menu)
        return manager_choice

    def create_tournament(self):
        """Create a tournament.

        Returns:
            tournament (tournament): tournament
        """

        tournament_informations = self.manager_view.prompt_to_create_tournament
        self.tournament = Tournament(*tournament_informations)

        print(f"Le tournoi suivant a bien été initialisé: \n"
              f"{self.tournament}")

        self.tournament.save_tournament()

        return self.tournament

    def create_player(self):
        """Add players in the tournament.
        Need to ask for players information
        to create it and add it to the tournament.

        Returns:
            list[player] : tournament players
        """

        while True:
            nb_players = self.manager_view.prompt_for_number_players_to_create()
            if nb_players.isdigit():
                break
            else:
                continue

        nb_players = int(nb_players)
        for player in range(nb_players):
            player_information = self.manager_view.prompt_to_create_player
            player = Player(player_information[0],
                            player_information[1],
                            player_information[2],
                            player_information[3],
                            int(player_information[4]))
            player.save_player()

        if nb_players == 1:
            print("Le joueur a été ajouté à la base de données.\n")
        else:
            print("Les joueurs ont été ajoutés à la base de données.\n")

    def load_player_in_tournament(self):
        """Select one or several player(s) from the database and add them to the current tournament.

        Returns:
            list[player]: tournament players
        """
        if Tournament.DB.table("Players").contains(doc_id=1) is False:
            print("There is no player in the database.\n \
            You have to create players before.")
        else:
            self.display_all_players('last_name')
            id = self.manager_view.prompt_for_player_id()
            User = Query()
            players_table = self.tournament.DB.table("Players")
            player_researched = players_table.search(User.player_id == id)
            player_parameters = [
                player_researched[0]['last_name'],
                player_researched[0]['first_name'],
                player_researched[0]['birth_date'],
                player_researched[0]['sexe'],
                player_researched[0]['ranking'],
                player_researched[0]['points']
            ]
            player_researched = Player(*player_parameters)
            self.tournament.players.append(player_researched)

            print(f"Le joueur a été ajouté au tournoi {self.tournament.tournament_id}.\n")

            self.tournament.save_tournament_players()

    def create_round(self):
        """Create the next round of the tournament.
        Name and start time are automatically created.

        Returns:
            list[round]: tournament rounds
        """

        if len(self.tournament.rounds) == 0:
            round_name = "Round 1"
        elif len(self.tournament.rounds) == 1:
            round_name = "Round 2"
        elif len(self.tournament.rounds) == 2:
            round_name = "Round 3"
        else:
            round_name = "Round 4"

        start_date = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")

        tour = Round(round_name,
                     start_date=start_date)
        print(f"Le tour suivant a été créé: \n"
              f"{tour}\n")
        self.tournament.rounds.append(tour)

        self.tournament.save_tournament_rounds()

        return self.tournament.rounds

    def create_matchs(self):
        """Generate matchs of each round.

        Round 1: player 1 with player 5, player 2 with player 6 and so on.

        Round 2: player 1 with player 2, plauyer 3 with player 4 and so on.
        If player 1 already played player 2, then player 1 with player 3.

        """

        round_number = len(self.tournament.rounds)
        round_name = self.tournament.rounds[round_number - 1].name
        matchs_number_needed = int(len(self.tournament.players) / 2)
        if round_number == 1:
            self.tournament.sort_players_by_ranking()
            sublist_players_1 = self.tournament.players[:matchs_number_needed]
            sublist_players_2 = self.tournament.players[matchs_number_needed:]
            first_round = list(zip(sublist_players_1, sublist_players_2))
            for match in first_round:
                player_one = match[0]
                player_two = match[1]
                match = Match(player_one, player_two)
                player_one.opponents.append(player_two)
                player_two.opponents.append(player_one)
                self.tournament.rounds[round_number - 1].matchs.append(match)
        else:
            self.tournament.sort_players_by_point()
            self.tournament.sort_players_by_point()
            nb_matchs_round = len(self.tournament.rounds[round_number - 1].matchs)
            index_player = 0
            while nb_matchs_round < matchs_number_needed:
                player_un = self.tournament.players[index_player]
                player_deux = self.tournament.players[index_player + 1]
                match = Match(player_un, player_deux)
                self.tournament.rounds[round_number - 1].matchs.append(match)
                index_player += 2
                nb_matchs_round += 1

        self.tournament.save_tournament_rounds()

        print(f"Les matchs du tour {round_name} ont bien été initialisés\n")

    def create_matchs_results(self):
        """Save matchs scores by asking for matchs results.
        End time of the associated round
        is automatically created at the end. """

        round_number = len(self.tournament.rounds)
        matchs = self.tournament.rounds[round_number - 1].matchs
        for match in matchs:
            result = self.manager_view.prompt_for_match_result(match)
            if result == str(1):
                match.match_stored[0][1] = 1
                match.match_stored[1][1] = 0
                match.match_stored[0][0].points += 1
                player = match.match_stored[0][0]
                points = match.match_stored[0][0].points
                self.tournament.update_player_point(player, points)
            elif result == str(2):
                match.match_stored[0][1] = 0
                match.match_stored[1][1] = 1
                match.match_stored[1][0].points += 1
                player = match.match_stored[1][0]
                points = match.match_stored[1][0].points
                self.tournament.update_player_point(player, points)
            else:
                match.match_stored[0][1] = 0.5
                match.match_stored[1][1] = 0.5
                match.match_stored[0][0].points += 0.5
                match.match_stored[1][0].points += 0.5
                player_one = match.match_stored[0][0]
                points_one = match.match_stored[0][0].points
                player_two = match.match_stored[1][0]
                points_two = match.match_stored[1][0].points
                self.tournament.update_player_point(player_one, points_one)
                self.tournament.update_player_point(player_two, points_two)

        end_date = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        self.tournament.rounds[round_number - 1].end_date = end_date
        print(f"Le tour {round_number} est terminé")
        print(self.tournament.rounds[round_number - 1])

        self.tournament.save_tournament_rounds()
        self.tournament.save_tournament_players()

    def display_all_players(self, sort_key):
        """Display all players in a chosen order.

        Args:
            sort_key (str): key to select a player parameter
            and to sort players list
        """

        all_players = Tournament.DB.table('Players').all()
        all_players = sorted(all_players, key=itemgetter(sort_key))
        print("Liste de tous les joueurs:\n")
        for player in all_players:
            player_parameters = [
                player['last_name'],
                player['first_name'],
                player['birth_date'],
                player['sexe'],
                player['ranking'],
                player['points']
            ]
            player_displayed = Player(*player_parameters)
            print(f"{player_displayed}\n")

    def display_tournament_players(self, sort_key):
        """Display all players, of a selected tournament, in a chosen order.

        Args:
            sort_key (str): key to select a player parameter
            and to sort players list
        """

        self.display_tournaments()
        while True:
            tournament_id = self.manager_view.prompt_for_tournament_id()
            Request = Query()
            table = Tournament.DB.table("Tournaments")
            tournament = table.search(Request.tournament_id == tournament_id)
            if not tournament:
                print("L'id n'existe pas")
                continue
            else:
                break
        players = tournament[0]['players']
        serialized_players = []
        for key in players:
            serialized_players.append(players[key])

        serialized_players = sorted(serialized_players, key=itemgetter(sort_key))
        print(f"Liste des joueurs du tournoi {tournament_id}:")
        for player in serialized_players:
            parameters = [
                player['last_name'],
                player['first_name'],
                player['birth_date'],
                player['sexe'],
                player['ranking'],
                player['points']
            ]
            player_displayed = Player(*parameters)
            print(player_displayed)

    def get_all_tournaments(self):
        serialized_tournaments = Tournament.DB.table('Tournaments').all()
        tournaments = []
        for tournament in serialized_tournaments:
            tournament = Tournament(tournament['name'],
                                    tournament['place'],
                                    tournament['date'])
            tournaments.append(tournament)
        return tournaments

    def display_tournaments(self):
        """Display all tournaments of the database. """

        tournaments = self.get_all_tournaments()
        print("Liste de tous les tournois: \n")
        for tournament in tournaments:
            print(f"{tournament}\n")

    def get_all_tournament_rounds(self):
        """Get all tournament rounds
        by selecting an id tournament.

        """
        self.display_tournaments()
        while True:
            tournament_id = self.manager_view.prompt_for_tournament_id()
            Request = Query()
            table = Tournament.DB.table("Tournaments")
            tournament = table.search(Request.tournament_id == tournament_id)
            if not tournament:
                print("L'id n'existe pas")
                continue
            else:
                break
        rounds = tournament[0]['rounds']
        return rounds, tournament_id

    def display_tournament_rounds(self):
        """Display all rounds of a selected tournament. """

        tournament_information = self.get_all_tournament_rounds()
        rounds_researched = tournament_information[0]
        tournament_id = tournament_information[1]
        print(f"Liste de tous les tours du tournoi {tournament_id}")
        for round in rounds_researched:
            round_parameters = [
                rounds_researched[round]['name'],
                rounds_researched[round]['start_date'],
                rounds_researched[round]['start_hour'],
                rounds_researched[round]['end_date'],
                rounds_researched[round]['end_hour']
            ]
            round_displayed = Round(*round_parameters)
            print(f"{round_displayed}\n")

    def display_tournament_matchs(self):
        """Display all matchs of a selected tournament. """

        tournament_information = self.get_all_tournament_rounds()
        rounds_researched = tournament_information[0]
        tournament_id = tournament_information[1]
        matchs_researched = []
        for round in rounds_researched:
            matchs_researched.append(rounds_researched[round]['matchs']['1'])
            matchs_researched.append(rounds_researched[round]['matchs']['2'])
            matchs_researched.append(rounds_researched[round]['matchs']['3'])
            matchs_researched.append(rounds_researched[round]['matchs']['4'])
        print(f"Liste de tous les matchs du tournoi {tournament_id} \n")
        for match in matchs_researched:
            match_researched = Match(Player(match['player_one']['last_name'],
                                            match['player_one']['first_name'],
                                            match['player_one']['birth_date'],
                                            match['player_one']['sexe'],
                                            match['player_one']['ranking']),
                                     Player(match['player_two']['last_name'],
                                            match['player_two']['first_name'],
                                            match['player_two']['birth_date'],
                                            match['player_two']['sexe'],
                                            match['player_two']['ranking']),
                                     match['score_one'],
                                     match['score_two'])
            print(match_researched)

    def update_ranking_end(self):
        """Update the ranking of each player manually. """

        self.display_tournament_players('last_name')
        for tournament_player in self.tournament.players:
            print(f"\n{tournament_player}")
            id = tournament_player.player_id
            new_ranking = self.manager_view.prompt_for_ranking_update()
            new_ranking = int(new_ranking)

            players_table = Tournament.DB.table("Players")
            players_table.update({'ranking': new_ranking}, where('player_id') == id)

        print("Le classement de chaque joueur du tournoi a été mis à jour")

    def update_ranking_any_time(self):
        """Update the ranking of a selected player."""

        self.display_all_players('last_name')
        while True:
            id = self.manager_view.prompt_for_player_id()
            Player = Query()
            table = Tournament.DB.table("Players")
            player_researched = table.search(Player.player_id == id)
            if not player_researched:
                print("L'id n'existe pas.")
                continue
            else:
                break
        new_ranking = self.manager_view.prompt_for_ranking_update()
        new_ranking = int(new_ranking)

        table = Tournament.DB.table("Players")
        table.update({'ranking': new_ranking}, where('player_id') == id)

        print("Le classement du joueur a été mis à jour. \n")

    def load_tournament(self):

        if Tournament.DB.table("Tournaments").contains(doc_id=1) is False:
            print("There is no tournament in the database.\n \
            You have to create a tournament before.")
        else:
            self.display_tournaments()
            while True:
                id = self.manager_view.prompt_for_tournament_id()
                Request = Query()
                table = Tournament.DB.table("Tournaments")
                tournament = table.search(Request.tournament_id == id)
                if not tournament:
                    print("L'id n'existe pas")
                    continue
                else:
                    break

            # initialiser le tournoi
            tournament_parameters = [
                tournament[0]['name'],
                tournament[0]['place'],
                tournament[0]['date'],
                tournament[0]['description']
            ]
            self.tournament = Tournament(*tournament_parameters)

            # initialiser la liste des tours et des players du tournoi
            rounds = tournament[0]['rounds']

            for round_key in rounds:
                round_parameters = [
                    rounds[round_key]['name'],
                    rounds[round_key]['start_date'],
                    rounds[round_key]['end_date']
                ]
                round = Round(*round_parameters)
                self.tournament.rounds.append(round)

                # initialiser la liste des matchs de chaque round du tournoi
                matchs = tournament[0]['rounds'][round_key]['matchs']
                for match_key in matchs:
                    player_one_parameters = [
                        matchs[match_key]['player_one']['last_name'],
                        matchs[match_key]['player_one']['first_name'],
                        matchs[match_key]['player_one']['birth_date'],
                        matchs[match_key]['player_one']['sexe'],
                        matchs[match_key]['player_one']['ranking'],
                        matchs[match_key]['player_one']['points']
                    ]
                    player_two_parameters = [
                        matchs[match_key]['player_two']['last_name'],
                        matchs[match_key]['player_two']['first_name'],
                        matchs[match_key]['player_two']['birth_date'],
                        matchs[match_key]['player_two']['sexe'],
                        matchs[match_key]['player_two']['ranking'],
                        matchs[match_key]['player_one']['points']
                    ]

                    match_parameters = [
                        Player(*player_one_parameters),
                        Player(*player_two_parameters),
                        matchs[match_key]['score_one'],
                        matchs[match_key]['score_two']
                    ]
                    match = Match(*match_parameters)
                    round_index = int(round_key) - 1
                    self.tournament.rounds[round_index].matchs.append(match)

            players = tournament[0]['players']
            for player_key in players:
                player = Player(players[player_key]['last_name'],
                                players[player_key]['first_name'],
                                players[player_key]['birth_date'],
                                players[player_key]['sexe'],
                                players[player_key]['ranking'],
                                players[player_key]['points'])
                self.tournament.players.append(player)

            if not self.tournament.rounds:
                response = "Reprise du tournoi suivant:\n"
                f"{self.tournament}"
                "Aucun tour n'a été créé."

                print(response)
            else:
                current_round = self.tournament.rounds[len(self.tournament.rounds) - 1]
                response = "Reprise du tournoi suivant:\n" \
                f"{self.tournament}" \
                f"Tour actuel: {str(current_round)}\n"
                print(response)

    def run(self):
        """List actions for the progress of a tournament. """

        while True:

            global_menu = {
                "Créer un nouveau tournoi": self.create_tournament,
                "Reprendre un tournoi": self.load_tournament,
                "Mettre à jour le classement en fin de tournoi": self.update_ranking_end,
                "Mettre à jour le classement d'un joueur": self.update_ranking_any_time,
                "Créer un round": self.create_round,
                "Ajouter un joueur dans la base de données": self.create_player,
                "Ajouter un joueur dans le tournoi": self.load_player_in_tournament,
                "Créer les matchs": self.create_matchs,
                "Assigner les résultats": self.create_matchs_results,
                "Afficher un rapport": ''
            }

            reports_menu = {
                "Afficher tous les joueurs par ordre alpha": self.display_all_players,
                "Afficher tous les joueurs par ranking": self.display_all_players,
                "Afficher les joueurs d'un tournoi (alpha)": self.display_tournament_players,
                "Afficher les joueurs d'un tournoi (ranking)": self.display_tournament_players,
                "Afficher les tournois": self.display_tournaments,
                "Afficher les tours d'un tournoi": self.display_tournament_rounds,
                "Afficher les matchs d'un tournoi": self.display_tournament_matchs
            }

            # Loops to handle menu display when database has not enough data
            if os.path.getsize(Path(__file__).resolve().parent.parent / 'db.json') == 0:
                global_menu.pop("Afficher un rapport")

            if Tournament.DB.table("Tournaments").contains(doc_id=1) is False:
                reports_menu.pop("Afficher les joueurs d'un tournoi (alpha)")
                reports_menu.pop("Afficher les joueurs d'un tournoi (ranking)")
                reports_menu.pop("Afficher les tournois")
                reports_menu.pop("Afficher les tours d'un tournoi")
                reports_menu.pop("Afficher les matchs d'un tournoi")

            if Tournament.DB.table("Players").contains(doc_id=1) is False:
                reports_menu.pop("Afficher tous les joueurs par ordre alpha")
                reports_menu.pop("Afficher tous les joueurs par ranking")
                global_menu.pop("Mettre à jour le classement d'un joueur")

            # Loops to handle the progress of a tournament
            # If no tournament is running
            if self.tournament is None:
                print("Menu when no tournament is running\n")
                global_menu.pop("Mettre à jour le classement en fin de tournoi")
                global_menu.pop("Créer un round")
                global_menu.pop("Ajouter un joueur dans le tournoi")
                global_menu.pop("Créer les matchs")
                global_menu.pop("Assigner les résultats")
            else:
                players_number = len(self.tournament.players)
                rounds_number = len(self.tournament.rounds)
                # If the tournament doesn't have 8 players
                if players_number != 8:
                    print("Menu when a tournament is running without 8 players\n")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")
                    global_menu.pop("Créer un round")
                    global_menu.pop("Créer les matchs")
                    global_menu.pop("Assigner les résultats")
                #  If the tournament doesn't have a round, we are forced to create one
                elif rounds_number == 0:
                    print("Menu when a tournament is running without a round\n")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")
                    global_menu.pop("Ajouter un joueur dans le tournoi")
                    global_menu.pop("Créer les matchs")
                    global_menu.pop("Assigner les résultats")
                # If a roud doesn't have all matchs, we are forced to create match(s)
                elif len(self.tournament.rounds[rounds_number - 1].matchs) != 4:
                    print("Menu when a running tournament has a round without 4 matchs\n")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")
                    global_menu.pop("Ajouter un joueur dans le tournoi")
                    global_menu.pop("Créer un round")
                    global_menu.pop("Assigner les résultats")
                # If all matchs don't have a score, we are forced to assign scores
                elif self.tournament.rounds[rounds_number - 1].end_date is None:
                    print("Menu when a running tournament has matchs without scores\n")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")
                    global_menu.pop("Ajouter un joueur dans le tournoi")
                    global_menu.pop("Créer un round")
                    global_menu.pop("Créer les matchs")
                # cas d'une fin de tournoi
                elif rounds_number == 4:
                    print("Menu when a tournament is running and the round 4 is done\n")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement d'un joueur")
                    global_menu.pop("Créer un round")
                    global_menu.pop("Ajouter un joueur dans le tournoi")
                    global_menu.pop("Créer les matchs")
                    global_menu.pop("Assigner les résultats")
                else:
                    print("Menu when a tournament is running and a round need to be created\n")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Ajouter un joueur dans le tournoi")
                    global_menu.pop("Créer les matchs")
                    global_menu.pop("Assigner les résultats")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")

            choice = self.display_menu(global_menu)

            if choice == "Q":
                break
            elif choice == "Afficher un rapport":
                choice = self.display_menu(reports_menu)
                if choice in ["Afficher tous les joueurs par ordre alpha",
                              "Afficher les joueurs d'un tournoi (alpha)"]:
                    reports_menu[choice]('last_name')
                elif choice in ["Afficher tous les joueurs par ranking",
                                "Afficher les joueurs d'un tournoi (ranking)"]:
                    reports_menu[choice]('ranking')
                else:
                    reports_menu[choice]()
            else:
                global_menu[choice]()
