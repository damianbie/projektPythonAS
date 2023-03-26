import pygame

from simulation.Tile import Tile

class Map:    
    def __init__(self):
        self.map = []
        self.size = (0, 0)
        self.tileSize = (15, 15)

    def getMap(self): return self.map
    def getTileSize(self): return self.tileSize
    def getSizeX(self): return self.size[0]
    def getSizeY(self): return self.size[0]
    def getSize(self): return self.size

    def setTileSize(self, newSize):
        self.tileSize = newSize

    def setMap(self, map, _size):
        self.map = map
        self.size = _size

    def _removeAllByType(self, type):
        for til in self.map:
            if til.type == type:
                self.map.remove(til)

    def calcFromPosToTileNum(self, pos):
        if pos[0] < 0 or pos[1] < 0: return (-1, -1)

        tileX = int(pos[0]/(self.tileSize[0]))
        tileY = int(pos[1]/(self.tileSize[1]))
        return (tileX, tileY)

    def getTile(self, num):
        for ti in self.map:
            if ti.x == num[0] and ti.y == num[1]:
                return ti
        return None

    def setWallByPos(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.tileSize[0] * self.size[0] or pos[1] > self.tileSize[1] * self.size[1]:
            return
        (tileX, tileY) = self.calcFromPosToTileNum(pos)
        for (indx, t) in enumerate(self.map):
            if tileX == t.x and tileY == t.y:
                self.map.remove(t)
                return

        newTile = Tile(Tile.WALL, (tileX, tileY))
        self.map.append(newTile)

    def _addTIle(self, num, type):
        tile = self.getTile(num)
        if tile is not None:
            self.map.remove(tile)
        tile = Tile(type, num)
        self.map.append(tile)

    def setStartPos(self, num):
        self._startCords = num
        self._removeAllByType(Tile.START)
        self._addTIle(num, Tile.START)

    def setEndPos(self, num):
        self._endCords = num
        self._removeAllByType(Tile.END)
        self._addTIle(num, Tile.END)

    def getStartCords(self): return self._startCords
    def getEndCords(self): return self._endCords

    def draw(self, _wnd):
        #draw background
        background = 228, 228, 228
        pygame.draw.rect(_wnd, 
                        background, 
                        (0, 0, 
                        self.tileSize[0] * self.size[0], 
                        self.tileSize[1] * self.size[1]))
        
        for item in self.map:
            if item.type == Tile.AIR:
                continue
            item.draw(_wnd, self.tileSize, (0, 0))
    def _findSpecialTiles(self):
        for item in self.map:
            if item.getType() == Tile.START:
                self._startCords = item.getCords()
            elif item.getType() == Tile.END:
                self._endCords = item.getCords()
    def setMapFile(self, name):
        self._mapFileName = name
    def getMapFileName(self):
        return self._mapFileName
    
    def drawPath(self, wnd, path):
         for item in path:
            if item.getCords() != self.getEndCords() and item.getCords() != self.getStartCords():
                ti = Tile(Tile.PATH, item.getCords())
                ti.draw(wnd, self.tileSize, (0, 0))