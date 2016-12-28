import pygame
import sys
from Constants.Numbers import *
from Constants.Colors import *
from Sprites.Sprite import *
from Tile import Tile
from Sprites.Piece import Pawn
from Sprites.Piece import Rook
from Sprites.Piece import Knight
from Sprites.Piece import Bishop
from Sprites.Piece import Queen
from Sprites.Piece import King
from Network.Socket import SocketClient
from Network.Socket import SocketServer

class Board:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Chess Board")
        self.background = Sprite("Sprites/chessboard.jpg")
        self.background.setSize(SIZE[0], SIZE[1])
        self.whitePieces = []
        self.blackPieces = []
        self.grid = self.initGrid()
        self.turn = "w"

    def initGrid(self):
        grid = [[None]*8 for i in range(8)]
        for x in range(8):
            for y in range(8):
                color = ORANGE if x%2==y%2 else WHITE
                if y == 6:
                    grid[x][y] = Tile(x, y, color, Pawn("w", x, y))
                    self.whitePieces.append(grid[x][y].getPiece())
                elif y==1:
                    grid[x][y] = Tile(x, y, color, Pawn("b", x, y))
                    self.blackPieces.append(grid[x][y].getPiece())
                elif y==0 or y==7:
                    type = "w" if y==7 else "b"
                    if x==0 or x==7:
                        grid[x][y] = Tile(x, y, color, Rook(type, x, y))
                    elif x==1 or x==6:
                        grid[x][y] = Tile(x, y, color, Knight(type, x, y))
                    elif x==2 or x==5:
                        grid[x][y] = Tile(x, y, color, Bishop(type, x, y))
                    elif x==3:
                        grid[x][y] = Tile(x, y, color, Queen(type, x, y))
                    elif x==4:
                        grid[x][y] = Tile(x, y, color, King(type, x, y))
                    if type == "b":
                        self.blackPieces.append(grid[x][y].getPiece())
                    else:
                        self.whitePieces.append(grid[x][y].getPiece())
                else:
                    grid[x][y] = Tile(x, y, color)
        return grid

    def movePiece(self, oldTile, newTile):
        moves, captures, special = oldTile.getPiece().getMoves(self, self.grid, oldTile.getPos()[0], oldTile.getPos()[1])
        newPos = newTile.getPos()
        oldPos = oldTile.getPos()
        if newPos in moves or newPos in captures:
            if newTile.getPiece() in self.whitePieces:
                self.whitePieces.remove(newTile.getPiece())
            elif newTile.getPiece() in self.blackPieces:
                self.blackPieces.remove(newTile.getPiece())
            newTile.setPiece(oldTile.getPiece())
            oldTile.getPiece().moved()
            oldTile.setPiece()
            self.turn = "b" if self.turn == "w" else "w"
            return True
        if special is not None:
            if newPos in special:
                if newPos[0] < oldPos[0]:
                    self.grid[oldPos[0]-2][oldPos[1]].setPiece(oldTile.getPiece())
                    self.grid[oldPos[0]-1][oldPos[1]].setPiece(newTile.getPiece())
                else:
                    self.grid[oldPos[0]+2][oldPos[1]].setPiece(oldTile.getPiece())
                    self.grid[oldPos[0]+1][oldPos[1]].setPiece(newTile.getPiece())
                oldTile.getPiece().moved()
                oldTile.setPiece()
                newTile.getPiece().moved()
                newTile.setPiece()
                self.turn = "b" if self.turn == "w" else "w"
                return True
        return False

    def draw(self):
        self.screen.fill(BLACK)
        self.background.draw(self.screen)
        for x in range(8):
            for y in range(8):
                if self.grid[x][y] is not None:
                    self.grid[x][y].draw(self.screen)
        pygame.display.flip()

