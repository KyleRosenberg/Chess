from Constants.Colors import *
from Constants.Numbers import *
from Sprites.Sprite import *

def isPieceInDanger(board, piece, pos, testPos=None): #Piece = the piece you are moving, pos = pos moving to, testPos = pos testing for danger
    if testPos is None:
        testPos = pos
    enemies = board.blackPieces if piece.color == "w" else board.whitePieces
    caps = []
    gridX, gridY = piece.getGridPos()
    moveX, moveY = pos[0], pos[1]
    oldPiece = board.grid[moveX][moveY].getPiece()
    board.grid[gridX][gridY].setPiece()
    board.grid[moveX][moveY].setPiece(piece)
    for e in enemies:
        if e is not oldPiece:
            if not isinstance(e, King):
                x, y = e.getGridPos()
                if isinstance(e, Pawn):
                    caps += e.getCaptures(board, board.grid, x, y)
                else:
                    m, c, s = e.getMoves(board, board.grid, x, y, False)
                    caps += c
                    caps += m
    board.grid[gridX][gridY].setPiece(piece)
    board.grid[moveX][moveY].setPiece(oldPiece)
    for c in caps:
        if testPos[0] == c[0] and testPos[1] == c[1]:
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

    def getMoves(self, board, grid, x, y, checkCheck=True):
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

    def getMoves(self, board, grid, x, y, checkCheck=True):
        offset = -1 if self.color == "w" else 1
        moves = []
        captures = []
        if y+offset in range(8):
            if grid[x][y+offset].getPiece() is None:
                if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (x, y+offset), board.getKingPos(self.color))):
                    moves.append((x, y+offset))
            if y==(6 if self.color == "w" else 1):
                if grid[x][y+offset*2].getPiece() is None:
                    if not checkCheck or (
                        checkCheck and not isPieceInDanger(board, self, (x, y+offset*2), board.getKingPos(self.color))):
                        moves.append((x, y+offset*2))
            if x+1 in range(8):
                if grid[x+1][y+offset].getPiece() is not None:
                    if grid[x+1][y+offset].getPiece().color != self.color:
                        if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (x+1, y+offset), board.getKingPos(self.color))):
                            captures.append((x+1, y+offset))
            if x-1 in range(8):
                if grid[x-1][y+offset].getPiece() is not None:
                    if grid[x-1][y+offset].getPiece().color != self.color:
                        if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (x-1, y+offset), board.getKingPos(self.color))):
                            captures.append((x-1, y+offset))
        return moves, captures, None

