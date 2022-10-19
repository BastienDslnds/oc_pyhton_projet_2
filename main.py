"""Entry point."""

from controllers.base import Controller
from views.manager import ManagerView
from models.tournament import Tournament
from models.player import Player


def main():
    """game.run"""


if __name__ == "__main__":
    """main()"""

    manager_view = ManagerView()  # creation de la vue pour la saisie d'informations par le manager
    game = Controller(manager_view)  # creation du controller permettant de contrôler les étapes d'un tournoi

    game.tournament = Tournament("1", "Tournoi initial", "Paris", "22/09/2022")

    joueur_un = Player("Bastien", "Deslandes", "10/11/1995", "M", 1)
    game.tournament.players.append(joueur_un)
    joueur_deux = Player("Sam", "Idilbi", "15/06/1995", "M", 4)
    game.tournament.players.append(joueur_deux)
    joueur_trois = Player("Pierre", "Leparoux", "10/11/1995", "M", 5)
    game.tournament.players.append(joueur_trois)
    joueur_quatre = Player("Hugo", "Crosnier", "10/11/1995", "M", 2)
    game.tournament.players.append(joueur_quatre)
    joueur_cinq = Player("Camille", "Guillaume", "10/11/1995", "M", 3)
    game.tournament.players.append(joueur_cinq)
    joueur_six = Player("Ambroise", "Leporcher", "10/11/1995", "M", 8)
    game.tournament.players.append(joueur_six)
    joueur_sept = Player("Hugo", "Perrin", "10/11/1995", "M", 6)
    game.tournament.players.append(joueur_sept)
    joueur_huit = Player("Jean", "Coquet", "10/11/1995", "M", 7)
    game.tournament.players.append(joueur_huit)

    game.tournament.save_players()
    game.tournament.save_tournament()

    game.run()  # lancement d'un tournoi"""


