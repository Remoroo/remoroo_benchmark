"""Tic-Tac-Toe game using pygame."""

import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 450, 450
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
current_player = 'X'
game_over = False
winner = None

def draw_lines():
    """Draw the game board lines."""
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    """Draw X and O on the board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, 
                               (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + 30),
                               (col * SQUARE_SIZE + SQUARE_SIZE - 30, row * SQUARE_SIZE + SQUARE_SIZE - 30),
                               15)
                pygame.draw.line(screen, RED,
                               (col * SQUARE_SIZE + SQUARE_SIZE - 30, row * SQUARE_SIZE + 30),
                               (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + SQUARE_SIZE - 30),
                               15)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE,
                                  (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                  60, 15)

def check_winner():
    """Check if there's a winner."""
    global winner, game_over
    # Check rows
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            game_over = True
            return
    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            game_over = True
            return
    # Check diagonal (top-left to bottom-right)
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        game_over = True
        return
    # Check diagonal (top-right to bottom-left)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        game_over = True
        return

def check_draw():
    """Check if the game is a draw."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def mark_square(row, col, player):
    """Mark a square with the player's symbol."""
    board[row][col] = player

def available_square(row, col):
    """Check if a square is available."""
    return board[row][col] is None

def display_winner():
    """Display the winner message."""
    font = pygame.font.Font(None, 36)
    if winner:
        text = font.render(f"Player {winner} wins!", True, BLACK)
    else:
        text = font.render("It's a draw!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, GRAY, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    screen.blit(text, text_rect)

def main():
    """Main game loop."""
    global current_player, game_over, winner
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, current_player)
                    check_winner()
                    
                    if not game_over:
                        if check_draw():
                            game_over = True
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'
        
        screen.fill(WHITE)
        draw_lines()
        draw_figures()
        
        if game_over:
            display_winner()
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
