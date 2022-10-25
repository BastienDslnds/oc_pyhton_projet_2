from random import *


class Round:
    """Round"""

    def __init__(self, name,
                 round_id=None, start_date=None, start_hour=None, end_date=None, end_hour=None, matchs=None):
        """Initialize a round.

        Args:
            name (str): name of the round
            round_id (str): id of the round
            start_date (str): start date of the round
            start_hour (str): start hour of the round
            end_date (str): end date of the round
            end_hour (str): end hour of the round
            matchs[match]: list of round matchs

        """

        if round_id is None:
            self.round_id = randint(0, 100)
        else:
            self.round_id = round_id
        if matchs is None:
            self.matchs = []
        else:
            self.matchs = matchs
        self.name = name
        self.start_date = start_date
        self.start_hour = start_hour
        self.end_date = end_date
        self.end_hour = end_hour

    def __str__(self):
        """Display a round with the following format.

        Returns:
            str: rounds description

        """

        return f"Nom du round: {self.name}\n" \
               f"Début: {self.start_date} {self.start_hour}\n" \
               f"Fin: {self.end_date} {self.end_hour}"

    def serialize_round(self):
        """Serialize a round in order to add it in the database.

        Returns:
            serialized_round (dict): round serialized

        """

        serialized_matchs = {}

        for match in self.matchs:
            index = self.matchs.index(match)
            key = index + 1
            serialized_matchs[key] = match.serialize_match()

        serialized_round = {
            'round_id': self.round_id,
            'name': self.name,
            'start_date': self.start_date,
            'start_hour': self.start_hour,
            'end_date': self.end_date,
            'end_hour': self.end_hour,
            'matchs': serialized_matchs
        }

        return serialized_round
