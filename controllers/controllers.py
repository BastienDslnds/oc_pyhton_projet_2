import datetime
import os
from operator import itemgetter
from pathlib import Path

from tinydb import Query, where

from views.views import HomeMenuView, ManagerView
from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match
from utils.menu import Menu


class ApplicationController:
    """Initialize the application
    by lauching a home menu.
    """

    def __init__(self) -> None:
        """Initialize the application.
        """
        self.controller = None

    def start(self):
        """Start the application.
        It starts with the home menu controller."""

        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller.run()


class HomeMenuController:
    """Implement home menu logic.
    """

    def __init__(self) -> None:
        """Initialize the home menu.
        With a menu and a view using the menu.
        """

        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def run(self):
        """Display the home menu.
        Get back the controller chosen.

        Returns:
            handler (Controller): controller associated to the choice
        """

        self.menu.add("auto", "Créer un nouveau tournoi", NewTournamentController())
        if Tournament.DB.table("Tournaments").contains(doc_id=1) is True:
            self.menu.add("auto", "Reprendre un tournoi", OnGoingTournamentController())
        self.menu.add("auto", "Ajouter un joueur", PlayersController())
        if Tournament.DB.table("Players").contains(doc_id=1) is True:
            self.menu.add("auto", "Mettre à jour le classement d'un joueur", RankingController())
        if os.path.getsize(Path(__file__).resolve().parent.parent / 'database.json') != 0:
            self.menu.add("auto", "Afficher les rapports", ReportsController())
        self.menu.add("auto", "Quitter", EndScreenController())

        choice = self.view.get_choice()

        return choice.handler


class NewTournamentController:
    """Controller to create a new tournament."""

    def __init__(self):
        """Generate a controller to create a tournament.

        Args:
            menu (Menu): menu with next possible choices
            manager_view : view of the manager
            view (HomeMenuView) : view to display the menu
        """

        # menu
        self.menu = Menu()

        # views
        self.manager_view = ManagerView()
        self.view = HomeMenuView(self.menu)

    def create_tournament(self):
        """Create a tournament.

        Returns:
            tournament (Tournament): tournament
        """

        tournament_info = self.manager_view.prompt_to_create_tournament()
        tournament = Tournament(*tournament_info)

        print(f"Le tournoi suivant a bien été initialisé: \n"
              f"{tournament}")

        tournament.save_tournament()

        return tournament

    def run(self):
        """List of actions to create a new tournament
        and choose the next controller.
        """

        tournament = self.create_tournament()

        return TournamentController(tournament)


class OnGoingTournamentController:
    """Controller to continue a tournament."""

    def __init__(self):
        """Initialize a controller to continue a tournament.
        """

        self.menu = Menu()
        self.manager_view = ManagerView()
        self.view = HomeMenuView(self.menu)

    def load_tournament(self):

        if Tournament.DB.table("Tournaments").contains(doc_id=1) is False:
            print("There is no tournament in the database.\n \
            You have to create a tournament before.")
        else:
            while True:
                id = self.manager_view.prompt_for_tournament_id()
                Request = Query()
                table = Tournament.DB.table("Tournaments")
                tournament_searched = table.search(Request.tournament_id == id)
                if not tournament_searched:
                    print("L'id n'existe pas")
                    continue
                else:
                    break

            # initialiser le tournoi
            tournament_parameters = [
                tournament_searched[0]['name'],
                tournament_searched[0]['place'],
                tournament_searched[0]['date'],
                tournament_searched[0]['description']
            ]
            tournament = Tournament(*tournament_parameters)   

            # initialiser la liste des tours et des players du tournoi
            rounds = tournament_searched[0]['rounds']

            for round_key in rounds:
                round_parameters = [
                    rounds[round_key]['name'],
                    rounds[round_key]['start_date'],
                    rounds[round_key]['end_date']
                ]
                round = Round(*round_parameters)
                tournament.rounds.append(round)

                # initialiser la liste des matchs de chaque round du tournoi
                matchs = tournament_searched[0]['rounds'][round_key]['matchs']
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
                    tournament.rounds[round_index].matchs.append(match)

            players = tournament_searched[0]['players']
            for player_key in players:
                player = Player(players[player_key]['last_name'],
                                players[player_key]['first_name'],
                                players[player_key]['birth_date'],
                                players[player_key]['sexe'],
                                players[player_key]['ranking'],
                                players[player_key]['points'])
                tournament.players.append(player)

            if not tournament.rounds:
                print(f"Reprise du tournoi suivant:\n")
                print(f"{tournament.tournament_id}")
                print("Aucun tour n'a été créé.\n")

            else:
                current_round = tournament.rounds[len(tournament.rounds) - 1]
                print(f"Reprise du tournoi suivant:\n")
                print(f"{tournament}")
                print(f"Tour actuel: {str(current_round)}\n")
            
            return tournament

    def run(self):
        """List of actions to load a tournament
        and choose the next controller.
        """

        tournament = self.load_tournament()

        return TournamentController(tournament)


