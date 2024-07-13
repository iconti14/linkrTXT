# bot.py

import os
import random
import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')
channel = None
channel = (bot.get_channel(1261066726393511980) or bot.fetch_channel(1261066726393511980))

pictureFolderNames = ["gay", "snowball"]

def select_image(folderName):
    """
    Selects a random photo from photo bank and returns it to be sent

    :returns (str): Path to image

    :param folderName (str): Name of folder
    """
    folderName = folderName.lower()
    pathToPhotos = os.path.join("c:/dev/discord_bot/pics",folderName)

    if not folderName in pictureFolderNames:
        return None
    
    listofAvailablePics = os.listdir(pathToPhotos)
    return os.path.join(pathToPhotos, listofAvailablePics[random.randint(0,len(listofAvailablePics))])

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    

@bot.event
async def on_message(message):
    message.content = message.content.lower()

    if message.author == bot.user:
        return

    if message.content.startswith('$'):
        text = message.content.split("$")

        if text[1] == "hello":
            await message.channel.send('Hello!')

        if text[1].startswith("sendpic "):
            sendPicSplit = text[1].split(" ")
            if sendPicSplit[1] == "list":
                await message.channel.send("List of folders is: {}".format(pictureFolderNames))
            else:
                if select_image(sendPicSplit[1]) == None:
                    await message.channel.send("That's not an option, idiot :(")
                else:
                    await message.channel.send("Here is a {} picture".format(sendPicSplit[1]), file=discord.File(select_image(sendPicSplit[1])))

    if "thank" in message.content:
            await message.channel.send("You're welcome :)")

    if "ur mom" in message.content:
       await message.channel.send(file=discord.File('c:/dev/discord_bot/pics/mom_gay.png'))

bot.run(TOKEN)