class Rook(Piece):

    def __init__(self, color, x, y):
        filename = color + "rook"
        Piece.__init__(self, color, x, y, filename)

    def getMoves(self: Piece, board, grid, x, y, checkCheck=True):
        moves = []
        captures = []
        nx, ny = x, y
        while nx - 1 in range(8):
            nx -= 1
            if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (nx, y), board.getKingPos(self.color))):
                if grid[nx][y].getPiece() is None:
                    moves.append((nx, y))
                else:
                    if grid[nx][y].getPiece().color != self.color:
                        captures.append((nx, y))
                    nx = 9
        nx = x
        while nx + 1 in range(8):
            nx += 1
            if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (nx, y), board.getKingPos(self.color))):
                if grid[nx][y].getPiece() is None:
                    moves.append((nx, y))
                else:
                    if grid[nx][y].getPiece().color != self.color:
                        captures.append((nx, y))
                    nx = -2
        while ny - 1 in range(8):
            ny -= 1
            if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (x, ny), board.getKingPos(self.color))):
                if grid[x][ny].getPiece() is None:
                    moves.append((x, ny))
                else:
                    if grid[x][ny].getPiece().color != self.color:
                        captures.append((x, ny))
                    ny = 9
        ny = y
        while ny + 1 in range(8):
            ny += 1
            if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (x, ny), board.getKingPos(self.color))):
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

    def getMoves(self, board, grid, x, y, checkCheck=True):
        moves = []
        captures = []
        movepattern = [(x + 1, y + 2), (x - 1, y + 2), (x + 1, y - 2), (x - 1, y - 2), (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1)]
        for mp in movepattern:
            if mp[0] in range(8) and mp[1] in range(8):
                if not checkCheck or (
                    checkCheck and not isPieceInDanger(board, self, mp, board.getKingPos(self.color))):
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

    def getMoves(self: Piece, board, grid, x, y, checkCheck=True):
        moves = []
        captures = []
        nx, ny = x, y
        while nx - 1 in range(8) and ny - 1 in range(8):
            nx -= 1
            ny -= 1
            if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (nx, ny), board.getKingPos(self.color))):
                if grid[nx][ny].getPiece() is None:
                    moves.append((nx, ny))
                else:
                    if grid[nx][ny].getPiece().color != self.color:
                        captures.append((nx, ny))
                    nx = 9
                    ny = 9
        nx, ny = x, y
        while nx + 1 in range(8) and ny - 1 in range(8):
            nx += 1
            ny -= 1
            if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (nx, ny), board.getKingPos(self.color))):
                if grid[nx][ny].getPiece() is None:
                    moves.append((nx, ny))
                else:
                    if grid[nx][ny].getPiece().color != self.color:
                        captures.append((nx, ny))
                    nx = -2
                    ny = 9
        nx, ny = x, y
        while nx + 1 in range(8) and ny + 1 in range(8):
            nx += 1
            ny += 1
            if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (nx, ny), board.getKingPos(self.color))):
                if grid[nx][ny].getPiece() is None:
                    moves.append((nx, ny))
                else:
                    if grid[nx][ny].getPiece().color != self.color:
                        captures.append((nx, ny))
                    nx = -2
                    ny = -2
        nx, ny = x, y
        while nx - 1 in range(8) and ny + 1 in range(8):
            nx -= 1
            ny += 1
            if not checkCheck or (checkCheck and not isPieceInDanger(board, self, (nx, ny), board.getKingPos(self.color))):
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

    def getMoves(self, board, grid, x, y, checkCheck=True):
        moves, captures, s = Bishop.getMoves(self, board, grid, x, y, checkCheck)
        moves2, captures2, s = Rook.getMoves(self, board, grid, x, y, checkCheck)
        return moves + moves2, captures + captures2, None

class King(Piece):

    def __init__(self, color, x, y):
        filename = color + "king"
        Piece.__init__(self, color, x, y, filename)

    def getMoves(self, board, grid, x, y, checkCheck=True):
        moves = []
        captures = []
        special = []
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if not (nx == x and ny == y) and nx in range(8) and ny in range(8):
                    if (checkCheck and not isPieceInDanger(board, self, (nx, ny), (nx, ny))) or not checkCheck:
                        if grid[nx][ny].getPiece() is None:
                            moves.append((nx, ny))
                        else:
                            if grid[nx][ny].getPiece().color != self.color:
                                captures.append((nx, ny))
        if not self.hasMoved:
            if grid[0][y].getPiece() is not None and not grid[0][y].getPiece().hasMoved:
                if grid[1][y].getPiece() is None and \
                grid[2][y].getPiece() is None and not isPieceInDanger(board, self, (2, y), (2, y)) and \
                grid[3][y].getPiece() is None and not isPieceInDanger(board, self, (3, y), (3, y)):
                    if not isPieceInDanger(board, self, (x, y)) and not isPieceInDanger(board, grid[0][y].getPiece(), (0, y)):
                        special.append((0, y))
            if grid[7][y].getPiece() is not None and not grid[7][y].getPiece().hasMoved:
                if grid[6][y].getPiece() is None and not isPieceInDanger(board, self, (6, y), (6, y)) and \
                grid[5][y].getPiece() is None and not isPieceInDanger(board, self, (5, y), (5, y)):
                    if not isPieceInDanger(board, self, (x, y)) and not isPieceInDanger(board, grid[7][y].getPiece(), (7, y)):
                        special.append((7, y))
        return moves, captures, special
