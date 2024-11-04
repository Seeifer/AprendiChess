import pygame
import chess

# Initialize Pygame and set up screen
pygame.init()
screen = pygame.display.set_mode((640, 640))  # 8x8 board, each square is 80x80

# Colors
WHITE = (208, 240, 192)
BLACK = (0, 128, 0)
HIGHLIGHT = (173, 216, 230)  # Light blue for highlighting selected piece

# Load images
# Cargar y redimensionar imágenes
piece_images = {}
piece_types = ['p', 'r', 'n', 'b', 'q', 'k']
for color in ['w', 'b']:
    for piece in piece_types:
        image_path = f'C:/Users/sammh/PycharmProjects/AprendiChess/img/{color}{piece}.png'
        piece_image = pygame.image.load(image_path)
        piece_images[color + piece] = pygame.transform.scale(piece_image, (80, 80))


# Initialize chess board
board = chess.Board()

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * 80, row * 80, 80, 80))

def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Convertir la pieza a minúsculas para que coincida con las claves en piece_images
            piece_key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()
            x, y = chess.square_file(square), chess.square_rank(square)
            screen.blit(piece_images[piece_key], (x * 80, (7 - y) * 80))


# Main game loop
running = True
selected_square = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0] // 80, event.pos[1] // 80
            square = chess.square(x, 7 - y)
            if selected_square is None:
                if board.piece_at(square):
                    selected_square = square
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None

    draw_board()
    draw_pieces()
    pygame.display.flip()

pygame.quit()
