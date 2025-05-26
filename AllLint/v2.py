"""
Gobblet Jr. game implementation using pygame.
"""
import pygame
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 615, 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gobblet Jr.")

GRID_SIZE = 300
GRID_X = (WINDOW_WIDTH - GRID_SIZE) // 2
GRID_Y = (WINDOW_HEIGHT - GRID_SIZE) // 2
CELL_SIZE = GRID_SIZE // 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 190, 255)
PINK = (255, 105, 180)
LIME     = (50, 205, 50)
PURPLE   = (128, 0, 128)

pygame.font.init()
font = pygame.font.Font(None, 36)

SMALL_RADIUS = 10
MEDIUM_RADIUS = 20
LARGE_RADIUS = 30
SPACING_X = LARGE_RADIUS * 2
SPACING_Y = LARGE_RADIUS * 1.5
LEFT_X = GRID_X - SPACING_X * 2
RIGHT_X = GRID_X + GRID_SIZE + SPACING_X * 2
ROW2_Y = WINDOW_HEIGHT - LARGE_RADIUS - 20
ROW1_Y = ROW2_Y - SPACING_Y * 1.5

def init_pieces():
    """Initializes all pieces."""
    return [
        # Blue pieces (Left side)
        {"color": BLUE, "pos": [LEFT_X, ROW1_Y], "radius": SMALL_RADIUS, "stack": []},
        {"color": BLUE, "pos": [LEFT_X + SPACING_X - 12, ROW1_Y],
            "radius": MEDIUM_RADIUS, "stack": []},
        {"color": BLUE, "pos": [LEFT_X + SPACING_X * 2, ROW1_Y],
            "radius": LARGE_RADIUS, "stack": []},
        {"color": BLUE, "pos": [LEFT_X, ROW2_Y], "radius": SMALL_RADIUS, "stack": []},
        {"color": BLUE, "pos": [LEFT_X + SPACING_X - 12, ROW2_Y],
            "radius": MEDIUM_RADIUS, "stack": []},
        {"color": BLUE, "pos": [LEFT_X + SPACING_X * 2, ROW2_Y],
            "radius": LARGE_RADIUS, "stack": []},
        # Pink pieces (Right side)
        {"color": PINK, "pos": [RIGHT_X, ROW1_Y], "radius": SMALL_RADIUS, "stack": []},
        {"color": PINK, "pos": [RIGHT_X - SPACING_X + 12, ROW1_Y],
            "radius": MEDIUM_RADIUS, "stack": []},
        {"color": PINK, "pos": [RIGHT_X - SPACING_X * 2, ROW1_Y],
            "radius": LARGE_RADIUS, "stack": []},
        {"color": PINK, "pos": [RIGHT_X, ROW2_Y], "radius": SMALL_RADIUS, "stack": []},
        {"color": PINK, "pos": [RIGHT_X - SPACING_X + 12, ROW2_Y],
            "radius": MEDIUM_RADIUS, "stack": []},
        {"color": PINK, "pos": [RIGHT_X - SPACING_X * 2, ROW2_Y],
            "radius": LARGE_RADIUS, "stack": []}
    ]

pieces = init_pieces()
selected_piece = None
turn = "BLUE"
game_over = False
winner = None

def reset_game():
    """Resets the game state."""
    global pieces, selected_piece, turn, game_over, winner
    pieces = init_pieces()
    selected_piece = None
    turn = "BLUE"
    game_over = False
    winner = None

def draw_grid():
    """Draws a 3x3 grid."""
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (GRID_X + i * CELL_SIZE, GRID_Y),
                         (GRID_X + i * CELL_SIZE, GRID_Y + GRID_SIZE), 5)
        pygame.draw.line(screen, BLACK, (GRID_X, GRID_Y + i * CELL_SIZE),
                         (GRID_X + GRID_SIZE, GRID_Y + i * CELL_SIZE), 5)
    pygame.draw.rect(screen, BLACK, (GRID_X, GRID_Y, GRID_SIZE, GRID_SIZE), 5)

