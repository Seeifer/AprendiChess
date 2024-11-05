import pygame
import chess

# Initialize Pygame and set up screen
pygame.init()
screen = pygame.display.set_mode((640, 640))  # 8x8 board, each square is 80x80

# Colors
WHITE = (208, 240, 192)
BLACK = (0, 128, 0)
SELECTED_COLOR = (255, 215, 0)  # Amarillo para la casilla seleccionada
MOVE_COLOR = (173, 216, 230)  # Azul claro para movimientos válidos
CAPTURE_COLOR = (255, 0, 0)  # Rojo para movimientos que capturan


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


def highlight_moves(selected_square):
    """Resalta los movimientos válidos para la pieza seleccionada con un fondo semitransparente."""
    if selected_square is None:
        return

    # Resaltar la casilla de la pieza seleccionada
    x, y = chess.square_file(selected_square), chess.square_rank(selected_square)
    # Dibujar el marco de la casilla seleccionada
    pygame.draw.rect(screen, SELECTED_COLOR, pygame.Rect(x * 80, (7 - y) * 80, 80, 80), 5)

    # Resaltar la casilla de la pieza seleccionada con un color semitransparente
    highlight_surface = pygame.Surface((80, 80))  # Crear una nueva superficie
    highlight_surface.fill(SELECTED_COLOR)  # Llenar la superficie con el color seleccionado
    highlight_surface.set_alpha(128)  # Establecer la transparencia (0-255, donde 255 es opaco)
    screen.blit(highlight_surface, (x * 80, (7 - y) * 80))  # Dibujar la superficie

    # Obtener movimientos legales para la pieza seleccionada
    for move in board.legal_moves:
        if move.from_square == selected_square:
            target_square = move.to_square
            x, y = chess.square_file(target_square), chess.square_rank(target_square)

            # Determinar si el movimiento es una captura
            if board.piece_at(target_square):
                pygame.draw.rect(screen, CAPTURE_COLOR, pygame.Rect(x * 80, (7 - y) * 80, 80, 80), 5)
                # Resaltar la casilla de la captura con un color semitransparente
                capture_surface = pygame.Surface((80, 80))  # Crear superficie para la captura
                capture_surface.fill(CAPTURE_COLOR)  # Llenar con el color de captura
                capture_surface.set_alpha(128)  # Transparente
                screen.blit(capture_surface, (x * 80, (7 - y) * 80))  # Dibujar la superficie de captura
            else:
                pygame.draw.rect(screen, MOVE_COLOR, pygame.Rect(x * 80, (7 - y) * 80, 80, 80), 5)
                # Resaltar la casilla de movimiento con un color semitransparente
                move_surface = pygame.Surface((80, 80))  # Crear superficie para el movimiento
                move_surface.fill(MOVE_COLOR)  # Llenar con el color de movimiento
                move_surface.set_alpha(128)  # Transparente
                screen.blit(move_surface, (x * 80, (7 - y) * 80))  # Dibujar la superficie de movimiento

def show_message(message):
    """Muestra un mensaje en la pantalla."""
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(320, 320))  # Centrar el texto en la pantalla
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Espera 2 segundos para mostrar el mensaje



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
                # Seleccionar una pieza
                if board.piece_at(square):
                    selected_square = square
            else:
                # Intentar mover la pieza seleccionada
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                    # Comprobar si el movimiento genera jaque o jaque mate
                    if board.is_check():
                        if board.is_checkmate():
                            show_message("¡Jaque Mate!")
                        else:
                            show_message("¡Jaque!")
                selected_square = None

    draw_board()
    highlight_moves(selected_square)
    draw_pieces()
    pygame.display.flip()

pygame.quit()
