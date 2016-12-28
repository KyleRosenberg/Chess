import pygame

SIZE = [800, 800]
TOP_LEFT = [44, 44]
SPACE_SIZE = 89

W_PAWN = pygame.Rect(0, 0, 64, 64)
B_PAWN = pygame.Rect(0, 64, 64, 64)
W_BISHOP = pygame.Rect(64, 0, 64, 64)
B_BISHOP = pygame.Rect(64, 64, 64, 64)
W_KNIGHT = pygame.Rect(128, 0, 64, 64)
B_KNIGHT = pygame.Rect(128, 64, 64, 64)
W_ROOK = pygame.Rect(192, 0, 64, 64)
B_ROOK = pygame.Rect(192, 64, 64, 64)
W_QUEEN = pygame.Rect(256, 0, 64, 64)
B_QUEEN = pygame.Rect(256, 64, 64, 64)
W_KING = pygame.Rect(320, 0, 64, 64)
B_KING = pygame.Rect(320, 64, 64, 64)

def string_to_piece(string):
    pieces = {
        "wpawn": W_PAWN,
        "wbishop": W_BISHOP,
        "wknight": W_KNIGHT,
        "wrook": W_ROOK,
        "wqueen": W_QUEEN,
        "wking": W_KING,
        "bpawn": B_PAWN,
        "bbishop": B_BISHOP,
        "bknight": B_KNIGHT,
        "brook": B_ROOK,
        "bqueen": B_QUEEN,
        "bking": B_KING
    }
    return pieces.get(string, None)