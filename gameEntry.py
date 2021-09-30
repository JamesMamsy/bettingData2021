class gameEntry:

    def _init_ (self, teamA, teamB, finalScore):
        self.teamA = teamA
        self.teamB = teamB
        self.finalScore = finalScore

    def _init_ (self):
        self.teamA = None
        self.teamB = None
        self.finalScore = None

    def setFinalScore(self, scoreA, scoreB):
        self.finalScore = scoreA + scoreB
