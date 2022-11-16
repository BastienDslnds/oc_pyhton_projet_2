class Round:
    """Round"""

    def __init__(self, name, start_date, end_date=None, matchs=None):
        """Initialize a round.

        Args:
            name (str): name of the round
            round_id (str): id of the round
            start_date (str): start date of the round
            end_date (str): end date of the round
            matchs[match]: list of round matchs
        """

        self.round_id = name + start_date
        if matchs is None:
            self.matchs = []
        else:
            self.matchs = matchs
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        """Display a round with the following format.

        Returns:
            str: rounds description

        """

        return f"{self.name}\n" \
               f"Début: {self.start_date}\n" \
               f"Fin: {self.end_date}\n"

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
            'end_date': self.end_date,
            'matchs': serialized_matchs
        }

        return serialized_round
