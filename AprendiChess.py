import pygame
import chess
import sys

pygame.init()
screen = pygame.display.set_mode((850, 640))

# Definicion de colores
WHITE = (208, 240, 192)
BLACK = (0, 128, 0)
Elegida = (255, 215, 0)
Movimientos = (173, 216, 230)
Captura = (255, 0, 0)
Jaque = (255, 165, 0)
SIDEBAR = (15, 78,17)
TURN = (255, 255, 255)

# Cargar y redimensionar imágenes
piece_images = {}
piece_types = ['p', 'r', 'n', 'b', 'q', 'k']
for color in ['w', 'b']:
    for piece in piece_types:
        image_path = f'C:/Users/sammh/PycharmProjects/AprendiChess/img/{color}{piece}.png'
        piece_image = pygame.image.load(image_path)
        piece_images[color + piece] = pygame.transform.scale(piece_image, (80, 80))


board = chess.Board()


def draw_board():
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            color = WHITE if (row + col) % 2 == 0 else BLACK

            if board.is_check() and piece and piece.piece_type == chess.KING and piece.color != board.turn:
                color = Jaque

            pygame.draw.rect(screen, color, pygame.Rect(col * 80, row * 80, 80, 80))


def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()
            x, y = chess.square_file(square), chess.square_rank(square)
            screen.blit(piece_images[piece_key], (x * 80, (7 - y) * 80))


def highlight_moves(selected_square):
    if selected_square is None:
        return

    x, y = chess.square_file(selected_square), chess.square_rank(selected_square)
    pygame.draw.rect(screen, Elegida, pygame.Rect(x * 80, (7 - y) * 80, 80, 80), 5)

    highlight_surface = pygame.Surface((80, 80))
    highlight_surface.fill(Elegida)
    highlight_surface.set_alpha(128)
    screen.blit(highlight_surface, (x * 80, (7 - y) * 80))

    for move in board.legal_moves:
        if move.from_square == selected_square:
            target_square = move.to_square
            x, y = chess.square_file(target_square), chess.square_rank(target_square)

            if board.piece_at(target_square):
                pygame.draw.rect(screen, Captura, pygame.Rect(x * 80, (7 - y) * 80, 80, 80), 5)
                capture_surface = pygame.Surface((80, 80))
                capture_surface.fill(Captura)
                capture_surface.set_alpha(128)
                screen.blit(capture_surface, (x * 80, (7 - y) * 80))
            else:
                pygame.draw.rect(screen, Movimientos, pygame.Rect(x * 80, (7 - y) * 80, 80, 80), 5)
                move_surface = pygame.Surface((80, 80))
                move_surface.fill(Movimientos)
                move_surface.set_alpha(128)
                screen.blit(move_surface, (x * 80, (7 - y) * 80))


def show_turn():
    """Muestra el turno actual en la barra lateral."""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    sidebar_width = screen_width - 640
    pygame.draw.rect(screen, SIDEBAR, pygame.Rect(640, 0, sidebar_width, screen_height))

    font = pygame.font.Font(None, 36)
    turn_text = "Turno: WHITE" if board.turn == chess.WHITE else "Turno: BLACK"
    text = font.render(turn_text, True, (245, 245, 220))
    screen.blit(text, (660, 50))


def show_message(message):
    font = pygame.font.Font(None, 64)

    lines = message.split('\n')

    y_offset = screen.get_height() // 2 - len(lines) * 24 // 2

    for line in lines:
        text = font.render(line, True, (230, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 48

    pygame.display.flip()

    pygame.time.wait(1500)




def confirm_move():
    font = pygame.font.Font(None, 36)
    confirm_text = font.render("¿Confirmas el movimiento?", True, TURN)
    yes_text = font.render("Sí", True, TURN)
    no_text = font.render("No", True, TURN)

    confirm_surface = pygame.Surface((400, 200))
    confirm_surface.fill(SIDEBAR)
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
                if confirm_surface_rect.x + 80 <= mouse_x <= confirm_surface_rect.x + 130 and confirm_surface_rect.y + 120 <= mouse_y <= confirm_surface_rect.y + 150:
                    return True
                elif confirm_surface_rect.x + 280 <= mouse_x <= confirm_surface_rect.x + 330 and confirm_surface_rect.y + 120 <= mouse_y <= confirm_surface_rect.y + 150:
                    return False




running = True
selected_square = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0] // 80, event.pos[1] // 80
            square = chess.square(x, 7 - y)

            if selected_square == square:
                selected_square = None
            elif board.piece_at(square) and board.piece_at(square).color == board.turn:
                selected_square = square
            elif selected_square:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    if board.turn == chess.WHITE:
                        if confirm_move():
                            board.push(move)
                    else:
                        board.push(move)
                    if board.is_checkmate():
                        print("¡Jaque mate!")
                        show_message("¡JAQUE MATE! \n Fin del juego")
                        pygame.time.wait(2000)  # Esperar 2 segundos antes de cerrar el juego
                        pygame.quit()
                        sys.exit()  # Termina el programa
                    elif board.is_check():
                        print("¡Jaque!")
                        show_message("¡JAQUE!")

                    selected_square = None  # Deseleccionar después del movimiento

    draw_board()
    highlight_moves(selected_square)
    draw_pieces()
    show_turn()
    pygame.display.flip()

pygame.quit()
