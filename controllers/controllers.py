"""Module to define controllers."""

import datetime
import os
from operator import itemgetter
from constants import DATABASE_PATH

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
        # menu
        self.menu = Menu()

        # views
        self.view = HomeMenuView(self.menu)

    def run(self):
        """Display the home menu.
        Get back the chosen controller.

        Returns:
            handler (Controller): controller associated to the choice
        """

        self.menu.add("auto",
                      "Créer un nouveau tournoi",
                      NewTournamentController())

        # if "Tournaments" table is not empty, i can resume a tournament
        if Tournament.DB.table("Tournaments").contains(doc_id=1) is True:
            self.menu.add("auto",
                          "Reprendre un tournoi",
                          OnGoingTournamentController())
        self.menu.add("auto",
                      "Ajouter un joueur",
                      PlayersController())
        # if "Players" table is not empty, i can update a player ranking
        if Tournament.DB.table("Players").contains(doc_id=1) is True:
            self.menu.add("auto",
                          "Mettre à jour le classement d'un joueur",
                          RankingController())
        # if databse is not empty, i can access reports
        if os.path.getsize(DATABASE_PATH) != 0:
            self.menu.add("auto",
                          "Afficher les rapports",
                          ReportsController())
        self.menu.add("auto",
                      "Quitter",
                      EndScreenController())
        self.menu.add("auto",
                      "Nettoyer l'affichage",
                      CleanController())

        choice = self.view.get_choice()

        return choice.handler


class NewTournamentController:
    """Controller to create a new tournament."""

    def __init__(self):
        """Generate a controller to create a tournament.
        """

        # menu
        self.menu = Menu()

        # views
        self.manager_view = ManagerView()
        self.view = HomeMenuView(self.menu)

    def create_tournament(self):
        """Create a tournament.

        Returns:
            tournament (Tournament): tournament created
        """

        tournament_info = self.manager_view.prompt_to_create_tournament()
        today_date = datetime.datetime.today()
        start_date = today_date.strftime("%d/%m/%Y")
        tournament_info.append(start_date)
        tournament = Tournament(*tournament_info)

        tournament.save_tournament()

        return tournament

    def run(self):
        """Method to create a new tournament
        and to automatically use the TournamentController.
        """

        tournament = self.create_tournament()

        return TournamentController(tournament)


class OnGoingTournamentController:
    """Controller to continue a tournament."""

    def __init__(self):
        """Initialize a controller to continue a tournament.
        """

        # menu
        self.menu = Menu()

        # views
        self.manager_view = ManagerView()
        self.view = HomeMenuView(self.menu)

    def load_tournament(self):
        """load a tournament already in database.

        Returns:
            tournament (Tournament): resumed tournament
        """

        if Tournament.DB.table("Tournaments").contains(doc_id=1) is False:
            print("\nThere is no tournament in the database.\n \
            You have to create a tournament before.")
        else:
            while True:
                id = self.manager_view.prompt_for_tournament_id()
                todo = Query()
                table = Tournament.DB.table("Tournaments")
                tournament_searched = table.search(todo.tournament_id == id)  # type: ignore
                if not tournament_searched:
                    print("\nL'id n'existe pas")
                    continue
                else:
                    break

            # initialization of the tournament
            tournament_parameters = [
                tournament_searched[0]['name'],
                tournament_searched[0]['place'],
                tournament_searched[0]['time_control'],
                tournament_searched[0]['date'],
                tournament_searched[0]['description']
            ]
            tournament = Tournament(*tournament_parameters)

            # Initialization of rounds' and players' tournament
            rounds = tournament_searched[0]['rounds']

            for round_key in rounds:
                round_parameters = [
                    rounds[round_key]['name'],
                    rounds[round_key]['start_date'],
                    rounds[round_key]['end_date']
                ]
                round = Round(*round_parameters)
                tournament.rounds.append(round)

                # Initialization of matchs list of each tournament round
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
                print("\nReprise du tournoi suivant:\n")
                print(f"{tournament.tournament_id}")
                print("Aucun tour n'a été créé.\n")

            else:
                current_round = tournament.rounds[len(tournament.rounds) - 1]
                print("\nReprise du tournoi suivant:\n")
                print(f"{tournament}")
                print(f"Tour actuel: {str(current_round)}\n")

            return tournament

    def run(self):
        """Method to load a tournament
        and to automatically use the TournamentController.
        """

        tournament = self.load_tournament()

        return TournamentController(tournament)


