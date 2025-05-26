# Gobblet Jr. Game

Python implementation of the Gobblet Jr. board game. The repository contains several versions of the same game, each reflecting improvements in code quality and style based on `pylint` reports.

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
     python gobbletfinal.py
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
