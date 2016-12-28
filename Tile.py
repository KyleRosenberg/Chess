from Constants.Numbers import *

class Tile:

    def __init__(self, x, y, color, piece=None):
        self.color = color
        self.drawcolor = color
        self.piece = piece
        self.x = x
        self.y = y

    def getPiece(self):
        return self.piece

    def setPiece(self, piece=None):
        self.piece = piece
        if piece is not None:
            self.piece.setPos(self.x, self.y)

    def getPos(self):
        return (self.x, self.y)

    def resetColor(self):
        self.drawcolor = self.color

    def setDrawColor(self, color):
        self.drawcolor = color

    def getDrawColor(self):
        return self.drawcolor

    def draw(self, screen):
        pygame.draw.rect(screen, self.drawcolor, [TOP_LEFT[0] + SPACE_SIZE * self.x, TOP_LEFT[1] + SPACE_SIZE * self.y, SPACE_SIZE, SPACE_SIZE])
        if self.piece is not None:
            self.piece.draw(screen)
