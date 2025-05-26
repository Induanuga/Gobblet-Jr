"""
Gobblet Jr. game implementation using pygame.
"""
import pygame

class GobbletGame:
    """Gobblet Jr. game implementation"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 190, 255)
    PINK = (255, 105, 180)
    LIME = (50, 205, 50)
    PURPLE = (128, 0, 128)
    SMALL_RADIUS = 10
    MEDIUM_RADIUS = 20
    LARGE_RADIUS = 30
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        self.window_width, self.window_height = 615, 700
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Gobblet Jr.")
        self.grid_size = 300
        self.grid_x = (self.window_width - self.grid_size) // 2
        self.grid_y = (self.window_height - self.grid_size) // 2
        self.cell_size = self.grid_size // 3
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.spacing_x = self.LARGE_RADIUS * 2
        self.spacing_y = self.LARGE_RADIUS * 1.5
        self.left_x = self.grid_x - self.spacing_x * 2
        self.right_x = self.grid_x + self.grid_size + self.spacing_x * 2
        self.row2_y = self.window_height - self.LARGE_RADIUS - 20
        self.row1_y = self.row2_y - self.spacing_y * 1.5
        self.pieces = self.init_pieces()
        self.selected_piece = None
        self.turn = "BLUE"
        self.game_over = False
        self.winner = None

    def init_pieces(self):
        """Initializes all pieces."""
        return [
            # Blue pieces (Left side)
            {"color": self.BLUE, "pos": [self.left_x, self.row1_y],
                "radius": self.SMALL_RADIUS, "stack": []},
            {"color": self.BLUE, "pos": [self.left_x + self.spacing_x - 12, self.row1_y],
                "radius": self.MEDIUM_RADIUS, "stack": []},
            {"color": self.BLUE, "pos": [self.left_x + self.spacing_x * 2, self.row1_y],
                "radius": self.LARGE_RADIUS, "stack": []},
            {"color": self.BLUE, "pos": [self.left_x, self.row2_y],
                "radius": self.SMALL_RADIUS, "stack": []},
            {"color": self.BLUE, "pos": [self.left_x + self.spacing_x - 12, self.row2_y],
                "radius": self.MEDIUM_RADIUS, "stack": []},
            {"color": self.BLUE, "pos": [self.left_x + self.spacing_x * 2, self.row2_y],
                "radius": self.LARGE_RADIUS, "stack": []},
            # Pink pieces (Right side)
            {"color": self.PINK, "pos": [self.right_x, self.row1_y],
                "radius": self.SMALL_RADIUS, "stack": []},
            {"color": self.PINK, "pos": [self.right_x - self.spacing_x + 12, self.row1_y],
                "radius": self.MEDIUM_RADIUS, "stack": []},
            {"color": self.PINK, "pos": [self.right_x - self.spacing_x * 2, self.row1_y],
                "radius": self.LARGE_RADIUS, "stack": []},
            {"color": self.PINK, "pos": [self.right_x, self.row2_y],
                "radius": self.SMALL_RADIUS, "stack": []},
            {"color": self.PINK, "pos": [self.right_x - self.spacing_x + 12, self.row2_y],
                "radius": self.MEDIUM_RADIUS, "stack": []},
            {"color": self.PINK, "pos": [self.right_x - self.spacing_x * 2, self.row2_y],
                "radius": self.LARGE_RADIUS, "stack": []}
        ]

    def reset_game(self):
        """Resets the game state."""
        self.pieces = self.init_pieces()
        self.selected_piece = None
        self.turn = "BLUE"
        self.game_over = False
        self.winner = None

    def draw_grid(self):
        """Draws a 3x3 grid."""
        for i in range(1, 3):
            pygame.draw.line(
                self.screen, self.BLACK,
                (self.grid_x + i * self.cell_size, self.grid_y),
                (self.grid_x + i * self.cell_size, self.grid_y + self.grid_size),
                5
            )
            pygame.draw.line(
                self.screen, self.BLACK,
                (self.grid_x, self.grid_y + i * self.cell_size),
                (self.grid_x + self.grid_size, self.grid_y + i * self.cell_size),
                5
            )
        pygame.draw.rect(self.screen, self.BLACK, (self.grid_x,
                            self.grid_y, self.grid_size, self.grid_size), 5)

    def write_text(self):
        """Displays player names, turn."""
        text1 = self.font.render("Player 1", True, self.BLUE)
        text2 = self.font.render("Player 2", True, self.PINK)
        turn_text = self.font.render(f"Turn: {self.turn}", True, self.BLACK)
        self.screen.blit(text1, (20, 50))
        self.screen.blit(text2, (self.window_width - 110, 50))
        self.screen.blit(turn_text, (self.window_width // 2 - 50, 20))

    def draw_pieces(self):
        """Draws all pieces and highlights the selected piece."""
        for p in self.pieces:
            pygame.draw.circle(self.screen, p["color"], p["pos"], p["radius"])
            if p == self.selected_piece:
                pygame.draw.circle(self.screen, self.LIME, p["pos"], p["radius"] + 3, 2)

    def get_grid_cell(self, x, y):
        """
        Snaps a position to the nearest grid cell and returns the cell center 
        and the stack of pieces at that cell.
        """
        if (
            self.grid_x <= x <= self.grid_x + self.grid_size
            and self.grid_y <= y <= self.grid_y + self.grid_size
        ):
            col = (x - self.grid_x) // self.cell_size
            row = (y - self.grid_y) // self.cell_size
            grid_pos = (self.grid_x + col * self.cell_size + self.cell_size // 2,
                        self.grid_y + row * self.cell_size + self.cell_size // 2)
            stk = [p for p in self.pieces if tuple(p["pos"]) == grid_pos]
            return grid_pos, stk
        return None, []

    def check_board_win(self):
        """
        Returns a set of winning colors if there is a win on the board,
        otherwise returns None.
        """
        board = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                cell_center = (self.grid_x + col * self.cell_size + self.cell_size // 2,
                               self.grid_y + row * self.cell_size + self.cell_size // 2)
                cell_stack = [p for p in self.pieces if tuple(p["pos"]) == cell_center]
                if cell_stack:
                    board[row][col] = cell_stack[-1]["color"]
        winning_colors = set()
        for row in board:
            if row[0] and row[0] == row[1] == row[2]:
                winning_colors.add(row[0])
        for col in range(3):
            if board[0][col] and board[0][col] == board[1][col] == board[2][col]:
                winning_colors.add(board[0][col])
        if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
            winning_colors.add(board[0][0])
        if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
            winning_colors.add(board[0][2])
        return winning_colors if winning_colors else None

    def handle_game_over_display(self):
        """Displays the game over screen"""
        over_font = pygame.font.Font(None, 50)
        winner_font = pygame.font.Font(None, 52)
        prompt_font = pygame.font.Font(None, 56)
        line1 = over_font.render("Game Over!", True, self.PURPLE)
        varx = self.BLUE if self.winner == self.BLUE else self.PINK
        line2 = winner_font.render(
            f"Winner: {'Player 1' if self.winner == self.BLUE else 'Player 2'}", True, varx)
        line3 = prompt_font.render("Press R to restart the game", True, self.LIME)
        total_height = line1.get_height() + line2.get_height() + line3.get_height() + 20
        start_y = self.window_height // 2 - total_height // 2
        self.screen.blit(line1, (self.window_width // 2 - line1.get_width() // 2, start_y))
        self.screen.blit(line2, (self.window_width // 2 - line2.get_width() // 2,
                            start_y + line1.get_height() + 30))
        self.screen.blit(line3, (self.window_width // 2 - line3.get_width() // 2,
                            start_y + line1.get_height() + line2.get_height() + 70))

    def handle_piece_selection(self, mx, my):
        """Handle selecting a piece"""
        for piece in self.pieces:
            px, py = piece["pos"]
            if (mx - px) ** 2 + (my - py) ** 2 <= piece["radius"] ** 2:
                _, stack = self.get_grid_cell(px, py)
                if stack and stack[-1] != piece:
                    continue
                if ((self.turn == "BLUE" and piece["color"] == self.BLUE) or
                    (self.turn == "PINK" and piece["color"] == self.PINK)):
                    self.selected_piece = piece
                    piece["orig_pos"] = piece["pos"][:]
                break

    def handle_piece_placement(self, mx, my):
        """Handle placing a selected piece"""
        new_pos, stack = self.get_grid_cell(mx, my)
        if new_pos:
            # Enforce stacking rule: only place on an empty cell
            # or on a piece that is smaller.
            if stack and self.selected_piece["radius"] <= stack[-1]["radius"]:
                # Invalid move: revert to original position.
                self.selected_piece["pos"] = self.selected_piece.get(
                    "orig_pos", self.selected_piece["pos"])
            else:
                self.selected_piece["pos"] = list(new_pos)
                # To mark this piece as now on top, remove and re-append it.
                if self.selected_piece in self.pieces:
                    self.pieces.remove(self.selected_piece)
                    self.pieces.append(self.selected_piece)
                winning_colors = self.check_board_win()
                if winning_colors:
                    if len(winning_colors) == 1:
                        self.winner = winning_colors.pop()
                    else:
                        self.winner = self.PINK if self.turn == "BLUE" else self.BLUE
                    self.game_over = True
                else:
                    self.turn = "PINK" if self.turn == "BLUE" else "BLUE"
        else:
            # Tapped outside the grid: revert.
            self.selected_piece["pos"] = self.selected_piece.get(
                "orig_pos", self.selected_piece["pos"])
        self.selected_piece = None

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.screen.fill(self.WHITE)
            if self.game_over:
                self.handle_game_over_display()
            else:
                self.draw_grid()
                self.write_text()
                self.draw_pieces()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_over:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.reset_game()
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if self.selected_piece is None:
                        self.handle_piece_selection(mx, my)
                    else:
                        self.handle_piece_placement(mx, my)
        pygame.quit()

if __name__ == "__main__":
    game = GobbletGame()
    game.run()
