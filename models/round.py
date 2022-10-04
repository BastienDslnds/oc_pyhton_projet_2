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
