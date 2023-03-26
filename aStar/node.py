
class Node:
    def __init__(self, cords, g = 10, h = 10):
        self.pos = cords
        # self.cost = cost
        self.parent = None
        self.g = g
        self.h = h
    
    def __eq__(self, other):
        if self.pos == other.pos:
            return True
        else:
            return False
    def setParent(self, par):
        self.parent = par
    def getCords(self):
        return self.pos
    def getParent(self):
        return self.parent
    
    def getScore(self):
        return self.g + self.h
        
    def __str__(self):
        return f"{self.pos} Score->{self.getScore()}"
    
    def __ge__(self, other):
        return (self.g + self.h) > (other.g + other.h)
    def __lt__(self, other):
        return self.g + self.h < other.g + other.h