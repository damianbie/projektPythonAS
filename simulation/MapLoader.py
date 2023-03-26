import json, pygame
from simulation.Map import Map
from simulation.Tile import Tile
from simulation.robot import Robot

class MapLoader:
    def _loadFromTxt(fileName, size):
        map = []
        with open(fileName, "r") as f:
            indy = 0
            for line in f.readlines():
                indx = 0
                for ch in line:
                    if ch == " " or ch == '\n':
                        continue
          
                    elif int(ch) != Tile.AIR:
                        if indx <= size[0] and indy <= size[1]:
                            t = Tile(int(ch), (indx, indy))
                            map.append(t)
                            
                    indx = indx + 1
                indy = indy + 1
        return map


    def _loadDromBitmap(fileName, size):
        return []

    def fromJson(fileName):
        jsonFile = open(fileName, "r")
        mi = json.load(jsonFile)
        pixelsPerCm = mi["pixelsPerCm"]
        m = mi["map"]
        mapSize = (m["sizeX"], m["sizeY"])
        tileSize =  (pixelsPerCm*m["tileSizeX"], pixelsPerCm*m["tileSizeY"])
        mapType = 0
        mapFileName = ""
        try:
            mapFileName = m["txtFile"]
            mapType = 1
        except KeyError as ex:
            try:
                mapFileName = m["bmpFile"]
                mapType = 2
            except KeyError as kr:
                mapType = 0
        
        if mapType == 0:
            print("Error while parsing map file")
            raise RuntimeError()
        elif mapType == 1:
            loadedMap = MapLoader._loadFromTxt(mapFileName, mapSize)
        elif mapType == 2:
            loadedMap = MapLoader._loadDromBitmap(mapFileName, mapSize)

        finalMap = Map()
        finalMap.setMapFile(mapFileName)
        finalMap.setTileSize(tileSize)
        finalMap.setMap(loadedMap, mapSize)
        finalMap._findSpecialTiles()

        _r = mi["robot"]
        _rVel = (_r["maxSpeedX"], _r["maxSpeedY"])
        robot = Robot(_r["radius"], _rVel)
        robot.setTileSize(tileSize)

        return (finalMap, robot)


    def saveMap(fName, map):
        mapFile = open(fName, "w")
        copyMap = map
        mapSize = copyMap.getSize()
        lineToSave = ""
        mmap = copyMap.getMap()

        for i in range(0, mapSize[1]):
            for j in range(0, mapSize[0]):
                isEmpty = True
                for k in mmap:
                    if k.getCords() == (j, i):
                        lineToSave = lineToSave+(str(k.getType()))
                        mmap.remove(k)
                        isEmpty = False
                        break
                if isEmpty:
                    lineToSave = lineToSave+ str(Tile.AIR)
            mapFile.write(lineToSave + "\n")
            lineToSave = ""