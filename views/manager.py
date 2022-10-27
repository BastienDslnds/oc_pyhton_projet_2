"""Base view."""


class ManagerView:
    """Manager view."""

    def prompt_for_choice(self, menu):
        """Prompt for a choice in the menu.

        Args:
            menu[str]: actions menu

        Returns:
            manager_choice (str): choice of the manager

        """
        menu_list = []
        for action in menu:
            menu_list.append(action)

        index_choice = 1
        for action in menu_list:
            print(f"Choice {index_choice} - {action}")
            index_choice += 1

        while True:
            manager_choice = input("Entrez un choix valide ou la lettre Q pour quitter l'application: ")

            if manager_choice == 'Q':
                manager_choice = "Q"
                break
            elif int(manager_choice) in list(range(1, len(menu_list)+1)):
                manager_choice = menu_list[int(manager_choice)-1]
                break
            else:
                print("Le choix n'est pas valide.")
                continue

        return manager_choice

    @property
    def prompt_to_create_tournament(self):
        """Prompt for a name, a place and a date of tournament.

        Returns:
            tournament_informations[str]: list of tournament information

        """

        tournament_informations = []
        name = input("Nom du tournoi: ")
        place = input("Lieu du tournoi: ")
        date = input("Date du tournoi: ")
        tournament_informations.append(name)
        tournament_informations.append(place)
        tournament_informations.append(date)
        return tournament_informations

    @property
    def prompt_to_create_player(self):
        """Prompt for the last_name, the first_name, the date of birth, the sexe and the ranking of a player.

        Returns:
            player_information[str]: list of player information

        """

        player_information = []
        last_name = input("Nom du joueur: ")
        first_name = input("Prénom du joueur: ")
        birth_date = input("Date de naissance:  ")
        while True:
            sexe = input("Sexe: ")
            if sexe not in ["M", "F"]:
                print(f"Renseigner M ou F")
                continue
            else:
                break
        ranking = input("Classement: ")
        while True:
            if ranking.isdigit():
                break
            else:
                continue
        player_information.append(last_name)
        player_information.append(first_name)
        player_information.append(birth_date)
        player_information.append(sexe)
        player_information.append(ranking)
        return player_information

    def prompt_for_number_players_to_create(self):
        """Ask for a number of players to create before the beginning of the tournament.

        Returns:
            number_players (int): number of players

        """

        number_players = input(f"Nombre de joueurs à créer: ")
        while True:
            if number_players.isdigit():
                break
            else:
                continue

        return number_players

    def prompt_for_match_result(self, match):
        """Ask for a match result.

        Returns:
            result (str): result of the match
        """

        while True:
            result = input(
                f"Choississez le résultat du match entre {match.match_stored[0][0]} et {match.match_stored[1][0]}.\n"
                f"Si {match.match_stored[0][0]} est le vainqueur, tapez 1\n"
                f"Si {match.match_stored[1][0]} est le vainqueur, tapez 2\n"
                f"Si match nul, tapez n\n"
                f"résultat: ")
            if result in ["1", "2", "n"]:
                break
            else:
                print("Choisir 1 ou 2 ou n")
                continue
        return result

    def prompt_for_player_id(self):
        """Ask for a player id.

        Returns:
            player_id (int): player id
        """

        player_id = input("Id du joueur au format suivant 'last_name-First_name-Birth_date' : ")

        return player_id

    def prompt_for_ranking_update(self):
        """Ask for the new ranking of a player.

        Returns:
            ranking (int): new ranking

        """

        ranking = input(f"Nouveau ranking: ")

        return ranking

    def prompt_for_tournament_id(self):
        """Ask for a tournament id.

        Returns:
            tournament id (str): new ranking

        """

        tournament_id = input(f"Id du tournoi au format suivant 'name-date': ")

        return tournament_id
