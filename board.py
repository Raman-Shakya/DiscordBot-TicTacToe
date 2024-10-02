class Board:
    def __init__(self):
        self.size = 3
        self.board = [[' ' for i in range(self.size)] for j in range(self.size)]
        self.players = 'XO'
        self.turn = 0
        self.playersID = []

    def setPlayer(self, player):
        if player in self.playersID: return self.outputStr('player already added')
        if len(self.playersID) == 2: return self.outputStr('players filled')
        self.playersID.append(player)
        return self.outputStr('added player', player)
    
    def removePlayer(self, player):
        if player in self.playersID:
            self.playersID.remove(player)
            return self.outputStr('player left')
        return self.outputStr('no player')

    def place(self, author, pos):
        if not pos.isnumeric(): return "Invalid move"
        if int(pos) < 0 or int(pos) >= 10: return "Invalid move"
        # if len(self.playersID) != 2: return "Players not selected."
        # if author != self.playersID[self.turn]: return "Not your turn"
        pos = int(pos) - 1
        x_pos = pos % self.size
        y_pos = 2 - pos // self.size
        if self.board[y_pos][x_pos] == ' ':
            self.board[y_pos][x_pos] = self.players[self.turn]
            self.turn = 1 - self.turn
            return f"Playing move {pos+1}\n{self.printBoard()}"
        return "Place occupied"
        
    def printBoard(self):
        output = "```\n"
        for i in range(self.size):
            if i != 0:
                output += '--- --- ---\n'
            output += f' {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}\n'
        return output + "\n```"
        # + f"\n <@{self.playersID[self.turn].id}>'s turn"
    
    def reset(self):
        self.board = [[' ' for i in range(self.size)] for j in range(self.size)]
        return self.outputStr('reset')





    def outputStr(self, outMsg, member=None):
        print("msgs", outMsg)
        return {
            'show': self.printBoard(),
            'added player': f"<@{member.id}> is playing {self.players[len(self.playersID)-1]}'s place.",
            'player already added': f"Player already added.",
            'players filled': f"Cannot accept more players.",
            'player left': f"Player left",
            'no player': f"No player in the list.",
            'reset': f"Board resetted\n{self.printBoard()}",
        }[outMsg]
