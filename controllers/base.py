"""Module to define the main controller."""

import datetime
from operator import itemgetter
from pathlib import Path
import os
from IPython.display import clear_output

from tinydb import Query

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

        """self.tournament = Tournament("1", "Tournoi initial", "Paris", "22/09/2022")"""
        self.tournament = Tournament("2", "Tournoi 2", "Rennes", "30/09/2022")
        print(f"Le tournoi suivant a bien été initialisé: \n"
              f"{self.tournament}")
        """tournament_informations = self.manager_view.prompt_to_create_tournament
        self.tournament = Tournament(tournament_informations[0], tournament_informations[1], tournament_informations[2])
        return self.tournament"""

    def create_tournament_players(self):
        """Add players in the tournament.
        Need to ask for players information to create it and add it to the tournament.

        Returns:
            list[player] : tournament players
        """

        joueur_un = Player("Deslandes", "Bastien", "10/11/1995", "M", 1)
        self.tournament.players.append(joueur_un)
        joueur_deux = Player("Idilbi", "Sam", "15/06/1995", "M", 4)
        self.tournament.players.append(joueur_deux)
        joueur_trois = Player("Leparoux", "Pierre", "10/11/1995", "M", 5)
        self.tournament.players.append(joueur_trois)
        joueur_quatre = Player("Crosnier", "Hugo", "10/11/1995", "M", 2)
        self.tournament.players.append(joueur_quatre)
        joueur_cinq = Player("Guillaume", "Camille", "10/11/1995", "M", 3)
        self.tournament.players.append(joueur_cinq)
        joueur_six = Player("Leporcher", "Ambroise", "10/11/1995", "M", 8)
        self.tournament.players.append(joueur_six)
        joueur_sept = Player("Perrin", "Hugo", "10/11/1995", "M", 6)
        self.tournament.players.append(joueur_sept)
        joueur_huit = Player("Coquet", "Jean", "10/11/1995", "M", 7)
        self.tournament.players.append(joueur_huit)

        print(f"Les joueurs suivants ont été ajoutés au tournoi {self.tournament.tournament_id}:\n")
        for player in self.tournament.players:
            print(f"{player}\n")

        """nb_players = self.manager_view.prompt_for_number_players_to_create()

        for player in range(nb_players):
            player_information = self.manager_view.prompt_to_create_player
            player = Player(player_information[0],
                            player_information[1],
                            player_information[2],
                            player_information[3],
                            player_information[4])
            self.tournament.players.append(player)
            
        return self.tournament.players"""

    def load_players_in_tournament(self):
        """Select one or several player(s) from the database and add them to the current tournament.

        Returns:
            list[player]: tournament players
        """

        self.display_all_players('last_name')
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

        return self.tournament.players

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
            for i in range(matchs_number_needed):
                player_un = self.tournament.players[i]
                player_deux = self.tournament.players[i + 4]
                match = Match(player_un, player_deux)
                self.tournament.rounds[round_number - 1].matchs.append(match)
        else:
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

        print(f"Les matchs du tour {round_name} ont bien été initialisés\n")

    def create_matchs_results(self):
        """Save matchs scores by asking for matchs results.
        End time of the associated round is automatically created at the end. """

        round_number = len(self.tournament.rounds)
        for match in self.tournament.rounds[round_number - 1].matchs:
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

        self.tournament.rounds[round_number - 1].end_date = datetime.datetime.today().strftime("%d/%m/%Y")
        self.tournament.rounds[round_number - 1].end_hour = datetime.datetime.now().time().strftime("%H:%M:%S")
        print(f"Le tour {round_number} est terminé")
        print(self.tournament.rounds[round_number - 1])

    def display_all_players(self, sort_key):
        """Display all players in a chosen order.

        Args:
            sort_key (str): key to select a player parameter and to sort players list
        """

        serialized_players = Tournament.DB.table('Players').all()
        serialized_players_ordered = sorted(serialized_players, key=itemgetter(sort_key))
        print("Liste de tous les joueurs:")
        for player in serialized_players_ordered:
            player_displayed = Player(player['last_name'],
                                      player['first_name'],
                                      player['birth_date'],
                                      player['sexe'],
                                      player['ranking'],
                                      player['points'])
            print(player_displayed)

    def display_tournament_players(self, sort_key):
        """Display all players, of a selected tournament, in a chosen order.

        Args:
            sort_key (str): key to select a player parameter and to sort players list
        """

        self.display_report_tournaments()
        tournament_id = self.manager_view.prompt_to_select_one_tournament()
        Request = Query()
        tournament_researched = Tournament.DB.table("Tournaments").search(Request.tournament_id == tournament_id)
        matchs = tournament_researched[0]['rounds']['1']['matchs']
        serialized_players = []
        for key in matchs:
            player_un = matchs[key]['player_one']
            player_deux = matchs[key]['player_two']
            serialized_players.append(player_un)
            serialized_players.append(player_deux)

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
            tournament = Tournament(tournament['tournament_id'],
                                    tournament['name'],
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
        tournament_id = self.manager_view.prompt_to_select_one_tournament()
        Request = Query()
        tournament_researched = Tournament.DB.table("Tournaments").search(Request.tournament_id == tournament_id)
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
                                    rounds_researched[round]['round_id'],
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
                                            match['player_one']['ranking'],
                                            match['player_one']['player_id']),
                                     Player(match['player_two']['last_name'],
                                            match['player_two']['first_name'],
                                            match['player_two']['birth_date'],
                                            match['player_two']['sexe'],
                                            match['player_two']['ranking'],
                                            match['player_two']['player_id']),
                                     match['score_one'],
                                     match['score_two'])
            print(match_researched)

    def update_tournament_ranking_end(self):
        """Update the ranking of each player manually. """

        for player in self.tournament.players:
            ranking = self.manager_view.prompt_for_ranking_update(player)
            player.ranking = ranking

        print("Le classement de chaque joueur du tournoi a été mis à jour")

    def update_ranking_player(self):
        """Update the ranking of a selected player.

        It also modifies players ranking impacted by the new ranking of the selected player. """

        self.display_tournament_players('last_name')
        player_id = self.manager_view.prompt_for_player_id
        Player = Query()
        player_researched = Tournament.DB.search(Player.player_id == player_id)
        new_ranking = self.manager_view.prompt_for_ranking_update()
        player_researched['ranking'] = new_ranking

        players_available = self.tournament.DB.table('Players').all()
        for player in players_available:
            if player['id_player'] != player_id:
                if player['ranking'] < new_ranking:
                    player['ranking'] -= 1
                elif player['ranking'] > new_ranking:
                    player['ranking'] += 1
                else:
                    continue
            else:
                continue

        players_table = Tournament.DB.table("Players")
        players_table.truncate()
        players_table.insert_multiple(players_available)

        print("Le classement du joueur a été mis à jour. \n"
              "Le classement des autres joueurs a été modifié en conséquence.")

    def delete_tournament(self):
        """Delete a tournament. """

        pass

    def delete_round(self):
        """Delete a round. """

        pass

    def load_tournament(self):
        self.display_report_tournaments()
        tournament_id = self.manager_view.prompt_to_select_one_tournament()
        Request = Query()
        tournament_researched = Tournament.DB.table("Tournaments").search(Request.tournament_id == tournament_id)

        # initialiser le tournoi
        tournament_name = tournament_researched[0]['name']
        tournament_place = tournament_researched[0]['place']
        tournament_date = tournament_researched[0]['date']
        tournament_description = tournament_researched[0]['description']
        self.tournament = Tournament(tournament_id,
                                     tournament_name,
                                     tournament_place,
                                     tournament_date,
                                     tournament_description)

        # initialiser la liste des tours et des players du tournoi
        rounds = tournament_researched[0]['rounds']

        for round_key in rounds:
            round = Round(rounds[round_key]['name'],
                          rounds[round_key]['round_id'],
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
                                     matchs[match_key]['player_one']['player_id']),
                              Player(matchs[match_key]['player_two']['last_name'],
                                     matchs[match_key]['player_two']['first_name'],
                                     matchs[match_key]['player_two']['birth_date'],
                                     matchs[match_key]['player_two']['sexe'],
                                     matchs[match_key]['player_two']['ranking'],
                                     matchs[match_key]['player_two']['player_id']),
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
                            players[player_key]['player_id'])
            self.tournament.players.append(player)

        print(f"Reprise du tournoi suivant:\n"
              f"{self.tournament}")

    def run(self):
        """List actions for the progress of a tournament. """

        while True:

            clear_output()
            menu_dict = {'Créer un nouveau tournoi': self.create_tournament,
                         'Reprendre un tournoi': self.load_tournament,
                         'Mettre à jour le classement en fin de tournoi': self.update_tournament_ranking_end,
                         'Créer un round': self.create_round,
                         "Créer les joueurs d'un tournoi": self.create_tournament_players,
                         "Importer les joueurs dans un tournoi": self.load_players_in_tournament,
                         'Créer les matchs': self.create_matchs,
                         'Assigner les résultats': self.create_matchs_results,
                         "Afficher un rapport": ''}

            menu_reports = {'Afficher tous les joueurs par ordre alpha': self.display_all_players,
                            'Afficher tous les joueurs par ranking': self.display_all_players,
                            "Afficher les joueurs d'un tournoi (alpha)": self.display_tournament_players,
                            "Afficher les joueurs d'un tournoi (ranking)": self.display_tournament_players,
                            'Afficher les tournois': self.display_report_tournaments,
                            "Afficher les tours d'un tournoi": self.display_tournament_rounds,
                            "Afficher les matchs d'un tournoi": self.display_tournament_matchs}

            if os.path.getsize(Path(__file__).resolve().parent.parent / 'db.json') == 0:
                menu_dict.pop("Reprendre un tournoi")
                menu_dict.pop("Afficher un rapport")
            else:
                #  vérifier si la table "Players" contient au moins un joueur
                if Tournament.DB.table("Players").contains(doc_id=1) is False:
                    menu_reports.pop("Afficher tous les joueurs par ordre alpha")
                    menu_reports.pop("Afficher tous les joueurs par ranking")

                #  vérifier si la table "Tournaments" contient déjà au moins un tournoi
                if Tournament.DB.table("Tournaments").contains(doc_id=1) is False:
                    menu_dict.pop("Reprendre un tournoi")
                    menu_reports.pop("Afficher les joueurs d'un tournoi (alpha)")
                    menu_reports.pop("Afficher les joueurs d'un tournoi (ranking)")
                    menu_reports.pop("Afficher les tournois")
                    menu_reports.pop("Afficher les tours d'un tournoi")
                    menu_reports.pop("Afficher les matchs d'un tournoi")

            #  If we don't have a tournament, we are forced to create one or to restart one.
            if self.tournament is None:
                menu_dict.pop("Mettre à jour le classement en fin de tournoi")
                menu_dict.pop("Créer un round")
                menu_dict.pop("Créer les joueurs d'un tournoi")
                menu_dict.pop("Importer les joueurs dans un tournoi")
                menu_dict.pop("Créer les matchs")
                menu_dict.pop("Assigner les résultats")
            #  If we don't have all players in the tournament, we are forced to create or import player(s)
            elif len(self.tournament.players) != 8:
                menu_dict.pop("Créer un nouveau tournoi")
                menu_dict.pop("Reprendre un tournoi")
                menu_dict.pop("Mettre à jour le classement en fin de tournoi")
                menu_dict.pop("Créer un round")
                menu_dict.pop("Créer les matchs")
                menu_dict.pop("Assigner les résultats")
            #  If we don't have a round in the tournament, we are forced to create one
            elif len(self.tournament.rounds) == 0:
                menu_dict.pop("Créer un nouveau tournoi")
                menu_dict.pop("Reprendre un tournoi")
                menu_dict.pop("Mettre à jour le classement en fin de tournoi")
                menu_dict.pop("Créer les joueurs d'un tournoi")
                menu_dict.pop("Importer les joueurs dans un tournoi")
                menu_dict.pop("Créer les matchs")
                menu_dict.pop("Assigner les résultats")
            elif len(self.tournament.rounds) == 4:
                menu_dict.pop("Reprendre un tournoi")
                menu_dict.pop("Créer les joueurs d'un tournoi")
                menu_dict.pop("Importer les joueurs dans un tournoi")
                menu_dict.pop("Créer les matchs")
                menu_dict.pop("Assigner les résultats")
            # If we don't have all matchs in a round, we are forced to create match(s)
            elif len(self.tournament.rounds[len(self.tournament.rounds) - 1].matchs) != 4:
                menu_dict.pop("Créer un nouveau tournoi")
                menu_dict.pop("Reprendre un tournoi")
                menu_dict.pop("Mettre à jour le classement en fin de tournoi")
                menu_dict.pop("Créer les joueurs d'un tournoi")
                menu_dict.pop("Importer les joueurs dans un tournoi")
                menu_dict.pop("Créer un round")
                menu_dict.pop("Assigner les résultats")
            # If we don't assign all matchs score = the round is not ended, we are forced to assign scores
            elif self.tournament.rounds[len(self.tournament.rounds) - 1].end_date is None:
                menu_dict.pop("Créer un nouveau tournoi")
                menu_dict.pop("Reprendre un tournoi")
                menu_dict.pop("Mettre à jour le classement en fin de tournoi")
                menu_dict.pop("Créer les joueurs d'un tournoi")
                menu_dict.pop("Importer les joueurs dans un tournoi")
                menu_dict.pop("Créer un round")
                menu_dict.pop("Créer les matchs")
            else:
                menu_dict.pop("Créer un nouveau tournoi")
                menu_dict.pop("Reprendre un tournoi")
                menu_dict.pop("Mettre à jour le classement en fin de tournoi")
                menu_dict.pop("Créer les joueurs d'un tournoi")
                menu_dict.pop("Importer les joueurs dans un tournoi")
                menu_dict.pop("Créer les matchs")
                menu_dict.pop("Assigner les résultats")

            choice = self.display_menu(menu_dict)

            if choice == "Q":
                break
            elif choice == "Afficher un rapport":
                choice = self.display_menu(menu_reports)
                if choice in ["Afficher tous les joueurs par ordre alpha",
                              "Afficher les joueurs d'un tournoi (alpha)"]:
                    menu_reports[choice]('last_name')
                elif choice in ["Afficher tous les joueurs par ranking",
                                "Afficher les joueurs d'un tournoi (ranking)"]:
                    menu_reports[choice]('ranking')
                else:
                    menu_reports[choice]()
            else:
                menu_dict[choice]()

            # sauvegarder si nous avons créé de nouveaux joueurs
            if choice == "Créer les joueurs d'un tournoi":
                self.tournament.save_players()
                self.tournament.save_tournament_players()
            elif choice == "Créer un nouveau tournoi":
                self.tournament.save_tournament()
            elif choice in ["Créer un round", "Créer les paires", "Assigner les résultats"]:
                self.tournament.save_tournament_rounds()
            elif choice == "Mettre à jour le classement en fin de tournoi":
                self.tournament.save_tournament_players()
            else:
                continue

            # penser à mettre à jour les points de chaque joueur dans la table Players après chaque tour ?
