import pygame

class Tile:
    AIR     = 1
    WALL    = 2
    START   = 3
    END     = 4
    PATH    = 5

    def __init__(self, _type, p, fontsize=24) -> None:
        font = pygame.font.SysFont(None, fontsize)
        
        self.type = _type
        self.x, self.y = self.pos = p
        self.Simg = font.render("S", True, (0, 0, 0))
        self.Kimg = font.render("K", True, (0, 0, 0))

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
            pygame.draw.rect(_wnd, 
                        color,  
                        ((self.x*tileSize[0]) + offset[0], (self.y*tileSize[1]) + offset[1], 
                        tileSize[0], tileSize[1]))

            r = self.Simg.get_rect()
            r.top = (self.y*tileSize[1]) + offset[1]
            r.left = (self.x*tileSize[0]) + offset[0]
            _wnd.blit(self.Simg, r)
            return
        elif self.type == self.END:
            color = (255, 0, 0)
            pygame.draw.rect(_wnd, 
                        color,  
                        ((self.x*tileSize[0]) + offset[0], (self.y*tileSize[1]) + offset[1], 
                        tileSize[0], tileSize[1]))

            r = self.Simg.get_rect()
            r.top = (self.y*tileSize[1]) + offset[1]
            r.left = (self.x*tileSize[0]) + offset[0]
            _wnd.blit(self.Kimg, r)
            return
        elif self.type == self.PATH:
            color = (127, 127, 0)
        
        pygame.draw.rect(_wnd, 
                        color,  
                        ((self.x*tileSize[0]) + offset[0], (self.y*tileSize[1]) + offset[1], 
                        tileSize[0], tileSize[1]))

    def getType(self):
        return self.type