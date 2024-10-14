import discord
from board import Board
from dotenv import load_dotenv
import os
from webserver import keep_alive

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# master board
board = Board()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # handle different case words
    message.content = message.content.lower()

    # GAME MODE
    if message.content == 'mode single':
        await message.channel.send(embed=board.modeSingle())

    if message.content == 'mode multi':
        await message.channel.send(embed=board.modeMulti())

    if message.content.startswith('difficulty'):
        await message.channel.send(embed=board.changeDifficulty(message.content))


    # PLAYER CONFIG
    if message.content == 'players':
        # await message.channel.send(board.showPlayers())
        await message.channel.send(embed=board.showPlayers())

    if message.content == 'play':
        await message.channel.send(board.setPlayer(message.author))
    
    if message.content.startswith('exit'):
        await message.channel.send(board.removePlayer(message.author))


    # GAME LOGIC / GAME PLAY
    if message.content.startswith('place'):
        embed, file = board.place(message.author, message.content)
        if file:
            await message.channel.send(embed=embed, file=discord.File("./currentBoard.jpg"))
        else:
            await message.channel.send(embed=embed)
    
    
    # RESET
    if message.content == 'reset':
        embed, file = board.reset(message.author)
        if file:
            await message.channel.send(embed=embed, file=discord.File("./currentBoard.jpg"))
        else:
            await message.channel.send(embed=embed)
    

    # APPEARANCE
    if message.content == 'show':
        await message.channel.send(embed=board.outputStr('show'), file=discord.File("./currentBoard.jpg"))

    if message.content == 'change background':
        await message.channel.send(embed=board.changeBackground(message))

    if message.content == 'change x':
        await message.channel.send(embed=board.changeXImage(message))

    if message.content == 'change o':
        await message.channel.send(embed=board.changeOImage(message))

    if message.content == 'reset images':
        await message.channel.send(embed=board.resetImages())

    # HELP COMMAND    
    if message.content == 'help':
        await message.channel.send(embed=board.help())


keep_alive()                    # FOR WEB SERVER TO KEEP IT ONLINE (ONLY FOR DEPLOYMENT)
client.run(os.getenv('TOKEN'))  # TO GET BOT TOKEN