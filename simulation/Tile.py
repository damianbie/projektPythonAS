import pygame

class Tile:
    AIR     = 1
    WALL    = 2
    START   = 3
    END     = 4
    PATH    = 5

    def __init__(self, _type, p) -> None:
        self.type = _type
        self.x, self.y = self.pos = p

    def getCords(self):
        return (self.x, self.y)

    def draw(self, _wnd, tileSize = (20, 20), offset = (0, 0)):
        color = (127, 127, 127)
        if self.type == self.AIR:
            color = (255, 0, 0)
        elif self.type == self.WALL:
            color = (54, 54, 54)
        elif self.type == self.START:
            color = (0, 0, 255)
        elif self.type == self.END:
            color = (255, 0, 0)
        elif self.type == self.PATH:
            color = (127, 127, 0)

        pygame.draw.rect(_wnd, 
                        color,  
                        ((self.x*tileSize[0]) + offset[0], (self.y*tileSize[1]) + offset[1], 
                        tileSize[0], tileSize[1]))

    def getType(self):
        return self.type