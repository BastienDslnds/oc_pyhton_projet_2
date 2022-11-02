"""Module to define the entry point."""

from controllers.base import Controller
from views.manager import ManagerView


def main():
    manager_view = ManagerView()
    game = Controller(manager_view)
    game.run()


if __name__ == "__main__":
    main()
