from models.match import Match


class Round:
    """Round"""

    def __init__(self, name, start_date=None, start_hour=None, end_date=None, end_hour=None, matchs=None):
        """Initialize a round. """

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
        return f"Nom du round: {self.name}\n" \
               f"Début: {self.start_date} {self.start_hour}\n" \
               f"Fin: {self.end_date} {self.end_hour}"

    def serialize_round(self):
        serialized_matchs = {}

        for match in self.matchs:
            index = self.matchs.index(match)
            key = index + 1
            serialized_matchs[key] = match.serialize_match()

        serialized_round = {
            'name': self.name,
            'start_date': self.start_date,
            'start_hour': self.start_hour,
            'end_date': self.end_date,
            'end_hour': self.end_hour,
            'matchs': serialized_matchs
        }

        return serialized_round
