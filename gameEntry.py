from datetime import datetime
class gameEntry:

    # 0- Date 1- Time (Not Needed) 2-Team1 3-Score1 4-Team2 5-Score2 
    def __init__(self, array):
        self.gameInfo = array
        self.gameDate = datetime.strptime((self.gameInfo[0])[5:], "%b %d, %Y")
        self.teamA = self.gameInfo[2]
        self.teamB = self.gameInfo[4]
        self.score1 = self.gameInfo[3]
        self.score2 = self.gameInfo[5]
    
    def _init_(self):
        self.gameInfo = None
        self.gameDate = None
        self.score1= None
        self.score2 = None
        self.teamA = None
        self.teamB = None
     
    def printDate(self):
        return self.gameDate.strftime("%Y-%m-%d")

    