"""Base view."""


class PlayerView:
    """Player view."""

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
