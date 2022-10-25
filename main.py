"""Module to define the entry point."""

from controllers.base import Controller
from views.manager import ManagerView


def main():
    """Launch a game by generating a manager view and a controller. """
    manager_view = ManagerView()
    game = Controller(manager_view)
    game.run()


if __name__ == "__main__":
    main()


