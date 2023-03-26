import pygame

class Robot:
    color = 0, 127, 255
    def __init__(self, radius, speed = (0.2, 0.2)):
        
        self._drawRobot     = False
        self._isSimulating  = False
        
        self._speed         = speed
        self._tileSize      = (0, 0)
        self._pos           = (0, 0)
        self._radius        = radius
        self._path          = []
        
        self._currentTarget = 0
        
    def draw(self, _wnd):
        if self._drawRobot == False:
            return
        
        pygame.draw.circle(_wnd, (123, 234, 123), self._pos, self._radius)

    def startSimulation(self):
        self._isSimulating = True
        self._drawRobot = True
    def stopSimulation(self):
        self._isSimulating = False
    def showRobot(self):
        self._drawRobot = True
    def hideRobot(self):
        self._drawRobot = False
        
    def setTileSize(self, tileSize):
        self._tileSize = tileSize

    def setPath(self, path):
        self._path = path
        if len(self._path) < 1: 
            return
        
        self._currentTarget = len(path) - 1
        cords = self._path[self._currentTarget].getCords()
        self._pos = (
            cords[0] * self._tileSize[0] + 0.5 * self._tileSize[0],
            cords[1] * self._tileSize[1] + 0.5 * self._tileSize[1],
        )

    def update(self, timeStep):
        if self._isSimulating == False:
            return
        
        if self._currentTarget == -1:
            print("koniec symulacji")
            self._isSimulating = False
            return
        
        currentTargetPoint = self._path[self._currentTarget].getCords()
        currentTargetPointInPixels = (
            currentTargetPoint[0] * self._tileSize[0] + 0.5 * self._tileSize[0],
            currentTargetPoint[1] * self._tileSize[1] + 0.5 * self._tileSize[1]
        )
        tempPos = list((
            self._pos[0],
            self._pos[1],
        ))
        
        deltaPos0 = currentTargetPointInPixels[0] - self._pos[0]
        deltaPos1 = currentTargetPointInPixels[1] - self._pos[1]
        if deltaPos0 > 0:
            tempPos[0] = tempPos[0] + (currentTargetPointInPixels[0] - self._pos[0]) * self._speed[0]
        else:
            tempPos[0] = tempPos[0] - (-currentTargetPointInPixels[0] + self._pos[0]) * self._speed[0]
         
        if deltaPos1 > 0:
            tempPos[1] = tempPos[1] + (currentTargetPointInPixels[1] - self._pos[1]) * self._speed[1]
        else:
            tempPos[1] = tempPos[1] - (-currentTargetPointInPixels[1] + self._pos[1]) * self._speed[1]
        
        if abs(deltaPos0) < 0.2 and abs(deltaPos1) < 0.2:
            self._currentTarget -= 1
        
        
        self._pos = tempPos
        
        
        