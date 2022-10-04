"""Entry point."""

from controllers.base import Controller

from models.tournament import Tournament
from models.player import Player

from views.player import PlayerView


def main():
    """game = Controller()
    game.run()"""


if __name__ == "__main__":
    """main()"""
    active_view = PlayerView()

    game = Controller(active_view)

    tournament = Tournament("Tournoi initial", "Paris", "22/09/2022")

    joueur_un = Player("Bastien", "Deslandes", "10/11/1995", "M", 1)
    tournament.players.append(joueur_un)
    joueur_deux = Player("Sam", "Idilbi", "15/06/1995", "M", 4)
    tournament.players.append(joueur_deux)
    joueur_trois = Player("Pierre", "Leparoux", "10/11/1995", "M", 5)
    tournament.players.append(joueur_trois)
    joueur_quatre = Player("Hugo", "Crosnier", "10/11/1995", "M", 2)
    tournament.players.append(joueur_quatre)
    joueur_cinq = Player("Camille", "Guillaume", "10/11/1995", "M", 3)
    tournament.players.append(joueur_cinq)
    joueur_six = Player("Ambroise", "Leporcher", "10/11/1995", "M", 8)
    tournament.players.append(joueur_six)
    joueur_sept = Player("Hugo", "Perrin", "10/11/1995", "M", 6)
    tournament.players.append(joueur_sept)
    joueur_huit = Player("Jean", "Coquet", "10/11/1995", "M", 7)
    tournament.players.append(joueur_huit)

    for tour in range(int(tournament.nb_rounds)):  # boucle pour gérer les 4 tours du tournoi
        game.open_round(tournament)
        game.get_matchs_pairs(tournament, tournament.rounds[tour])  # Créer les paires de chaque match du tour
        game.get_matchs_results(tournament.rounds[tour])  # Récupérer les résultats de chaque match
        game.close_round(tournament.rounds[tour])  # Fermer le tour