class TournamentController:

    def __init__(self, tournament) -> None:
        self.tournament = tournament
        self.manager_view = ManagerView()

    def load_player_in_tournament(self):
        """Select one or several player(s) from the database and add them to the current tournament.

        Returns:
            list[player]: tournament players
        """

        if Tournament.DB.table("Players").contains(doc_id=1) is False:
            print("There is no player in the database.\n \
            You have to create players before.")
        else:
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

    def update_ranking_end(self):
        """Update the ranking of each player manually. """

        for tournament_player in self.tournament.players:
            print(f"\n{tournament_player}")
            id = tournament_player.player_id
            new_ranking = self.manager_view.prompt_for_ranking_update()
            new_ranking = int(new_ranking)

            players_table = Tournament.DB.table("Players")
            players_table.update({'ranking': new_ranking}, where('player_id') == id)

        print("Le classement de chaque joueur du tournoi a été mis à jour")

    def run(self):
        while True:
            menu = {
                "Ajouter un joueur dans le tournoi": self.load_player_in_tournament,
                "Créer un tour": self.create_round,
                "Créer les matchs": self.create_matchs,
                "Ajouter des résultats": self.create_matchs_results,
                "Mettre à jour le classement en fin de tournoi": self.update_ranking_end
            }

            players_number = len(self.tournament.players)
            rounds_number = len(self.tournament.rounds)

            if players_number != 8:
                menu.pop("Créer un tour")
                menu.pop("Créer les matchs")
                menu.pop("Ajouter des résultats")
                menu.pop("Mettre à jour le classement en fin de tournoi")
            elif rounds_number == 0:
                menu.pop("Ajouter un joueur dans le tournoi")
                menu.pop("Créer les matchs")
                menu.pop("Ajouter des résultats")
                menu.pop("Mettre à jour le classement en fin de tournoi")
            elif rounds_number > 0 and self.tournament.rounds[rounds_number - 1].end_date:
                menu.pop("Ajouter un joueur dans le tournoi")
                menu.pop("Créer les matchs")
                menu.pop("Ajouter des résultats")
                menu.pop("Mettre à jour le classement en fin de tournoi")
            elif len(self.tournament.rounds[rounds_number - 1].matchs) != 4:
                menu.pop("Ajouter un joueur dans le tournoi")
                menu.pop("Créer un tour")
                menu.pop("Ajouter des résultats")
                menu.pop("Mettre à jour le classement en fin de tournoi")
            elif self.tournament.rounds[rounds_number - 1].end_date is None:
                menu.pop("Ajouter un joueur dans le tournoi")
                menu.pop("Créer un tour")
                menu.pop("Créer les matchs")
                menu.pop("Mettre à jour le classement en fin de tournoi")
            elif rounds_number == 4:
                menu.pop("Ajouter un joueur dans le tournoi")
                menu.pop("Créer un tour")
                menu.pop("Créer les matchs")
                menu.pop("Ajouter des résultats")

            choice = self.manager_view.get_choice(menu)

            if choice == "Q":
                return HomeMenuController()
            else:
                menu[choice]()


class PlayersController:

    def __init__(self) -> None:
        self.manager_view = ManagerView()

    def create_player(self):
        """Add players in the tournament.
        Need to ask for players information
        to create it and add it to the tournament.

        Returns:
            list[player] : tournament players
        """

        player_information = self.manager_view.prompt_to_create_player()
        player = Player(player_information[0],
                        player_information[1],
                        player_information[2],
                        player_information[3],
                        int(player_information[4]))
        player.save_player()

    def run(self):
        self.create_player()
        return HomeMenuController()


