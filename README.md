# Gobblet Jr. Game

Python implementation of the Gobblet Jr. 3x3 board game. The repository contains several versions of the same game, each reflecting improvements in code quality and style based on `pylint` reports.

---

## Folder Structure

```
AllLint/
    gobbletfinal.py         # Final, linted version of the game
    lintfinal.txt           # Lint report for final version
    v1.py, v2.py, v3.py     # Earlier versions with incremental improvements
    r1.txt, r2.txt, r3.txt  # Lint reports for v1, v2, v3
InitialLint/ 
    a.txt                   # Initial lint report for the original game
OriginalGame/ 
    gobblet.py              # Original implementation
```

---

## How to Run

1. **Install dependencies:**
   - Requires Python 3.x
   - Requires `pygame` library  
     Install with:  
     ```
     pip install pygame
     ```

2. **Run the game:**
   - Navigate to the `AllLint` folder and run:
     ```
     python3 gobbletfinal.py
     ```
   - You can also try earlier versions (`v1.py`, `v2.py`, `v3.py`) for comparison.

---

## Linting and Code Quality

- Linting was performed using `pylint`.
- See `AllLint/lintfinal.txt` for the final code's lint report.
- See `AllLint/r1.txt`, `r2.txt`, `r3.txt` for earlier versions' lint reports.
- See `InitialLint/a.txt` for the original game's lint report.

---

## Features

- Playable Gobblet Jr. game with a graphical interface (using pygame).
- Multiple code versions showing progressive improvements in code quality.
- Code adheres to Python best practices and style guidelines.

---

## Game Rules

- The object of the game is to get three in a row of your color, vertically, horizontally, or diagonally. Size doesn’t matter for determining a winner.
- Each player (**blue** or **pink**) starts with 6 pieces: two large, two medium, and two small.
- On each turn, a player can either place a new piece on the board, or move a piece already on the board—from anywhere to anywhere, as long as the “from” and “to” are different.
- A piece can be placed (or moved to) an empty space, or it can be placed/moved on top of a smaller piece already on the board, “gobbling” the smaller piece. The smaller piece does not have to be an opponent’s piece, and the smaller piece may itself have gobbled another piece previously.
- Only visible pieces can be moved, and only visible pieces count toward winning. Gobbled pieces stay on the board, however, and when a piece is moved, any piece that it gobbled stays put and becomes visible.
- If moving a piece exposes a winning sequence for the opponent, and if the destination for the move does not cover up one of the other pieces in the sequence, then the opponent wins—even if the move makes a winning sequence for the moving player.
