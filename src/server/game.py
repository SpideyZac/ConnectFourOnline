from src.server.utils import stringify

class Game:
    def __init__(self):
        self.board = [[0 for j in range(7)] for i in range(6)]
        self.nextrow = [5 for i in range(7)]
        self.turn = 1
        self.lastmove = None
        self.lastturn = None

    def move(self, col: int) -> str:
        if self.nextrow[col] == -1:
            return stringify({"success": False})

        self.board[self.nextrow[col]][col] = self.turn
        self.lastmove = (self.nextrow[col], col)
        self.lastturn = self.turn
        self.nextrow[col] -= 1
        self.turn *= -1

        return stringify({"success": True})

    def is_tie(self) -> bool:
        for i in range(7):
            if i != -1:
                return False
        return True

    def is_win(self) -> bool:
        if self.lastmove[0] - 3 >= 0:
            for i in range(3):
                if self.board[self.lastmove[0] - i][self.lastmove[1]] != self.lastturn:
                    break
            else:
                return True
        if self.lastmove[1] - 3 >= 0:
            for i in range(3):
                if self.board[self.lastmove[0]][self.lastmove[1] - i] != self.lastturn:
                    break
            else:
                return True 
        if self.lastmove[1] + 3 <= 6:
            for i in range(3):
                if self.board[self.lastmove[0]][self.lastmove[1] + i] != self.lastturn:
                    break
            else:
                return True
        if self.lastmove[0] - 3 >= 0 and self.lastmove[1] - 3 >= 0:
            for i in range(3):
                if self.board[self.lastmove[0] - i][self.lastmove[1] - i] != self.lastturn:
                    break
            else:
                return True
        if self.lastmove[0] - 3 >= 0 and self.lastmove[1] + 3 <= 6:
            for i in range(3):
                if self.board[self.lastmove[0] - i][self.lastmove[1] + i] != self.lastturn:
                    break
            else:
                return True

        return False