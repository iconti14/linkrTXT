# main.py

import asyncio
import os
import random

from keep_alive import keep_alive
from discord.ext import commands
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='$')
channel = None
channel = (bot.get_channel(1261803363729674251)
           or bot.fetch_channel(1261803363729674251))

pictureFolderNames = ["gay", "snowball"]


def select_image(folderName: str):
    """
    Selects a random photo from photo bank and returns it to be sent

    :returns (str): Path to image

    :param folderName (str): Name of folder
    """
    folderName = folderName.lower()
    pathToPhotos = os.path.join("pics", folderName)

    if folderName not in pictureFolderNames:
        return None

    listofAvailablePics = os.listdir(pathToPhotos)
    return os.path.join(
        pathToPhotos,
        listofAvailablePics[random.randint(0, len(listofAvailablePics))])


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    message.content = message.content.lower()

    if message.author == bot.user:
        return

    # I couldn't get commands to work, so this will do for now
    if message.content.startswith('$'):
        text = message.content.split("$")

        if text[1] == "hello":
            await message.reply('Hello!')

        if text[1].startswith("sendpic "):
            sendPicSplit = text[1].split(" ")
            if sendPicSplit[1] == "list":
                await message.reply(
                    "List of folders is: {}".format(pictureFolderNames))
            else:
                selectImage = select_image(sendPicSplit[1])
                if selectImage is None:
                    await message.reply("That's not an option, idiot 😡")
                else:
                    await message.reply("Here is a {} picture".format(
                        sendPicSplit[1]),
                                        file=discord.File(selectImage))

    # These are not commands, just silly things
    elif "thank" in message.content:
        await message.reply("You're welcome ❤️")

    elif "ur mom" in message.content:
        await message.reply(file=discord.File('pics/gay/mom_gay.png'))

    elif "fuck you" in message.content:
        await message.add_reaction("😡")
        await message.add_reaction("🖕")

    elif message.content[-1] == "*":
        await message.reply("Ha ha! You can't spell, idiot")


@bot.event
async def on_message_edit(messageBefore, messageAfter):
    await messageAfter.reply("I SAW THAT 👀")


if TOKEN is None:
    print("DISCORD_TOKEN environment variable is not set. Please set it.")
else:
    keep_alive()
    bot.run(TOKEN)
