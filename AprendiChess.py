import pygame
import chess
import sys
# Initialize Pygame and set up screen
pygame.init()
screen = pygame.display.set_mode((850, 640))  # 8x8 board, each square is 80x80
chat_history = []  # Lista para almacenar los mensajes del chat
max_chat_lines = 5  # Número máximo de líneas que se mostrarán en el chat
chat_rect = pygame.Rect(600, 480, 250, 170)
# Colors
WHITE = (208, 240, 192)
BLACK = (0, 128, 0)
SELECTED_COLOR = (255, 215, 0)  # Amarillo para la casilla seleccionada
MOVE_COLOR = (173, 216, 230)  # Azul claro para movimientos válidos
CAPTURE_COLOR = (255, 0, 0)  # Rojo para movimientos que capturan
CHECK_COLOR = (255, 165, 0)
SIDEBAR_COLOR = (15, 78,17)
TURN_TEXT_COLOR = (255, 255, 255)

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
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            color = WHITE if (row + col) % 2 == 0 else BLACK

            # Resaltar casilla del rey en jaque
            if board.is_check() and piece and piece.piece_type == chess.KING and piece.color != board.turn:
                color = CHECK_COLOR  # Usa CHECK_COLOR (por ejemplo, un tono naranja) para destacar al rey en jaque

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

def show_turn():
    """Muestra el turno actual en la barra lateral."""
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Calcula el área de la barra lateral (la parte derecha de la ventana)
    sidebar_width = screen_width - 640  # Asumiendo que el tablero ocupa 640 píxeles
    pygame.draw.rect(screen, SIDEBAR_COLOR, pygame.Rect(640, 0, sidebar_width, screen_height))  # Dibujar barra lateral

    # Mostrar el turno en la barra lateral
    font = pygame.font.Font(None, 36)
    turn_text = "Turno: Blancas" if board.turn == chess.WHITE else "Turno: Negras"
    text = font.render(turn_text, True, (245, 245, 220))
    screen.blit(text, (660, 50))  # Mostrar el texto en la barra lateral


def show_message(message):
    """Muestra un mensaje en el centro de la pantalla, con saltos de línea."""
    font = pygame.font.Font(None, 64)

    # Dividir el mensaje por saltos de línea
    lines = message.split('\n')

    # Establecer una posición inicial para el texto
    y_offset = screen.get_height() // 2 - len(lines) * 24 // 2  # Ajustar verticalmente según el número de líneas

    # Renderizar y dibujar cada línea del mensaje
    for line in lines:
        text = font.render(line, True, (230, 0, 0))  # Texto en rojo
        text_rect = text.get_rect(center=(screen.get_width() // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 48  # Mover hacia abajo para la siguiente línea

    pygame.display.flip()

    pygame.time.wait(1500)




def confirm_move():
    """Muestra una ventana de confirmación para el jugador de las fichas blancas."""
    font = pygame.font.Font(None, 36)
    confirm_text = font.render("¿Confirmas el movimiento?", True, TURN_TEXT_COLOR)
    yes_text = font.render("Sí", True, TURN_TEXT_COLOR)
    no_text = font.render("No", True, TURN_TEXT_COLOR)

    # Crear una superficie para la ventana de confirmación
    confirm_surface = pygame.Surface((400, 200))
    confirm_surface.fill(SIDEBAR_COLOR)
    confirm_surface_rect = confirm_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    while True:
        screen.blit(confirm_surface, confirm_surface_rect)
        screen.blit(confirm_text, (confirm_surface_rect.x + 50, confirm_surface_rect.y + 50))
        screen.blit(yes_text, (confirm_surface_rect.x + 80, confirm_surface_rect.y + 120))
        screen.blit(no_text, (confirm_surface_rect.x + 280, confirm_surface_rect.y + 120))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Verificar si se hace clic en "Sí"
                if confirm_surface_rect.x + 80 <= mouse_x <= confirm_surface_rect.x + 130 and confirm_surface_rect.y + 120 <= mouse_y <= confirm_surface_rect.y + 150:
                    return True
                # Verificar si se hace clic en "No"
                elif confirm_surface_rect.x + 280 <= mouse_x <= confirm_surface_rect.x + 330 and confirm_surface_rect.y + 120 <= mouse_y <= confirm_surface_rect.y + 150:
                    return False




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

            # Deseleccionar o cambiar selección
            if selected_square == square:
                selected_square = None  # Deseleccionar si haces clic en la misma pieza
            elif board.piece_at(square) and board.piece_at(square).color == board.turn:
                selected_square = square  # Seleccionar si es una pieza del turno actual
            elif selected_square:
                # Intentar movimiento solo si hay una selección válida
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    if board.turn == chess.WHITE:
                        if confirm_move():
                            board.push(move)
                    else:
                        board.push(move)

                    # Verificar si hay jaque mate después del movimiento
                    if board.is_checkmate():
                        print("¡Jaque mate!")
                        show_message("¡JAQUE MATE! \n Fin del juego")
                        pygame.time.wait(2000)  # Esperar 2 segundos antes de cerrar el juego
                        pygame.quit()
                        sys.exit()  # Termina el programa
                    elif board.is_check():
                        print("¡Jaque!")
                        show_message("¡Jaque!")

                    selected_square = None  # Deseleccionar después del movimiento

    draw_board()
    highlight_moves(selected_square)
    draw_pieces()
    show_turn()
    pygame.display.flip()

pygame.quit()
