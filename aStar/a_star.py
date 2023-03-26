from aStar.node import Node
from heapq import heappop
from heapq import heappush
import math
from simulation.Tile import Tile
class AStar:

    def __init__(self, map, maxSize):
        self.maxSize                = maxSize
        self._diagonalJump          = False
        self._diagonalCorrection    = True
        self._map                   = []
        
        for m in map:
            if m.getType() == Tile.WALL:
                self._map.append(m.getCords())

    def diagonalJump(self, jump):
        self._diagonalJump = jump

    def diagolnalCorrection(self, correction):
        self._diagonalCorrection = correction

    def _findNodeOnList(self, list, cords):
        for _n in list:
            if _n.getCords() == cords:
                return Node(cords)

        return None
        
    def heurestic(self, cCord, endCord):
        
        d =  (abs(cCord[0] - endCord[0]), abs(cCord[1] - endCord[1]))
        # return d[0] + d[1]
        
        return 10 * math.sqrt(d[0]**2 + d[1]**2 )
    
        # return 1 * (d[0] + d[1]) + (1.41 - 2) * min(d[0], d[1])

    def findPath2(self, startNode, endNode):
        # kierunki skoków
        # top right bottom left
        # top-right right-bottom bottom-left left-top
        dir = [(0, 1), (1, 0), (0, -1), (-1, 0),
               (1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        openList = []
        startNode.h = self.heurestic(startNode.getCords(), endNode.getCords())
        startNode.g = 0
        heappush(openList, startNode)
        while len(openList) != 0:
            openList.sort()
            currentNode = heappop(openList)
            
            if currentNode == endNode:
                # return path
                break
            
            normalNeighbors = [False, False, False, False]
            currentCords = currentNode.getCords()
            for (indx, _dir) in enumerate(dir):
                if indx > 3 and self._diagonalJump == False: break
                newCords = (currentCords[0] + _dir[0], currentCords[1] + _dir[1])
                
                # sprawdzenie czy pozycja jset w zakresie mapy
                if newCords[0] < 0 or newCords[1] < 0:
                    continue
                if newCords[0] >= self.maxSize[0] or newCords[1] >= self.maxSize[1]:
                    continue                
                
                # czy na tej pozycji jest sciana?
                if newCords in self._map:
                    if indx < 4: normalNeighbors[indx] = True
                    continue
                
                # sprawdzenie diagonlanych przejsc
                if self._diagonalCorrection:
                    if indx == 4: #top-right
                        if normalNeighbors[0] or normalNeighbors[1]:
                            continue
                    elif indx == 5: #right-bottom
                        if normalNeighbors[1] or normalNeighbors[2]:
                            continue
                    elif indx == 6: #bottom-left
                        if normalNeighbors[2] or normalNeighbors[3]:
                            continue
                    elif indx == 7: #left-top
                        if normalNeighbors[3] or normalNeighbors[0]:
                            continue
                
                # if indx >= 4: COST = 14.14
                # else: COST = 10
                if indx >= 4: COST = 1.41
                else: COST = 1
                
                neighborNode = self._findNodeOnList(openList, newCords)
                if neighborNode is None:
                    neighborNode = Node(newCords)
                    neighborNode.g = COST
                    neighborNode.h = self.heurestic(newCords, endNode.getCords())
                    neighborNode.parent = currentNode
                    openList.append(neighborNode)

                distance_from_curr_to_neighbor = COST
                scoreFromStartToCurrentNeighbor =  currentNode.g + distance_from_curr_to_neighbor
                if neighborNode.getScore() <= currentNode.getScore():
                    neighborNode.g = scoreFromStartToCurrentNeighbor
                    neighborNode.h = scoreFromStartToCurrentNeighbor + self.heurestic(newCords, endNode.getCords())     
                    neighborNode.parent = currentNode
        
        #odwijanie sciezki
        if currentNode == endNode:
            path = []
            while currentNode is not None:
                path.append(currentNode)
                currentNode = currentNode.getParent()
            return path
        else: # nie znaleziono ścieżki
            return []