class ReportsController:

    def __init__(self):
        self.elements = []
        self.manager_view = ManagerView()

    def get_all_players(self, sort_key):
        """Display all players in a chosen order.

        Args:
            sort_key (str): key to select a player parameter
            and to sort players list
        """

        all_players = Tournament.DB.table('Players').all()
        all_players = sorted(all_players, key=itemgetter(sort_key))
        for player in all_players:
            player_parameters = [
                player['last_name'],
                player['first_name'],
                player['birth_date'],
                player['sexe'],
                player['ranking'],
                player['points']
            ]
            self.elements.append(Player(*player_parameters))

    def get_tournament_players(self, sort_key):
        """Display all players, of a selected tournament, in a chosen order.

        Args:
            sort_key (str): key to select a player parameter
            and to sort players list
        """

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
        if not players:
            print("Le tournoi ne contient pas de joueurs.")
        else:
            serialized_players = []
            for key in players:
                serialized_players.append(players[key])

            serialized_players = sorted(serialized_players, key=itemgetter(sort_key))
            for player in serialized_players:
                parameters = [
                    player['last_name'],
                    player['first_name'],
                    player['birth_date'],
                    player['sexe'],
                    player['ranking'],
                    player['points']
                ]
                self.elements.append(Player(*parameters))

    def get_all_tournaments(self):
        serialized_tournaments = Tournament.DB.table('Tournaments').all()
        for tournament in serialized_tournaments:
            tournament = Tournament(tournament['name'],
                                    tournament['place'],
                                    tournament['date'])
            self.elements.append(tournament)

    def get_tournament_rounds(self):
        """Display all rounds of a selected tournament. """

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

        rounds_researched = tournament[0]['rounds']
        if not rounds_researched:
            print("Le tournoi ne contient pas de tours.")
        else:
            for round in rounds_researched:
                round_parameters = [
                    rounds_researched[round]['name'],
                    rounds_researched[round]['start_date'],
                    rounds_researched[round]['end_date'],
                ]
                self.elements.append(Round(*round_parameters))

    def get_tournament_matchs(self):
        """Display all matchs of a selected tournament. """

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

        rounds_researched = tournament[0]['rounds']
        matchs_researched = []
        for round in rounds_researched:
            matchs_researched.append(rounds_researched[round]['matchs']['1'])
            matchs_researched.append(rounds_researched[round]['matchs']['2'])
            matchs_researched.append(rounds_researched[round]['matchs']['3'])
            matchs_researched.append(rounds_researched[round]['matchs']['4'])

        if not matchs_researched:
            print("Le tournoi ne possède pas de matchs.")
        else:
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
                self.elements.append(match_researched)

    def run(self):
        while True:

            self.elements = []

            menu = {
                "Afficher tous les joueurs par ordre alpha": self.get_all_players,
                "Afficher tous les joueurs par ranking": self.get_all_players,
                "Afficher les joueurs d'un tournoi (alpha)": self.get_tournament_players,
                "Afficher les joueurs d'un tournoi (ranking)": self.get_tournament_players,
                "Afficher les tournois": self.get_all_tournaments,
                "Afficher les tours d'un tournoi": self.get_tournament_rounds,
                "Afficher les matchs d'un tournoi": self.get_tournament_matchs
            }

            if Tournament.DB.table("Players").contains(doc_id=1) is False:
                menu.pop("Afficher tous les joueurs par ordre alpha")
                menu.pop("Afficher tous les joueurs par ranking")
            if Tournament.DB.table("Tournaments").contains(doc_id=1) is False:
                menu.pop("Afficher les joueurs d'un tournoi (alpha)")
                menu.pop("Afficher les joueurs d'un tournoi (ranking)")
                menu.pop("Afficher les tournois")
                menu.pop("Afficher les tours d'un tournoi")
                menu.pop("Afficher les matchs d'un tournoi")

            choice = self.manager_view.get_choice(menu)

            if choice == "Q":
                return HomeMenuController()
            elif choice in ["Afficher tous les joueurs par ordre alpha",
                            "Afficher les joueurs d'un tournoi (alpha)"]:
                menu[choice]('last_name')
            elif choice in ["Afficher tous les joueurs par ranking",
                            "Afficher les joueurs d'un tournoi (ranking)"]:
                menu[choice]('ranking')
            else:
                menu[choice]()

            self.manager_view.display_report(self.elements)


class RankingController:

    def __init__(self):
        self.manager_view = ManagerView()

    def update_ranking_any_time(self):
        """Update the ranking of a selected player."""

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

    def run(self):
        self.update_ranking_any_time()

        return HomeMenuController()


class EndScreenController:
    def run(self):
        return None

