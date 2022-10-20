"""Base view."""


class ManagerView:
    """Manager view."""

    def prompt_for_choice(self):
        tournament = {
            "1": {'description': "Créer un nouveau tournoi", 'on_choice': "A"},
            "2": {'description': "Reprendre un tournoi", 'on_choice': "B"},
            "3": {'description': "Supprimer un tournoi", 'on_choice': "C"},
            "4": {'description': "Mettre à jour le classement des joueurs", 'on_choice': "D"}
        }

        round = {
            "1": {'description': "Créer un tour", 'on_choice': "E"},
            "2": {'description': "Modifier un tour", 'on_choice': "F"},
            "3": {'description': "Supprimer un tour", 'on_choice': "G"}
        }

        match = {
            "1": {'description': "Générer les paires d'un tour", 'on_choice': "H"},
            "2": {'description': "Assigner les scores des matchs d'un tour", 'on_choice': "I"},
            "3": {'description': "Modifier les scores des matchs d'un tour", 'on_choice': "J"}
        }

        player = {
            "1": {'description': "Sélectionner des joueurs", 'on_choice': "K"},
            "2": {'description': "Créer de nouveaux joueurs", 'on_choice': "L"},
            "3": {'description': "Modifier le classement d'un joueur", 'on_choice': "M"}
        }

        report = {
            "1": {'description': "Afficher la liste des joueurs par ordre alphabétique", 'on_choice': "N"},
            "2": {'description': "Afficher la liste des joueurs par classement", 'on_choice': "O"},
            "3": {'description': "Afficher la liste des joueurs d'un tournoi par ordre alphabétique", 'on_choice': "P"},
            "4": {'description': "Afficher la liste des joueurs d'un tournoi par ordre classement", 'on_choice': "R"},
            "5": {'description': "Afficher la liste des tournois", 'on_choice': "S"},
            "6": {'description': "Afficher la liste de tous les tours d'un tournoi", 'on_choice': "T"},
            "7": {'description': "Afficher la liste de tous les matchs d'un tournoi", 'on_choice': "U"}
        }

        home = {
            "1": {'description': "Gérer les tournois", 'on_choice': tournament},
            "2": {'description': "Gérer les rounds", 'on_choice': round},
            "3": {'description': "Gérer les matchs", 'on_choice': match},
            "4": {'description': "Gérer les joueurs", 'on_choice': player},
            "5": {'description': "Afficher les rapports", 'on_choice': report}
        }

        main = home

        while True:
            if len(main) == 1:
                break
            else:
                for element in main:
                    print(f"Choice [{element}] - {main[element]['description']}")

                choice = input("Entrez un choix valide ou la lettre Q pour quitter l'application: ")

                if choice == 'Q':
                    main = 'Q'
                    break
                elif choice in main:
                    main = main[choice]['on_choice']
                else:
                    print("Le choix n'est pas valide.")
        return main

    @property
    def prompt_to_create_tournament(self):
        """Prompt for a name, a place and a date. """

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
        """Prompt for the last_name, the first_name, the date of birth, the sexe and the ranking of a player. """

        player_informations = []
        last_name = input("Nom du joueur: ")
        first_name = input("Prénom du joueur: ")
        birth_date = input("Date de naissance:  ")
        sexe = input("Sexe: ")
        ranking = input("Classement: ")
        player_informations.append(last_name)
        print(last_name)
        player_informations.append(first_name)
        player_informations.append(birth_date)
        player_informations.append(sexe)
        player_informations.append(ranking)
        return player_informations

    def prompt_for_number_players_to_create(self):

        number_players = input(f"Nombre de joueurs à créer: ")

        return number_players

    def prompt_for_match_result(self, match):
        """Ask for a match result. """

        result = input(
            f"Choississez le résultat du match entre {match.match_stored[0][0]} et {match.match_stored[1][0]}.\n"
            f"Si {match.match_stored[0][0]} est le vainqueur, tapez 1\n"
            f"Si {match.match_stored[1][0]} est le vainqueur, tapez 2\n"
            f"Si match nul, tapez n\n"
            f"résultat: ")
        return result

    def prompt_for_one_player_ranking_update(self):
        """Ask for an update of each player ranking. """

        id_player = input("Id du joueur: ")
        ranking = input(f"Nouveau ranking: ")
        return int(id_player), int(ranking)

    def prompt_for_update_ranking(self, player):

        ranking = input(f"Nouveau ranking de {str(player)}")

        return ranking

    def prompt_to_select_one_tournament(self):

        id_tournament = input(f"Id du tournoi: ")
        return id_tournament

    def prompt_to_select_players(self):

        ids_player = input("Id des joueurs au format suivant id1,id2,id3,etc : ")

        return ids_player