class TournamentController:
    """Controller to manager a tournament progress.
    """

    def __init__(self, tournament) -> None:
        """Initialize a tournament controller.

        Args:
            tournament (Tournament): tournament to control
        """
        self.tournament = tournament
        self.manager_view = ManagerView()

    def load_player(self):
        """Select one from the database and add it to the current tournament.

        Returns:
            list[player]: tournament players
        """

        if Tournament.DB.table("Players").contains(doc_id=1) is False:
            label = """
            Il n'y a pas de joueurs dans la base de données.
            Vous devez en ajouter avant.
            """
            print(label)
        else:
            while True:
                id = self.manager_view.prompt_for_player_id()
                todo = Query()
                players_table = self.tournament.DB.table("Players")
                player_researched = players_table.search(todo.player_id == id)
                if player_researched:
                    break
                else:
                    print("\nL'id n'existe pas.\n")
                    continue
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

            print(f"\nLe joueur a été ajouté au tournoi "
                  f"{self.tournament.tournament_id}.\n")

            self.tournament.save_tournament_players()

    def create_matchs(self):
        """Generate matchs of each round.

        Round 1: player 1 with player 5, player 2 with player 6 and so on.

        Round 2,3 and 4:
        players are sorted by theirs points.
        player 1 with player 2, player 3 with player 4 and so on.
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
                self.tournament.rounds[round_number - 1].matchs.append(match)
        else:
            self.tournament.sort_players_by_point()
            nb_matchs = len(self.tournament.rounds[round_number - 1].matchs)
            index_player = 0
            while nb_matchs < matchs_number_needed:
                player_un = self.tournament.players[index_player]
                player_deux = self.tournament.players[index_player + 1]
                match = Match(player_un, player_deux)
                self.tournament.rounds[round_number - 1].matchs.append(match)
                index_player += 2
                nb_matchs += 1

        self.tournament.save_tournament_rounds()

        print(f"\nLes matchs du tour {round_name} ont bien été initialisés\n")

    def create_round(self):
        """Create the next round of the tournament.
        Name and start time are automatically created.
        Round amtchs are automatically created.
        """

        if len(self.tournament.rounds) == 0:
            round_name = "Round 1"
        elif len(self.tournament.rounds) == 1:
            round_name = "Round 2"
        elif len(self.tournament.rounds) == 2:
            round_name = "Round 3"
        else:
            round_name = "Round 4"

        today_date = datetime.datetime.today()
        start_date = today_date.strftime("%d/%m/%Y %H:%M:%S")

        tour = Round(round_name,
                     start_date=start_date)
        print(f"\nLe tour suivant a été créé: \n"
              f"{tour.name}\n"
              f"{tour.start_date}\n")

        self.tournament.rounds.append(tour)
        self.tournament.save_tournament_rounds()

        self.create_matchs()

    def create_matchs_results(self):
        """Get matchs scores by asking for matchs results.
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

        today_date = datetime.datetime.today()
        end_date = today_date.strftime("%d/%m/%Y %H:%M:%S")
        self.tournament.rounds[round_number - 1].end_date = end_date
        print(f"\nLe tour {round_number} est terminé.\n")
        print(f"{self.tournament.rounds[round_number - 1]}\n")

        self.tournament.save_tournament_rounds()
        self.tournament.save_tournament_players()

    def update_ranking_end(self):
        """Update the ranking of each player manually. """

        for tournament_player in self.tournament.players:
            print(f"\n{tournament_player}")
            id = tournament_player.player_id
            while True:
                new_ranking = self.manager_view.prompt_for_ranking_update()
                if new_ranking.isdigit():
                    new_ranking = int(new_ranking)
                    break
                else:
                    continue

            table = Tournament.DB.table("Players")
            table.update({'ranking': new_ranking}, where('player_id') == id)

        print("\nLe classement de chaque joueur a été mis à jour.\n")

    def run(self):
        """Method to manage the tournament progress.
        """

        while True:

            menu = {
                "Ajouter un joueur dans le tournoi": self.load_player,
                "Créer un tour": self.create_round,
                "Ajouter des résultats": self.create_matchs_results,
                "Mettre à jour le classement": self.update_ranking_end
            }

            players_number = len(self.tournament.players)
            rounds_number = len(self.tournament.rounds)

            # if tournament doesn't have 8 players
            # we have to add a player
            if players_number != 8:
                menu.pop("Créer un tour")
                menu.pop("Ajouter des résultats")
                menu.pop("Mettre à jour le classement")
            # if tournament doesn't have a round
            # or 1, 2 or 3 rounds with an end date
            # we have to create a round
            elif rounds_number == 0 or \
                    (0 < rounds_number < 4 and
                     self.tournament.rounds[rounds_number - 1].end_date):
                menu.pop("Ajouter un joueur dans le tournoi")
                menu.pop("Ajouter des résultats")
                menu.pop("Mettre à jour le classement")
            # if tournament has a round without an end date
            # we have to assign results to close the round
            elif self.tournament.rounds[rounds_number - 1].end_date is None:
                menu.pop("Ajouter un joueur dans le tournoi")
                menu.pop("Créer un tour")
                menu.pop("Mettre à jour le classement")
            # if tournament has 4 rounds and an end date
            # we can only update the ranking of players tournament
            elif rounds_number == 4:
                menu.pop("Ajouter un joueur dans le tournoi")
                menu.pop("Créer un tour")
                menu.pop("Ajouter des résultats")

            choice = self.manager_view.get_choice(menu)

            if choice == "Q":
                return HomeMenuController()
            else:
                menu[choice]()


