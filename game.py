# game.py
EMPTY = 0
X = 1
O = 2
WIN_LEN = 5


def check_winner(grid):
    size = len(grid)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1),  # diagonal /
    ]

    for r in range(size):
        for c in range(size):
            player = grid[r][c]
            if player == EMPTY:
                continue

            for dr, dc in directions:
                if _has_five(grid, r, c, dr, dc, player):
                    return player
    return None


def _has_five(grid, r, c, dr, dc, player):
    size = len(grid)
    for k in range(WIN_LEN):
        rr = r + dr * k
        cc = c + dc * k
        if rr < 0 or rr >= size or cc < 0 or cc >= size:
            return False
        if grid[rr][cc] != player:
            return False
    return True


def is_draw(grid):
    if check_winner(grid) is not None:
        return False
    for row in grid:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


class GameEngine:
    def __init__(self, size=10):
        self.size = size
        self.reset()

    def reset(self):
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = X
        self.history = []

    def is_valid_move(self, row, col):
        return (
            0 <= row < self.size
            and 0 <= col < self.size
            and self.grid[row][col] == EMPTY
        )

    def play(self, row, col):
        if not self.is_valid_move(row, col):
            return False

        player = self.current_player
        self.grid[row][col] = player
        self.history.append((row, col, player))

        self.current_player = O if self.current_player == X else X
        return True

    def winner(self):
        return check_winner(self.grid)

    def draw(self):
        return is_draw(self.grid)
