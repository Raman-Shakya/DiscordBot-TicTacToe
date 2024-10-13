import discord
import requests
from genImg import drawBoard, readImages, resetImages

class Board:
    def __init__(self):
        self.size = 3
        self.board = [[' ' for i in range(self.size)] for j in range(self.size)]
        self.players = 'XO'
        self.turn = 0
        self.playersID = []
        self.single = False
        self.difficulty = 9
        self.started = False

    """
     ██████   █████  ███    ███ ███████     ███    ███  ██████  ██████  ███████ 
    ██       ██   ██ ████  ████ ██          ████  ████ ██    ██ ██   ██ ██      
    ██   ███ ███████ ██ ████ ██ █████       ██ ████ ██ ██    ██ ██   ██ █████   
    ██    ██ ██   ██ ██  ██  ██ ██          ██  ██  ██ ██    ██ ██   ██ ██      
     ██████  ██   ██ ██      ██ ███████     ██      ██  ██████  ██████  ███████ 
    """

    def modeSingle(self):
        if self.started: return discord.Embed(title="Game Mode", description="Cannot change mode after the game has started.", colour=discord.Colour.red())
        self.single = True
        return discord.Embed(title="Game Mode", description="Game mode set to single player.", colour=discord.Colour.blurple())

    def modeMulti(self):
        if self.started: return discord.Embed(title="Game Mode", description="Cannot change mode after the game has started.", colour=discord.Colour.red())
        self.single = False
        return discord.Embed(title="Game Mode", description="Game mode set to multi player.", colour=discord.Colour.blurple())
    
    def changeDifficulty(self, message):
        messageValue = message.split()
        if len(messageValue) != 2 or not messageValue[1].isnumeric():
            return discord.Embed(title='Error', description="Invalid difficulty", colour=discord.Colour.red())
        difficulty = int(messageValue[1])
        if difficulty <1 or difficulty > 9: return "Error: Invalid difficulty"
        self.difficulty = difficulty
        return discord.Embed(title='Difficulty', description=f"Difficulty set to {difficulty}", colour=discord.Colour.blurple())
        


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
        self.single = bool(len(self.playersID)==1)
        return self.outputStr('added player', player)
    

    def removePlayer(self, player):
        if player in self.playersID:
            self.playersID.remove(player)
            self.single = True
            if len(self.playersID):
                return f"<@{player.id}> left the game.\nSingle player mode activated."
            return f"<@{player.id}> left the game."
        return self.outputStr('no player')



    """
     ██████   █████  ███    ███ ███████     ██       ██████   ██████  ██  ██████ 
    ██       ██   ██ ████  ████ ██          ██      ██    ██ ██       ██ ██      
    ██   ███ ███████ ██ ████ ██ █████       ██      ██    ██ ██   ███ ██ ██      
    ██    ██ ██   ██ ██  ██  ██ ██          ██      ██    ██ ██    ██ ██ ██      
     ██████  ██   ██ ██      ██ ███████     ███████  ██████   ██████  ██  ██████ 
    """

    def place(self, author, message):
        inputArray = message.split()
        if len(inputArray) != 2 or not inputArray[1].isnumeric(): return discord.Embed(title='Error', description="Invalid command", colour=discord.Colour.red()), False
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
            winner = self.winCheck()

            if not winner:
                if self.single:
                    self.playAI()
                    winner = self.winCheck()
                    self.turn = 1 - self.turn
            self.turn = 1 - self.turn
                    

            out = f"Playing move {pos+1}\n"
            drawBoard(self.board)
            # winner or draw check
            if winner:
                self.started = False
                out += '\nGame Ended\n'
                if winner:
                    if self.single:
                        if winner == True:
                            out += "It was a draw!"
                        elif self.players.index(winner)==0:
                            out += f"<@{self.playersID[0].id}> won the game 🥳"
                        else:
                            out += f"AI won the game!"
                    else:
                        out += f"<@{self.playersID[self.players.index(winner)].id}> won the game 🥳"
                else:
                    out += f"It was a draw!"
                self.turn = 0
                self.resetBoard()
            elif not self.single:
                nextPlayer = f"<@{self.playersID[self.turn].id}>'s turn to play."
        else:
            out = "place occupied"
            if not self.single:
                nextPlayer = f"<@{self.playersID[self.turn].id}>'s turn to play."

        embed = discord.Embed(
            title="Place",
            colour=discord.Colour.blurple(),
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
        return sum([sum([ele!=' ' for ele in row]) for row in self.board])==9  # draw case


    """
     █████  ██ 
    ██   ██ ██ 
    ███████ ██ 
    ██   ██ ██ 
    ██   ██ ██         
    """
    def playAI(self):
        bestScore = float('inf')
        bestPos = [None, None]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(False)
                    if score < bestScore:
                        bestScore = score
                        bestPos = [i, j]
                    self.board[i][j] = ' '
        self.board[bestPos[0]][bestPos[1]] = 'O'

    def minimax(self, ai=True, depth=0):
        if depth==self.difficulty: return 0
        winner = self.winCheck()
        if winner == 'O': return -1
        elif winner == 'X': return 1
        elif winner: return 0

        minScore = float('inf')
        maxScore = -float('inf')
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != ' ': continue

                self.board[i][j] = 'XO'[ai] # play move
                score = self.minimax(not ai, depth+1)
                self.board[i][j] = ' '

                if score < minScore:
                    minScore = score
                if score > maxScore:
                    maxScore = score
        return [maxScore, minScore][ai]


    """
    ██████  ███████ ███████ ███████ ████████ 
    ██   ██ ██      ██      ██         ██    
    ██████  █████   ███████ █████      ██    
    ██   ██ ██           ██ ██         ██    
    ██   ██ ███████ ███████ ███████    ██    
    """

    def resetBoard(self):
        self.board = [[' ' for i in range(self.size)] for j in range(self.size)]


    def reset(self, author):
        if not author in self.playersID:
            return discord.Embed(title="Not Permitted", description=f"<@{author.id}> is not a player.", colour=discord.Colour.red()), False
        self.resetBoard()
        drawBoard(self.board)
        embed = discord.Embed(title="Board", description=f"<@{author.id}> resetted the board.", colour=discord.Colour.blurple())
        embed.set_image(url="attachment://currentBoard.jpg")
        return embed, True



    """
     █████  ██████  ██████  ███████  █████  ██████   █████  ███    ██  ██████ ███████ 
    ██   ██ ██   ██ ██   ██ ██      ██   ██ ██   ██ ██   ██ ████   ██ ██      ██      
    ███████ ██████  ██████  █████   ███████ ██████  ███████ ██ ██  ██ ██      █████   
    ██   ██ ██      ██      ██      ██   ██ ██   ██ ██   ██ ██  ██ ██ ██      ██      
    ██   ██ ██      ██      ███████ ██   ██ ██   ██ ██   ██ ██   ████  ██████ ███████                                                                                 
    """
        
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

        drawBoard(self.board)
        # if self.playersID:
        #     output += f"```\n**{self.playersID[self.turn].global_name}'s** turn to play for {self.players[self.turn]}"
        embed = discord.Embed(
            title='Game',
            colour=[discord.Colour.red(), discord.Colour.yellow(), discord.Colour.blurple()][len(self.playersID)],
            description='**Mode**: '+['multiplayer', 'singleplayer'][self.single]
                        + "\n**Difficulty**: " + str(self.difficulty) 
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


    def changeBackground(self, message):
        if not message.attachments: return discord.Embed(title="Error", description="No images provided", colour=discord.Colour.red())
        filename = message.attachments[0].filename
        if (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
        ):
            background = requests.get(message.attachments[0].url)
            open(f'./assets/Board.png', 'wb').write(background.content)
            readImages()
            return discord.Embed(title="Background Changed", description="Background image changed successfully.", colour=discord.Colour.blurple())
        return discord.Embed(title="Error", description="Invalid Images", colour=discord.Colour.red())


    def changeXImage(self, message):
        if not message.attachments: return discord.Embed(title="Error", description="No images provided", colour=discord.Colour.red())
        filename = message.attachments[0].filename
        if (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
        ):
            background = requests.get(message.attachments[0].url)
            open(f'./assets/X.png', 'wb').write(background.content)
            readImages()
            return discord.Embed(title="X Image Changed", description="X image changed successfully.", colour=discord.Colour.blurple())
        return discord.Embed(title="Error", description="Invalid Images", colour=discord.Colour.red())


    def changeOImage(self, message):
        if not message.attachments: return discord.Embed(title="Error", description="No images provided", colour=discord.Colour.red())
        filename = message.attachments[0].filename
        if (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
        ):
            background = requests.get(message.attachments[0].url)
            open(f'./assets/O.png', 'wb').write(background.content)
            readImages()
            return discord.Embed(title="O Image Changed", description="O image changed successfully.", colour=discord.Colour.blurple())
        return discord.Embed(title="Error", description="Invalid Images", colour=discord.Colour.red())


    def resetImages(self):
        resetImages()        
        return discord.Embed(title="Assets Resetted", description="All assets were changed to default.", colour=discord.Colour.blurple())



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


    def help(self):
        out = """
**Play**: Start playing the game
**Exit**: Exit the game
**Show**: Show board
**Players**: Show players
**Place**: Place your move
**Mode multi**: Multiplayer
**Mode single**: Play with bot
**Reset**: Reset board
        """
        embedded = discord.Embed(
            title="Help Commands",
            colour=[discord.Colour.red(), discord.Colour.yellow(), discord.Colour.blurple()][len(self.playersID)],
            description=out
        )
        # embedded.add_field(name="Play",value="Start the game")
        return embedded