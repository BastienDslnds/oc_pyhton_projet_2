"""Base view."""


class ManagerView:
    """Manager view."""

    def prompt_for_choice(self):
        tournament = {
            "1": {'description': "Créer un nouveau tournoi", 'on_choice': "A"},
            "2": {'description': "Reprendre un tournoi", 'on_choice': "B"},
            "3": {'description': "Supprimer un tournoi", 'on_choice': "B"},
        }

        round = {
            "1": {'description': "Créer un tour", 'on_choice': "D"},
            "1": {'description': "Modifier un tour", 'on_choice': "D"},
            "1": {'description': "Supprimer un tour", 'on_choice': "D"}
        }

        match = {
            "1": {'description': "Générer les paires d'un tour", 'on_choice': "D"},
            "1": {'description': "Assigner les scores des matchs d'un tour", 'on_choice': "D"},
            "1": {'description': "Modifier les scores des matchs d'un tour", 'on_choice': "D"}
        }

        player = {
            "1": {'description': "Sélectionner des joueurs", 'on_choice': "E"},
            "2": {'description': "Créer de nouveaux joueurs", 'on_choice': "F"},
            "3": {'description': "Modifier le classement d'un joueur", 'on_choice': "G"}
        }

        report = {
            "1": {'description': "Afficher la liste des joueurs par ordre alphabétique", 'on_choice': "H"},
            "2": {'description': "Afficher la liste des joueurs par classement", 'on_choice': "I"},
            "3": {'description': "Afficher la liste des joueurs d'un tournoi par ordre alphabétique", 'on_choice': "J"},
            "4": {'description': "Afficher la liste des joueurs d'un tournoi par ordre classement", 'on_choice': "K"},
            "5": {'description': "Afficher la liste des tournois", 'on_choice': "L"},
            "6": {'description': "Afficher la liste de tous les tours d'un tournoi", 'on_choice': "M"},
            "7": {'description': "Afficher la liste de tous les matchs d'un tournoi", 'on_choice': "N"}
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
    def prompt_for_tournament(self):
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
    def prompt_for_player(self):
        """Prompt for the last_name, the first_name, the date of birth, the sexe and the ranking of a player. """

        player_informations = []
        last_name = input("Nom du joueur: ")
        first_name = input("Prénom du joueur: ")
        birth_date = input("Date de naissance:  ")
        sexe = input("Sexe: ")
        ranking = input("Classement: ")
        player_informations.append(last_name)
        player_informations.append(first_name)
        player_informations.append(birth_date)
        player_informations.append(sexe)
        player_informations.append(ranking)
        return player_informations

    def prompt_for_match_result(self, match):
        """Ask for a match result. """

        result = input(
            f"Choississez le résultat du match entre {match.pair[0]} et {match.pair[1]}.\n"
            f"Si {match.pair[0]} est le vainqueur, tapez 1\n"
            f"Si {match.pair[1]} est le vainqueur, tapez 2\n"
            f"Si match nul, tapez n\n"
            f"résultat: ")
        return result

    def prompt_for_ranking_update(self, player):
        """Ask for an update of each player ranking. """

        ranking = input(f"Rang de {player.name}: ")
        return ranking
