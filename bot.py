# This example requires the 'message_content' intent.

import discord
from board import Board
import json
from dotenv import load_dotenv
import os

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

    if message.content == 'play':
        await message.channel.send(board.setPlayer(message.author))
    
    if message.content == 'players':
        # await message.channel.send(board.showPlayers())
        await message.channel.send(embed=board.showPlayers())

    if message.content.startswith('exit'):
        await message.channel.send(board.removePlayer(message.author))

    if message.content.startswith('place'):
        await message.channel.send(board.place(message.author, message.content.split()[1]))
    
    if message.content == 'show':
        await message.channel.send(board.outputStr('show'))

    if message.content.startswith('config'):
        await message.channel.send(message.author)

    if message.content == 'reset':
        await message.channel.send(board.reset())

    if message.content == 'mode single':
        await message.channel.send(board.modeSingle())

    if message.content == 'mode multi':
        await message.channel.send(board.modeMulti())

    if message.content == 'help':
        await message.channel.send(board.help())
        
    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')

client.run(os.getenv('TOKEN'))