def write_text():
    """Displays player names, turn."""
    text1 = font.render("Player 1", True, BLUE)
    text2 = font.render("Player 2", True, PINK)
    turn_text = font.render(f"Turn: {turn}", True, BLACK)
    screen.blit(text1, (20, 50))
    screen.blit(text2, (WINDOW_WIDTH - 110, 50))
    screen.blit(turn_text, (WINDOW_WIDTH // 2 - 50, 20))

def draw_pieces():
    """Draws all pieces and highlights the selected piece."""
    for p in pieces:
        pygame.draw.circle(screen, p["color"], p["pos"], p["radius"])
        if p == selected_piece:
            pygame.draw.circle(screen, LIME, p["pos"], p["radius"] + 3, 2)

def get_grid_cell(x, y):
    """
    Snaps a position to the nearest grid cell and returns the cell center 
    and the stack of pieces at that cell.
    """
    if GRID_X <= x <= GRID_X + GRID_SIZE and GRID_Y <= y <= GRID_Y + GRID_SIZE:
        col = (x - GRID_X) // CELL_SIZE
        row = (y - GRID_Y) // CELL_SIZE
        grid_pos = (GRID_X + col * CELL_SIZE + CELL_SIZE // 2,
                    GRID_Y + row * CELL_SIZE + CELL_SIZE // 2)
        stk = [p for p in pieces if tuple(p["pos"]) == grid_pos]
        return grid_pos, stk
    return None, []

def check_board_win():
    """
    Returns a set of winning colors if there is a win on the board,
    otherwise returns None.
    """
    board = [[None for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            cell_center = (GRID_X + col * CELL_SIZE + CELL_SIZE // 2,
                           GRID_Y + row * CELL_SIZE + CELL_SIZE // 2)
            cell_stack = [p for p in pieces if tuple(p["pos"]) == cell_center]
            if cell_stack:
                board[row][col] = cell_stack[-1]["color"]
    winners = set()
    for row in board:
        if row[0] and row[0] == row[1] == row[2]:
            winners.add(row[0])
    for col in range(3):
        if board[0][col] and board[0][col] == board[1][col] == board[2][col]:
            winners.add(board[0][col])
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        winners.add(board[0][0])
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        winners.add(board[0][2])
    return winners if winners else None

running = True
while running:
    screen.fill(WHITE)
    if game_over:
        over_font = pygame.font.Font(None, 50)
        winner_font = pygame.font.Font(None, 52)
        prompt_font = pygame.font.Font(None, 56)
        line1 = over_font.render("Game Over!", True, PURPLE)
        varx = BLUE if winner == BLUE else PINK
        line2 = winner_font.render(
            f"Winner: {'Player 1' if winner == BLUE else 'Player 2'}", True, varx)
        line3 = prompt_font.render("Press R to restart the game", True, LIME)
        total_height = line1.get_height() + line2.get_height() + line3.get_height() + 20
        start_y = WINDOW_HEIGHT // 2 - total_height // 2
        screen.blit(line1, (WINDOW_WIDTH // 2 - line1.get_width() // 2, start_y))
        screen.blit(line2, (WINDOW_WIDTH // 2 - line2.get_width() // 2,
                            start_y + line1.get_height() + 30))
        screen.blit(line3, (WINDOW_WIDTH // 2 - line3.get_width() // 2,
                            start_y + line1.get_height() + line2.get_height() + 70))
    else:
        draw_grid()
        write_text()
        draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
            continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if selected_piece is None:
                for piece in pieces:
                    px, py = piece["pos"]
                    if (mx - px) ** 2 + (my - py) ** 2 <= piece["radius"] ** 2:
                        _, stack = get_grid_cell(px, py)
                        if stack and stack[-1] != piece:
                            continue
                        if (
                            (turn == "BLUE" and piece["color"] == BLUE) or
                            (turn == "PINK" and piece["color"] == PINK)
                        ):
                            selected_piece = piece
                            piece["orig_pos"] = piece["pos"][:]
                        break
            else:
                # A piece is already selected: this tap is treated as target cell selection.
                new_pos, stack = get_grid_cell(mx, my)
                if new_pos:
                    # Enforce stacking rule: only place on an empty cell
                    # or on a piece that is smaller.
                    if stack and selected_piece["radius"] <= stack[-1]["radius"]:
                        # Invalid move: revert to original position.
                        selected_piece["pos"] = selected_piece.get(
                            "orig_pos", selected_piece["pos"])
                    else:
                        selected_piece["pos"] = list(new_pos)
                        # To mark this piece as now on top, remove and re-append it.
                        if selected_piece in pieces:
                            pieces.remove(selected_piece)
                            pieces.append(selected_piece)
                        winners = check_board_win()
                        if winners:
                            if len(winners) == 1:
                                winner = winners.pop()
                            else:
                                winner = PINK if turn == "BLUE" else BLUE
                            game_over = True
                        else:
                            turn = "PINK" if turn == "BLUE" else "BLUE"
                else:
                    # Tapped outside the grid: revert.
                    selected_piece["pos"] = selected_piece.get(
                        "orig_pos", selected_piece["pos"])
                selected_piece = None
pygame.quit()
