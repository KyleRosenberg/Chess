from Constants.Colors import *
from Constants.Numbers import *
from Sprites.Sprite import *

def isPieceInDanger(board, piece, pos, testPos=None):
    if testPos is None:
        testPos = pos
    enemies = board.blackPieces if piece.color == "w" else board.whitePieces
    caps = []
    gridX, gridY = piece.getGridPos()
    board.grid[gridX][gridY].setPiece()
    for e in enemies:
        if not isinstance(e, King):
            x, y = e.getGridPos()
            if isinstance(e, Pawn):
                caps += e.getCaptures(board, board.grid, x, y)
            else:
                m, c, s = e.getMoves(board, board.grid, x, y)
                caps += c
                caps += m
    board.grid[gridX][gridY].setPiece(piece)
    for c in caps:
        if testPos[0] == c[0] and testPos[1] == c[1]:
            return True
    if isinstance(piece, King):
        for x in range(testPos[0]-1, testPos[0]+2):
            if x in range(8):
                for y in range(testPos[1]-1, testPos[1]+2):
                    if y in range(8):
                        if not (x == testPos[0] and y == testPos[1]):
                            p = board.grid[x][y].getPiece()
                            if p is not None:
                                if p.color != piece.color:
                                    if isinstance(p, King):
                                        return True

    return False

class Piece:

    def __init__(self, color, x, y, filename):
        self.color = color
        self.sprite = Sprite("Sprites/pieces.png", filename)
        self.sprite.setSize(SPACE_SIZE, SPACE_SIZE)
        self.sprite.setPos(TOP_LEFT[0] + SPACE_SIZE*x, TOP_LEFT[1] + SPACE_SIZE*y)
        self.hasMoved = False

    def getGridPos(self):
        x, y = self.sprite.getPos()
        if x > TOP_LEFT[0] + SPACE_SIZE*8:
            x-=SPACE_SIZE
        return int((x-TOP_LEFT[0])/SPACE_SIZE), int((y-TOP_LEFT[1])/SPACE_SIZE)

    def setPos(self, x, y):
        self.sprite.setPos(TOP_LEFT[0] + SPACE_SIZE*x, TOP_LEFT[1] + SPACE_SIZE*y)

    def getMoves(self, board, grid, x, y):
        print("Get moves")

    def getCaptures(self, board, grid, x, y):
        print("Get captures")

    def moved(self):
        self.hasMoved = True

    def hasMoved(self):
        return self.hasMoved

    def draw(self, screen):
        self.sprite.draw(screen)

class Pawn(Piece):

    def __init__(self, color, x, y):
        filename = color + "pawn"
        Piece.__init__(self, color, x, y, filename)

    def getCaptures(self, board, grid, x, y):
        offset = -1 if self.color == "w" else 1
        captures = []
        if y+offset in range(8):
            if x+1 in range(8):
                if grid[x+1][y+offset].getPiece() is None:
                    captures.append((x+1, y+offset))
            if x-1 in range(8):
                if grid[x-1][y+offset].getPiece() is None:
                    captures.append((x-1, y+offset))
        return captures

    def getMoves(self, board, grid, x, y):
        offset = -1 if self.color == "w" else 1
        moves = []
        captures = []
        if y+offset in range(8):
            if grid[x][y+offset].getPiece() is None:
                moves.append((x, y+offset))
            if y==(6 if self.color == "w" else 1):
                if grid[x][y+offset*2].getPiece() is None:
                    moves.append((x, y+offset*2))
            if x+1 in range(8):
                if grid[x+1][y+offset].getPiece() is not None:
                    if grid[x+1][y+offset].getPiece().color != self.color:
                        captures.append((x+1, y+offset))
            if x-1 in range(8):
                if grid[x-1][y+offset].getPiece() is not None:
                    if grid[x-1][y+offset].getPiece().color != self.color:
                        captures.append((x-1, y+offset))
        return moves, captures, None

class Rook(Piece):

    def __init__(self, color, x, y):
        filename = color + "rook"
        Piece.__init__(self, color, x, y, filename)

    def getMoves(self, board, grid, x, y):
        moves = []
        captures = []
        nx, ny = x, y
        while nx-1 in range(8):
            nx-=1
            if grid[nx][y].getPiece() is None:
                moves.append((nx, y))
            else:
                if grid[nx][y].getPiece().color != self.color:
                    captures.append((nx, y))
                nx = 9
        nx = x
        while nx+1 in range(8):
            nx+=1
            if grid[nx][y].getPiece() is None:
                moves.append((nx, y))
            else:
                if grid[nx][y].getPiece().color != self.color:
                    captures.append((nx, y))
                nx = -2
        while ny-1 in range(8):
            ny-=1
            if grid[x][ny].getPiece() is None:
                moves.append((x, ny))
            else:
                if grid[x][ny].getPiece().color != self.color:
                    captures.append((x, ny))
                ny = 9
        ny = y
        while ny+1 in range(8):
            ny+=1
            if grid[x][ny].getPiece() is None:
                moves.append((x, ny))
            else:
                if grid[x][ny].getPiece().color != self.color:
                    captures.append((x, ny))
                ny = -2
        return moves, captures, None