def main(multi, color, socket):
    done = False
    selected_piece = None
    prevmouse = False
    b = Board()
    if multi:
        print("Connection made! Starting game...")
        if color == b.turn:
            print("Make your move!")
        else:
            print("Waiting for your opponent's move!")
    while not done:
        pos = pygame.mouse.get_pos()
        currmouse = pygame.mouse.get_pressed()[0]
        gx, gy = -1, -1
        if pos[0] > TOP_LEFT[0] and pos[0] < TOP_LEFT[0] + SPACE_SIZE*8 and pos[1] > TOP_LEFT[1] and pos[1]< TOP_LEFT[1] + SPACE_SIZE*8:
            gx, gy = int((pos[0] - TOP_LEFT[0])/SPACE_SIZE), int((pos[1] - TOP_LEFT[1])/SPACE_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if not multi or b.turn == color:
            if prevmouse == True and currmouse == False: #Mouse was clicked
                if gx > -1 and gy > -1:
                    if b.grid[gx][gy].getPiece() is not None:
                        if b.grid[gx][gy].getPiece().color == b.turn:
                            if selected_piece == b.grid[gx][gy].getPiece():
                                selected_piece = None
                                for i in range(64):
                                    if b.grid[i % 8][int(i / 8)] is not None:
                                        b.grid[i % 8][int(i / 8)].resetColor()
                            elif b.grid[gx][gy].getDrawColor() == PURPLE:
                                sx, sy = selected_piece.getGridPos()
                                if b.movePiece(b.grid[sx][sy], b.grid[gx][gy]):
                                    selected_piece = None
                                    if multi:
                                        msg = str(sx) + str(sy) + str(gx) + str(gy)
                                        print(msg)
                                        socket.send(msg)
                                        print("Waiting for your opponent's move!")
                            else:
                                for i in range(64):
                                    if b.grid[i % 8][int(i / 8)] is not None:
                                        b.grid[i % 8][int(i / 8)].resetColor()
                                selected_piece = b.grid[gx][gy].getPiece()
                                moves, captures, special = b.grid[gx][gy].getPiece().getMoves(b, b.grid, gx, gy)
                                for m in moves:
                                    b.grid[m[0]][m[1]].setDrawColor(GREEN)
                                for c in captures:
                                    b.grid[c[0]][c[1]].setDrawColor(BLUE)
                                if special is not None:
                                    for s in special:
                                        b.grid[s[0]][s[1]].setDrawColor(PURPLE)
                        elif selected_piece is not None:
                            sx, sy = selected_piece.getGridPos()
                            if b.movePiece(b.grid[sx][sy], b.grid[gx][gy]):
                                selected_piece = None
                                if multi:
                                    msg = str(sx) + str(sy) + str(gx) + str(gy)
                                    print(msg)
                                    socket.send(msg)
                                    print("Waiting for your opponent's move!")
                    elif selected_piece is not None:
                        sx, sy = selected_piece.getGridPos()
                        if b.movePiece(b.grid[sx][sy], b.grid[gx][gy]):
                            selected_piece = None
                            if multi:
                                msg = str(sx) + str(sy) + str(gx) + str(gy)
                                socket.send(msg)
                                print("Waiting for your opponent's move!")

            if selected_piece is None:
                for i in range(64):
                    if b.grid[i % 8][int(i / 8)] is not None:
                        b.grid[i % 8][int(i / 8)].resetColor()
                if gx > -1 and gy > -1:
                    if b.grid[gx][gy].getPiece() is not None:
                        if b.grid[gx][gy].getPiece().color == b.turn:
                            moves, captures, special = b.grid[gx][gy].getPiece().getMoves(b, b.grid, gx, gy)
                            for m in moves:
                                b.grid[m[0]][m[1]].setDrawColor(GREEN)
                            for c in captures:
                                b.grid[c[0]][c[1]].setDrawColor(BLUE)
                            if special is not None:
                                for s in special:
                                    b.grid[s[0]][s[1]].setDrawColor(PURPLE)
        elif multi:
            b.draw()
            msg = socket.receive()
            print(msg)
            sx = int(msg[0])
            sy = int(msg[1])
            gx = int(msg[2])
            gy = int(msg[3])
            b.movePiece(b.grid[sx][sy], b.grid[gx][gy])
            print("Make your move!")

        #check check
        caps = []
        for p in b.whitePieces:
            pos = p.getGridPos()
            m, c, s = p.getMoves(b, b.grid, pos[0], pos[1])
            caps += c
        for p in b.blackPieces:
            pos = p.getGridPos()
            m, c, s = p.getMoves(b, b.grid, pos[0], pos[1])
            caps += c
        if len(caps)>0:
            for c in caps:
                if isinstance(b.grid[c[0]][c[1]].getPiece(), King):
                    b.grid[c[0]][c[1]].setDrawColor(RED)


        b.draw()
        prevmouse = currmouse

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == "join":
            try:
                add = sys.argv[2]
                port = sys.argv[3]
                print("Connecting to server...")
                s = SocketClient(add, port)
                main(True, "b", s)
            except:
                print("There was an error.")
                quit()
        elif sys.argv[1] == "host":
            try:
                port = sys.argv[2]
                print("Waiting for client connection...")
                s = SocketServer(port)
                main(True, "w", s)
            except:
                print("There was an error.")
                quit()
        else:
            print("There was an error.")
            quit()

    else:
        main(False, "na", None)