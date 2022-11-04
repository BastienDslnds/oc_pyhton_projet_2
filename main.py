"""Module to define the entry point."""

from controllers.controllers import ApplicationController


def main():
    game = ApplicationController()
    game.start()


if __name__ == "__main__":
    main()