class PlayersController:
    """Controller to manager players.
    """

    def __init__(self) -> None:
        self.manager_view = ManagerView()

    def create_player(self):
        """Create player in the table "Players".
        Need to ask for players information
        to create it and automatically add it to the database.
        """

        player_information = self.manager_view.prompt_to_create_player()
        player = Player(player_information[0],
                        player_information[1],
                        player_information[2],
                        player_information[3],
                        int(player_information[4]))
        player.save_player()

    def run(self):
        """Method to create a player
        and get back to the home menu.
        """

        self.create_player()
        return HomeMenuController()


class ReportsController:
    """Controller to manage reports display.
    """

    def __init__(self):
        """Initialize a report controller.
        """
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
            todo = Query()
            table = Tournament.DB.table("Tournaments")
            tournament = table.search(todo.tournament_id == tournament_id)  # type: ignore
            if not tournament:
                print("\nL'id n'existe pas.\n")
                continue
            else:
                break
        players = tournament[0]['players']
        if not players:
            print("\nLe tournoi ne contient pas de joueurs.\n")
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
        """Get all tournaments of the database
        in form of tournament instance.
        """

        serialized_tournaments = Tournament.DB.table('Tournaments').all()
        for tournament in serialized_tournaments:
            tournament = Tournament(tournament['name'],
                                    tournament['place'],
                                    tournament['time_control'],
                                    tournament['date'],
                                    tournament['description'])
            self.elements.append(tournament)

    def get_tournament_rounds(self):
        """Get all rounds of a selected tournament. """

        while True:
            tournament_id = self.manager_view.prompt_for_tournament_id()
            todo = Query()
            table = Tournament.DB.table("Tournaments")
            tournament = table.search(todo.tournament_id == tournament_id)  # type: ignore
            if not tournament:
                print("\nL'id n'existe pas.\n")
                continue
            else:
                break

        rounds_researched = tournament[0]['rounds']
        if not rounds_researched:
            print("\nLe tournoi ne contient pas de tours.")
        else:
            for round in rounds_researched:
                round_parameters = [
                    rounds_researched[round]['name'],
                    rounds_researched[round]['start_date'],
                    rounds_researched[round]['end_date'],
                ]
                self.elements.append(Round(*round_parameters))

    def get_tournament_matchs(self):
        """Get all matchs of a selected tournament. """

        while True:
            tournament_id = self.manager_view.prompt_for_tournament_id()
            todo = Query()
            table = Tournament.DB.table("Tournaments")
            tournament = table.search(todo.tournament_id == tournament_id)  # type: ignore
            if not tournament:
                print("\nL'id n'existe pas.\n")
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
            print("\nLe tournoi ne possède pas de matchs.\n")
        else:
            for match in matchs_researched:
                player_one_parameters = [
                    match['player_one']['last_name'],
                    match['player_one']['first_name'],
                    match['player_one']['birth_date'],
                    match['player_one']['sexe'],
                    match['player_one']['ranking'],
                    match['player_one']['points']
                ]
                player_two_parameters = [
                    match['player_two']['last_name'],
                    match['player_two']['first_name'],
                    match['player_two']['birth_date'],
                    match['player_two']['sexe'],
                    match['player_two']['ranking'],
                    match['player_one']['points']
                ]
                match_parameters = [
                    Player(*player_one_parameters),
                    Player(*player_two_parameters),
                    match['score_one'],
                    match['score_two']
                    ]
                match_researched = Match(*match_parameters)
                self.elements.append(match_researched)

    def run(self):
        """Method to manage the report menu display
        and then allow the manager to choose.
        At the end, the view and a method allow to
        display the choosen report.
        """

        while True:

            self.elements = []

            menu = {
                "Afficher tous les joueurs ordre alpha": self.get_all_players,
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
            elif choice in ["Afficher tous les joueurs ordre alpha",
                            "Afficher les joueurs d'un tournoi (alpha)"]:
                menu[choice]('last_name')
            elif choice in ["Afficher tous les joueurs par ranking",
                            "Afficher les joueurs d'un tournoi (ranking)"]:
                menu[choice]('ranking')
            else:
                menu[choice]()

            self.manager_view.display_report(self.elements)


class RankingController:
    """Controller to change players ranking.
    """

    def __init__(self):
        self.manager_view = ManagerView()

    def update_ranking_any_time(self):
        """Update the ranking of a selected player.
        Table "Players" is update.
        """

        while True:
            id = self.manager_view.prompt_for_player_id()
            todo = Query()
            table = Tournament.DB.table("Players")
            player_researched = table.search(todo.player_id == id)  # type: ignore
            if not player_researched:
                print("\nL'id n'existe pas.\n")
                continue
            else:
                break
        new_ranking = self.manager_view.prompt_for_ranking_update()
        new_ranking = int(new_ranking)

        table = Tournament.DB.table("Players")
        table.update({'ranking': new_ranking}, where('player_id') == id)  # type: ignore

        print("\nLe classement du joueur a été mis à jour. \n")

    def run(self):
        """Method to update a player ranking
        and to automatically get back to home menu.

        Returns:
            HomeMenuController (Controller) : controller of the home menu
        """

        self.update_ranking_any_time()

        return HomeMenuController()


class EndScreenController:
    """Controller to leave the application.
    """

    def run(self):
        return None


class CleanController:
    """Controller to clean the command terminal.
    """

    def run(self):
        os.system('cls')
        return HomeMenuController()
