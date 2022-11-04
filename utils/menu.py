class MenuEntry:

    def __init__(self, option, handler) -> None:
        self.option = option
        self.handler = handler

    def __repr__(self) -> str:
        """Permet de donner une représentation textuelle d'un objet. """
        return str(self.option)


class Menu:

    def __init__(self) -> None:
        self.entries = {}
        self.auto_key = 1

    def add(self, key, option, handler):
        if key == "auto":
            key = str(self.auto_key)
            self.auto_key += 1

        self.entries[key] = MenuEntry(option, handler)


