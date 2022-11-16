"""Module to define the entry point."""

from controllers.controllers import ApplicationController


def main():
    """Main function to launch the application
    """

    game = ApplicationController()
    game.start()


if __name__ == "__main__":
    main()
