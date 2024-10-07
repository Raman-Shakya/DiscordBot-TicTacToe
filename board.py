import discord
from genImg import drawBoard

class Board:
    def __init__(self):
        self.size = 3
        self.board = [[' ' for i in range(self.size)] for j in range(self.size)]
        self.players = 'XO'
        self.turn = 0
        self.playersID = []
        self.single = False
        self.started = False

    def modeSingle(self):
        if self.started: return discord.Embed(title="Game Mode", description="Cannot change mode after the game has started.", colour=discord.Colour.red())
        self.single = True
        return discord.Embed(title="Game Mode", description="Game mode set to single player.", colour=discord.Colour.blurple())

    def modeMulti(self):
        if self.started: return discord.Embed(title="Game Mode", description="Cannot change mode after the game has started.", colour=discord.Colour.red())
        self.single = False
        return discord.Embed(title="Game Mode", description="Game mode set to multi player.", colour=discord.Colour.blurple())
    
    """                                                                                                    
    ██████  ██       █████  ██    ██ ███████ ██████       ██████  ██████  ███    ██ ███████ ██  ██████  
    ██   ██ ██      ██   ██  ██  ██  ██      ██   ██     ██      ██    ██ ████   ██ ██      ██ ██       
    ██████  ██      ███████   ████   █████   ██████      ██      ██    ██ ██ ██  ██ █████   ██ ██   ███ 
    ██      ██      ██   ██    ██    ██      ██   ██     ██      ██    ██ ██  ██ ██ ██      ██ ██    ██ 
    ██      ███████ ██   ██    ██    ███████ ██   ██      ██████  ██████  ██   ████ ██      ██  ██████  
                                                                                                        
    """

    def showPlayers(self):
        out = ''
        for i, player in enumerate(self.playersID):
            out += f'**{self.players[i]}**: {player.global_name}\n'

        embedded = discord.Embed(
            title="Players",
            colour=[discord.Colour.red(), discord.Colour.yellow(), discord.Colour.blurple()][len(self.playersID)],
            description=out
        )
        if not self.playersID:
            embedded.set_footer(text="No players available")
        return embedded


    def setPlayer(self, player):
        if player in self.playersID: return self.outputStr('player already added')
        if len(self.playersID) == 2: return self.outputStr('players filled')
        self.playersID.append(player)
        return self.outputStr('added player', player)
    
    def removePlayer(self, player):
        if player in self.playersID:
            self.playersID.remove(player)
            return f"<@{player.id}> left the game."
        return self.outputStr('no player')

    """
     ██████   █████  ███    ███ ███████     ██       ██████   ██████  ██  ██████ 
    ██       ██   ██ ████  ████ ██          ██      ██    ██ ██       ██ ██      
    ██   ███ ███████ ██ ████ ██ █████       ██      ██    ██ ██   ███ ██ ██      
    ██    ██ ██   ██ ██  ██  ██ ██          ██      ██    ██ ██    ██ ██ ██      
     ██████  ██   ██ ██      ██ ███████     ███████  ██████   ██████  ██  ██████ 
    """

    def place(self, author, pos):
        if not pos.isnumeric(): return discord.Embed(title='Error', description="Invalid move", colour=discord.Colour.red()), False
        if int(pos) < 0 or int(pos) >= 10: return discord.Embed(title='Error', description="Invalid move", colour=discord.Colour.red()), False
        
        if not self.single:
            if len(self.playersID) != 2: return discord.Embed(title='Error', description="Players not selected.", colour=discord.Colour.red()), False
            if author != self.playersID[self.turn]: return discord.Embed(title='Error', description="Not your turn", colour=discord.Colour.red()), False

        if not self.started:
            self.started = True

        pos = int(pos) - 1
        x_pos = pos % self.size
        y_pos = 2 - pos // self.size
        out = ''
        nextPlayer = ''
        if self.board[y_pos][x_pos] == ' ':
            self.board[y_pos][x_pos] = self.players[self.turn]
            self.turn = 1 - self.turn
            winner = self.winCheck()
            out = f"Playing move {pos+1}\n"
            # winner or draw check
            if winner or sum([sum([ele!=' ' for ele in row]) for row in self.board])==9:
                self.started = False
                out += '\nGame Ended\n'
                if winner:
                    out += f"<@{self.playersID[self.players.index(winner)].id}> won the game 🥳"
                else:
                    out += f"It was a draw!"
                self.turn = 0
            elif not self.single:
                nextPlayer = f"<@{self.playersID[self.turn].id}>'s turn to play."
        else:
            out = "place occupied"
            if not self.single:
                nextPlayer = f"<@{self.playersID[self.turn].id}>'s turn to play."

        drawBoard(self.board)
        embed = discord.Embed(
            title="Place",
            description=out
        )
        embed.set_image(url="attachment://currentBoard.jpg")
        if nextPlayer:
            embed.add_field(name="Next", value=nextPlayer)
        return embed, True
    
    def winCheck(self):
        def rowCheck(row):
            return len(set(row))==1 and row[0]!=' '
        pDiag = []
        sDiag = []
        for i in range(self.size):
            row = []
            col = []
            pDiag.append(self.board[i][i])
            sDiag.append(self.board[i][self.size-1-i])
            for j in range(self.size):
                row.append(self.board[i][j])
                col.append(self.board[j][i])
            if rowCheck(row): return row[0]
            if rowCheck(col): return col[0]
        if rowCheck(pDiag): return pDiag[0]
        if rowCheck(sDiag): return sDiag[0]
        return False

        
        
    def getBoardString(self):
        output = "```\n"
        for i in range(self.size):
            if i != 0:
                output += '--- --- ---\n'
            output += f' {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}\n'
        output += '```'
        return output


    def printBoard(self):
        out = ''
        for i, player in enumerate(self.playersID):
            out += f'**{self.players[i]}**: *{player.global_name}*\n'

        output = self.getBoardString()
        drawBoard(self.board)
        # if self.playersID:
        #     output += f"```\n**{self.playersID[self.turn].global_name}'s** turn to play for {self.players[self.turn]}"
        embed = discord.Embed(
            title='Game',
            colour=[discord.Colour.red(), discord.Colour.yellow(), discord.Colour.blurple()][len(self.playersID)],
            description='**Mode**: '+['singleplayer', 'multiplayer'][self.single]
        )
        embed.set_image(url="attachment://currentBoard.jpg")
        # embed.add_field(name='Board', value=output, inline=True)
        embed.add_field(name='Players', value=out or "No Players", inline=True)
        if self.playersID:
            if self.single:
                embed.set_footer(text=f"{self.playersID[0].display_name}'s turn")
            else:
                embed.set_footer(text=f"{self.playersID[self.turn].display_name}'s turn")
        return embed
    
    def reset(self):
        self.board = [[' ' for i in range(self.size)] for j in range(self.size)]
        return self.outputStr('reset')

    # def move(self, )


    """
     ██████  ██    ██ ████████ ██████  ██    ██ ████████     ██   ██  █████  ███    ██ ██████  ██      ███████ ██████  
    ██    ██ ██    ██    ██    ██   ██ ██    ██    ██        ██   ██ ██   ██ ████   ██ ██   ██ ██      ██      ██   ██ 
    ██    ██ ██    ██    ██    ██████  ██    ██    ██        ███████ ███████ ██ ██  ██ ██   ██ ██      █████   ██████  
    ██    ██ ██    ██    ██    ██      ██    ██    ██        ██   ██ ██   ██ ██  ██ ██ ██   ██ ██      ██      ██   ██ 
     ██████   ██████     ██    ██       ██████     ██        ██   ██ ██   ██ ██   ████ ██████  ███████ ███████ ██   ██ 
    """

    def outputStr(self, outMsg, member=None):
        match outMsg:
            case 'show': return self.printBoard()
            case 'added player': return f"<@{member.id}> is playing {self.players[len(self.playersID)-1]}'s place."
            case 'player already added': return f"Player already added."
            case 'players filled': return f"Cannot accept more players."
            case 'player left': return f"Player left"
            case 'no player': return f"No player in the list."
            case 'reset': return f"Board resetted\n{self.getBoardString()}"

    def help(self):
        out = """
        **Help Commands**
        *play*: Start playing the game
        *exit*: Exit the game
        *show*: Show board
        *players*: Show players
        *place*: Place your move
        *mode multi*: Multiplayer
        *mode single*: Play with bot
        *reset*: Reset board
        """
        return out