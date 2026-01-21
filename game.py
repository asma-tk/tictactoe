# game.py
EMPTY, X, O = 0, 1, 2
WIN_LEN = 5

class Game:
    def __init__(self, size=10):
        self.size = size
        self.reset()

    def reset(self):
        self.grid = [[EMPTY]*self.size for _ in range(self.size)]
        self.player = X

    def valid(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == EMPTY

    def play(self, r, c):
        if not self.valid(r, c):
            return False
        self.grid[r][c] = self.player
        self.player = O if self.player == X else X
        return True

    def winner(self):
        g, n = self.grid, self.size
        dirs = [(0,1),(1,0),(1,1),(1,-1)]
        for r in range(n):
            for c in range(n):
                p = g[r][c]
                if p == EMPTY: 
                    continue
                for dr, dc in dirs:
                    ok = True
                    for k in range(WIN_LEN):
                        rr, cc = r + dr*k, c + dc*k
                        if not (0 <= rr < n and 0 <= cc < n) or g[rr][cc] != p:
                            ok = False
                            break
                    if ok:
                        return p
        return None

    def draw(self):
        return self.winner() is None and all(cell != EMPTY for row in self.grid for cell in row)

    def fallback_move(self):
        center = self.size // 2
        best, best_d = None, 10**9
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == EMPTY:
                    d = abs(r-center) + abs(c-center)
                    if d < best_d:
                        best_d = d
                        best = (r, c)
        return best
