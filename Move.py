# this class keeps track the move taken from player either human or agent
class Move:
    def __init__(self,pit,score):
        self.pit = pit
        self.score = score

    def getPit(self):
        return self.pit

    def getScore(self):
        return self.score

    def setScore(self,s):
        self.score = s

    def setPit(self,p):
        self.pit = p