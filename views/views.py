class HomeMenuView:

    def __init__(self, menu) -> None:
        self.menu = menu

    def display(self):
        print("\n")
        for key, value in self.menu.entries.items():
            print(f"{key} - {value.option}")

    def get_choice(self):

        while True:
            self.display()
            choice = input(">>")
            if choice in self.menu.entries:
                break
            else:
                continue
        choice = self.menu.entries[str(choice)]
        return choice


class ManagerView:

    def display_menu(self, menu):
        menu_list = []
        for action in menu:
            menu_list.append(action)

        index_choice = 1
        for action in menu_list:
            print(f"Choice {index_choice} - {action}")
            index_choice += 1

        return menu_list

    def get_choice(self, menu):
        """Prompt for a choice in the menu.

        Args:
            menu[str]: actions menu

        Returns:
            manager_choice (str): choice of the manager

        """
        menu_list = self.display_menu(menu)
        while True:
            choice = input("Entrez un choix valide "
                           "ou Q pour revenir au menu d'accueil:")

            if choice == 'Q':
                choice = "Q"
                break
            elif not choice.isdigit():
                continue
            elif int(choice) in list(range(1, len(menu_list)+1)):
                choice = menu_list[int(choice)-1]
                break
            else:
                print("\nLe choix n'est pas valide.")
                continue

        return choice

    def prompt_to_create_tournament(self):
        """Prompt for a name, a place and a date of tournament.

        Returns:
            tournament_informations[str]: list of tournament information

        """

        tournament_informations = []

        name = input("\nNom du tournoi: ")
        place = input("Lieu du tournoi: ")
        date = input("Date du tournoi: ")

        tournament_informations.append(name)
        tournament_informations.append(place)
        tournament_informations.append(date)

        return tournament_informations

    def prompt_to_create_player(self):
        """Prompt for the last_name, the first_name, the date of birth,
        the sexe and the ranking of a player.

        Returns:
            player_information[str]: list of player information

        """

        while True:
            label = """
            Entrez un nouveau joueur à créer
            Format attendu :
            "Nom,Prénom,date de naissance(JJ/MM/AAAA),sexe(M ou F),classement"
            """
            player = input(label)
            player_info = list(player.split(','))
            if player_info[3] in ["M", "F"] and player_info[4].isdigit():
                break
            else:
                print("\nPour le sexe, renseigner M ou F\n"
                      "Pour le ranking, renseigner un nombre\n")

        return player_info

    def prompt_for_player_id(self):
        """Ask for a player id.

        Returns:
            player_id (int): player id
        """

        label = """
        Entrez l'Id du joueur
        Format attendu : "last_name-First_name-Birth_date"
        """

        player_id = input(label)

        return player_id

    def prompt_for_match_result(self, match):
        """Ask for a match result.

        Returns:
            result (str): result of the match
        """

        while True:
            result = input(
                f"\nChoississez le résultat du match entre: " +
                f"{match.match_stored[0][0]} et {match.match_stored[1][0]}.\n"
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

    def prompt_for_tournament_id(self):
        """Ask for a tournament id.

        Returns:
            tournament id (str): new ranking

        """

        label = """
        Entrez l'Id du tournoi
        Format attendu : "name-date"
        """
        tournament_id = input(label)

        return tournament_id

    def prompt_for_ranking_update(self):
        """Ask for the new ranking of a player.

        Returns:
            ranking (int): new ranking

        """

        ranking = input("\nNouveau ranking: ")

        return ranking

    def display_report(self, elements):
        print("\n")
        for element in elements:
            print(element)
        print("\n")