class Knight(Piece):

    def __init__(self, color, x, y):
        filename = color + "knight"
        Piece.__init__(self, color, x, y, filename)

    def getMoves(self, board, grid, x, y):
        moves = []
        captures = []
        movepattern = [(x+1, y+2), (x-1, y+2), (x+1, y-2), (x-1, y-2), (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1)]
        for mp in movepattern:
            if mp[0] in range(8) and mp[1] in range(8):
                if grid[mp[0]][mp[1]].getPiece() is None:
                    moves.append(mp)
                else:
                    if grid[mp[0]][mp[1]].getPiece().color != self.color:
                        captures.append(mp)
        return moves, captures, None

class Bishop(Piece):

    def __init__(self, color, x, y):
        filename = color + "bishop"
        Piece.__init__(self, color, x, y, filename)

    def getMoves(self, board, grid, x, y):
        moves = []
        captures = []
        nx, ny = x, y
        while nx-1 in range(8) and ny-1 in range(8):
            nx-=1
            ny-=1
            if grid[nx][ny].getPiece() is None:
                moves.append((nx, ny))
            else:
                if grid[nx][ny].getPiece().color != self.color:
                    captures.append((nx, ny))
                nx = 9
                ny = 9
        nx, ny = x, y
        while nx+1 in range(8) and ny-1 in range(8):
            nx+=1
            ny-=1
            if grid[nx][ny].getPiece() is None:
                moves.append((nx, ny))
            else:
                if grid[nx][ny].getPiece().color != self.color:
                    captures.append((nx, ny))
                nx = -2
                ny = 9
        nx, ny = x, y
        while nx+1 in range(8) and ny+1 in range(8):
            nx+=1
            ny+=1
            if grid[nx][ny].getPiece() is None:
                moves.append((nx, ny))
            else:
                if grid[nx][ny].getPiece().color != self.color:
                    captures.append((nx, ny))
                nx = -2
                ny = -2
        nx, ny = x, y
        while nx-1 in range(8) and ny+1 in range(8):
            nx-=1
            ny+=1
            if grid[nx][ny].getPiece() is None:
                moves.append((nx, ny))
            else:
                if grid[nx][ny].getPiece().color != self.color:
                    captures.append((nx, ny))
                nx = 9
                ny = -2
        return moves, captures, None

class Queen(Piece):

    def __init__(self, color, x, y):
        filename = color + "queen"
        Piece.__init__(self, color, x, y, filename)

    def getMoves(self, board, grid, x, y):
        moves, captures, s = Bishop.getMoves(self, board, grid, x, y)
        moves2, captures2, s = Rook.getMoves(self, board, grid, x, y)
        return moves + moves2, captures + captures2, None

class King(Piece):

    def __init__(self, color, x, y):
        filename = color + "king"
        Piece.__init__(self, color, x, y, filename)

    def getMoves(self, board, grid, x, y):
        moves = []
        captures = []
        special = []
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if not (nx == x and ny == y) and nx in range(8) and ny in range(8):
                    if not isPieceInDanger(board, self, (x, y), (nx, ny)):
                        if grid[nx][ny].getPiece() is None:
                            moves.append((nx, ny))
                        else:
                            if grid[nx][ny].getPiece().color != self.color:
                                captures.append((nx, ny))
        if not self.hasMoved:
            if grid[0][y].getPiece() is not None and not grid[0][y].getPiece().hasMoved:
                if grid[1][y].getPiece() is None and \
                    grid[2][y].getPiece() is None and not isPieceInDanger(board, self, (x, y), (2, y)) and \
                    grid[3][y].getPiece() is None and not isPieceInDanger(board, self, (x, y), (3, y)):
                    if not isPieceInDanger(board, self, (x, y)) and not isPieceInDanger(board, grid[0][y].getPiece(), (0, y)):
                        special.append((0, y))
            if grid[7][y].getPiece() is not None and not grid[7][y].getPiece().hasMoved:
                if grid[6][y].getPiece() is None and not isPieceInDanger(board, self, (x, y), (6, y)) and \
                    grid[5][y].getPiece() is None and not isPieceInDanger(board, self, (x, y), (5, y)):
                    if not isPieceInDanger(board, self, (x, y)) and not isPieceInDanger(board, grid[7][y].getPiece(), (7, y)):
                        special.append((7, y))
        return moves, captures, special
