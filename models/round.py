from models.match import Match


class Round:
    """Round"""

    def __init__(self, name):
        """Initialize a round. """

        self.name = name
        self.matchs = []
        self.start_date = None
        self.start_hour = None
        self.end_date = None
        self.end_hour = None

    def __str__(self):
        return f"{self.name}"

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
