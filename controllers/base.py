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
        """Create the tournament by asking tournament information to the player.

        Returns:
            tournament (tournament): tournament
        """

        """self.tournament = Tournament("Tournoi initial", "Paris", "22/09/2022")
        self.tournament = Tournament("Tournoi 2", "Rennes", "30/09/2022")"""

        tournament_informations = self.manager_view.prompt_to_create_tournament
        self.tournament = Tournament(tournament_informations[0], tournament_informations[1], tournament_informations[2])

        print(f"Le tournoi suivant a bien été initialisé: \n"
              f"{self.tournament}")

        self.tournament.save_tournament()

        return self.tournament

    def create_player(self):
        """Add players in the tournament.
        Need to ask for players information to create it and add it to the tournament.

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
            print(f"Le joueur a été ajouté à la base de données.\n")
        else:
            print(f"Les joueurs ont été ajoutés à la base de données.\n")

    def load_player_in_tournament(self):
        """Select one or several player(s) from the database and add them to the current tournament.

        Returns:
            list[player]: tournament players
        """
        
        if Tournament.DB.table("Players").contains(doc_id=1) is False:
            print(f"There is no player in the database.\n \
            You have to create players before.")
        else:
            self.display_all_players('last_name')
            player_id = self.manager_view.prompt_for_player_id()
            User = Query()
            players_table = self.tournament.DB.table("Players")
            player_researched = players_table.search(User.player_id == player_id)
            player_researched = Player(player_researched[0]['last_name'],
                                    player_researched[0]['first_name'],
                                    player_researched[0]['birth_date'],
                                    player_researched[0]['sexe'],
                                    player_researched[0]['ranking'],
                                    player_researched[0]['points'])
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

        start_date = datetime.datetime.today().strftime("%d/%m/%Y")
        start_hour = datetime.datetime.now().time().strftime("%H:%M:%S")

        tour = Round(round_name,
                     start_date=start_date,
                     start_hour=start_hour)
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
        End time of the associated round is automatically created at the end. """

        round_number = len(self.tournament.rounds)
        matchs = self.tournament.rounds[round_number - 1].matchs
        for match in matchs:
            result = self.manager_view.prompt_for_match_result(match)
            if result == str(1):
                match.match_stored[0][1] = 1
                match.match_stored[1][1] = 0
                match.match_stored[0][0].points += 1
                self.tournament.update_player_point(match.match_stored[0][0], match.match_stored[0][0].points)
            elif result == str(2):
                match.match_stored[0][1] = 0
                match.match_stored[1][1] = 1
                match.match_stored[1][0].points += 1
                self.tournament.update_player_point(match.match_stored[1][0], match.match_stored[1][0].points)
            else:
                match.match_stored[0][1] = 0.5
                match.match_stored[1][1] = 0.5
                match.match_stored[0][0].points += 0.5
                match.match_stored[1][0].points += 0.5
                self.tournament.update_player_point(match.match_stored[0][0], match.match_stored[0][0].points)
                self.tournament.update_player_point(match.match_stored[1][0], match.match_stored[1][0].points)

        self.tournament.rounds[round_number - 1].end_date = datetime.datetime.today().strftime("%d/%m/%Y")
        self.tournament.rounds[round_number - 1].end_hour = datetime.datetime.now().time().strftime("%H:%M:%S")
        print(f"Le tour {round_number} est terminé")
        print(self.tournament.rounds[round_number - 1])

        self.tournament.save_tournament_rounds()
        self.tournament.save_tournament_players()

        # Mettre à jour les points des joueurs au niveau de la base de données players

    def display_all_players(self, sort_key):
        """Display all players in a chosen order.

        Args:
            sort_key (str): key to select a player parameter and to sort players list
        """

        serialized_players = Tournament.DB.table('Players').all()
        serialized_players_ordered = sorted(serialized_players, key=itemgetter(sort_key))
        print("Liste de tous les joueurs:\n")
        for player in serialized_players_ordered:
            player_displayed = Player(player['last_name'],
                                        player['first_name'],
                                        player['birth_date'],
                                        player['sexe'],
                                        player['ranking'],
                                        player['points'])
            print(f"{player_displayed}\n")

    def display_tournament_players(self, sort_key):
        """Display all players, of a selected tournament, in a chosen order.

        Args:
            sort_key (str): key to select a player parameter and to sort players list
        """

        self.display_report_tournaments()
        while True:
            tournament_id = self.manager_view.prompt_for_tournament_id()
            Request = Query()
            tournament_researched = Tournament.DB.table("Tournaments").search(Request.tournament_id == tournament_id)
            if not tournament_researched:
                print(f"L'id n'existe pas")
                continue
            else:
                break
        players = tournament_researched[0]['players']
        serialized_players = []
        for key in players:
            serialized_players.append(players[key])

        serialized_players_ordered = sorted(serialized_players, key=itemgetter(sort_key))
        print(f"Liste des joueurs du tournoi {tournament_id}:")
        for player in serialized_players_ordered:
            player_displayed = Player(player['last_name'],
                                        player['first_name'],
                                        player['birth_date'],
                                        player['sexe'],
                                        player['ranking'],
                                        player['points'])
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

    def display_report_tournaments(self):
        """Display all tournaments of the database. """

        tournaments = self.get_all_tournaments()
        print("Liste de tous les tournois: \n")
        for tournament in tournaments:
            print(f"{tournament}\n")

    def get_all_tournament_rounds(self):
        
        self.display_report_tournaments()
        while True:
            tournament_id = self.manager_view.prompt_for_tournament_id()
            Request = Query()
            tournament_researched = Tournament.DB.table("Tournaments").search(Request.tournament_id == tournament_id)
            if not tournament_researched:
                print(f"L'id n'existe pas")
                continue
            else:
                break
        rounds = tournament_researched[0]['rounds']
        return rounds, tournament_id

    def display_tournament_rounds(self):
        """Display all rounds of a selected tournament. """

        tournament_information = self.get_all_tournament_rounds()
        rounds_researched = tournament_information[0]
        tournament_id = tournament_information[1]
        print(f"Liste de tous les tours du tournoi {tournament_id}")
        for round in rounds_researched:
            round_displayed = Round(rounds_researched[round]['name'],
                                        rounds_researched[round]['start_date'],
                                        rounds_researched[round]['start_hour'],
                                        rounds_researched[round]['end_date'],
                                        rounds_researched[round]['end_hour'])
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

    def update_ranking_player_end_tournament(self):
        """Update the ranking of each player manually. """

        self.display_tournament_players('last_name')
        for tournament_player in self.tournament.players:
            print(tournament_player)
            player_id = tournament_player.player_id
            new_ranking = self.manager_view.prompt_for_ranking_update()
            new_ranking = int(new_ranking)

            players_table = Tournament.DB.table("Players")
            players_table.update({'ranking': new_ranking}, where('player_id') == player_id)

        print("Le classement de chaque joueur du tournoi a été mis à jour")

    def update_ranking_player_any_time(self):
        """Update the ranking of a selected player.

        It also modifies players ranking impacted by the new ranking of the selected player. """

        self.display_all_players('last_name')
        while True:
            player_id = self.manager_view.prompt_for_player_id()
            Player = Query()
            player_researched = Tournament.DB.table("Players").search(Player.player_id == player_id)
            if not player_researched:
                print(f"L'id n'existe pas.")
                continue
            else:
                break
        new_ranking = self.manager_view.prompt_for_ranking_update()
        new_ranking = int(new_ranking)

        players_table = Tournament.DB.table("Players")
        players_table.update({'ranking': new_ranking}, where('player_id') == player_id)

        print("Le classement du joueur a été mis à jour. \n")

    def load_tournament(self):

        if Tournament.DB.table("Tournaments").contains(doc_id=1) is False:
            print(f"There is no tournament in the database.\n \
            You have to create a tournament before.")
        else:
            self.display_report_tournaments()
            while True:
                tournament_id = self.manager_view.prompt_for_tournament_id()
                Request = Query()
                tournament_researched = Tournament.DB.table("Tournaments").search(Request.tournament_id == tournament_id)
                if not tournament_researched:
                    print(f"L'id n'existe pas")
                    continue
                else:
                    break

            # initialiser le tournoi
            tournament_name = tournament_researched[0]['name']
            tournament_place = tournament_researched[0]['place']
            tournament_date = tournament_researched[0]['date']
            tournament_description = tournament_researched[0]['description']
            self.tournament = Tournament(tournament_name,
                                        tournament_place,
                                        tournament_date,
                                        tournament_description)

            # initialiser la liste des tours et des players du tournoi
            rounds = tournament_researched[0]['rounds']

            for round_key in rounds:
                round = Round(rounds[round_key]['name'],
                            rounds[round_key]['start_date'],
                            rounds[round_key]['start_hour'],
                            rounds[round_key]['end_date'],
                            rounds[round_key]['end_hour'])
                self.tournament.rounds.append(round)

                # initialiser la liste des matchs de chaque round du tournoi
                matchs = tournament_researched[0]['rounds'][round_key]['matchs']
                for match_key in matchs:
                    match = Match(Player(matchs[match_key]['player_one']['last_name'],
                                        matchs[match_key]['player_one']['first_name'],
                                        matchs[match_key]['player_one']['birth_date'],
                                        matchs[match_key]['player_one']['sexe'],
                                        matchs[match_key]['player_one']['ranking'],
                                        matchs[match_key]['player_one']['points']),
                                Player(matchs[match_key]['player_two']['last_name'],
                                        matchs[match_key]['player_two']['first_name'],
                                        matchs[match_key]['player_two']['birth_date'],
                                        matchs[match_key]['player_two']['sexe'],
                                        matchs[match_key]['player_two']['ranking'],
                                        matchs[match_key]['player_one']['points']),
                                matchs[match_key]['score_one'],
                                matchs[match_key]['score_two'])
                    round_index = int(round_key) - 1
                    self.tournament.rounds[round_index].matchs.append(match)

            players = tournament_researched[0]['players']
            for player_key in players:
                player = Player(players[player_key]['last_name'],
                                players[player_key]['first_name'],
                                players[player_key]['birth_date'],
                                players[player_key]['sexe'],
                                players[player_key]['ranking'],
                                players[player_key]['points'])
                self.tournament.players.append(player)

            if not self.tournament.rounds:
                print(f"Reprise du tournoi suivant:\n" \
                    f"{self.tournament}" \
                    f"Aucun tour n'a été créé.")
            else:
                current_round = self.tournament.rounds[len(self.tournament.rounds) - 1]
                print(f"Reprise du tournoi suivant:\n"
                    f"{self.tournament}"
                    f"Tour actuel: {str(current_round)}\n")

    def run(self):
        """List actions for the progress of a tournament. """

        while True:

            global_menu = {"Créer un nouveau tournoi": self.create_tournament,
            "Reprendre un tournoi": self.load_tournament,
            "Mettre à jour le classement en fin de tournoi": self.update_ranking_player_end_tournament,
            "Mettre à jour le classement d'un joueur": self.update_ranking_player_any_time,
            "Créer un round": self.create_round,
            "Ajouter un joueur dans la base de données": self.create_player,
            "Ajouter un joueur dans un tournoi": self.load_player_in_tournament,
            "Créer les matchs": self.create_matchs,
            "Assigner les résultats": self.create_matchs_results,
            "Afficher un rapport": ''}

            reports_menu = {'Afficher tous les joueurs par ordre alpha': self.display_all_players,
                            'Afficher tous les joueurs par ranking': self.display_all_players,
                            "Afficher les joueurs d'un tournoi (alpha)": self.display_tournament_players,
                            "Afficher les joueurs d'un tournoi (ranking)": self.display_tournament_players,
                            'Afficher les tournois': self.display_report_tournaments,
                            "Afficher les tours d'un tournoi": self.display_tournament_rounds,
                            "Afficher les matchs d'un tournoi": self.display_tournament_matchs}

            # gestion de l'affichage des rapports
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

            # gestion de l'affichage pour le déroulement d'un tournoi
            if self.tournament is None:
                print("Menu pour créer ou reprendre un tournoi")
                global_menu.pop("Mettre à jour le classement en fin de tournoi")
                global_menu.pop("Créer un round")
                global_menu.pop("Ajouter un joueur dans un tournoi")
                global_menu.pop("Créer les matchs")
                global_menu.pop("Assigner les résultats")
                #  If we don't have all players in the tournament, we are forced to create or import player(s)
            else:
                players_number = len(self.tournament.players)
                rounds_number = len(self.tournament.rounds)
                #  Si je n'ai pas 8 joueurs dans le tournoi
                if players_number != 8:
                    print("Menu pour ajouter les joueurs au tournoi")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")
                    global_menu.pop("Créer un round")
                    global_menu.pop("Créer les matchs")
                    global_menu.pop("Assigner les résultats")
                #  If we don't have a round in the tournament, we are forced to create one
                elif rounds_number == 0:
                    print("Menu pour créer un tour")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")
                    global_menu.pop("Ajouter un joueur dans un tournoi")
                    global_menu.pop("Créer les matchs")
                    global_menu.pop("Assigner les résultats")
                # If we don't have all matchs in a round, we are forced to create match(s)
                elif len(self.tournament.rounds[rounds_number - 1].matchs) != 4:
                    print("Menu pour créer les matchs d'un tour")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")
                    global_menu.pop("Ajouter un joueur dans un tournoi")
                    global_menu.pop("Créer un round")
                    global_menu.pop("Assigner les résultats")
                # If we don't assign all matchs score = the round is not ended, we are forced to assign scores
                elif self.tournament.rounds[rounds_number - 1].end_date is None:
                    print("Menu pour assigner les résultats d'un tour")
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement en fin de tournoi")
                    global_menu.pop("Ajouter un joueur dans un tournoi")
                    global_menu.pop("Créer un round")
                    global_menu.pop("Créer les matchs")
                # cas d'une fin de tournoi
                elif rounds_number == 4:
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Mettre à jour le classement d'un joueur")
                    global_menu.pop("Créer un round")
                    global_menu.pop("Ajouter un joueur dans un tournoi")
                    global_menu.pop("Créer les matchs")
                    global_menu.pop("Assigner les résultats")
                else:
                    global_menu.pop("Créer un nouveau tournoi")
                    global_menu.pop("Reprendre un tournoi")
                    global_menu.pop("Ajouter un joueur dans un tournoi")
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

            # penser à mettre à jour les points de chaque joueur dans la table Players après chaque tour ?
