# main.py

import asyncio
import os
import random
import json

from discord.ext import commands
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='$')
channel = None
channel = (bot.get_channel(1261803363729674251)
           or bot.fetch_channel(1261803363729674251))

pictureFolderNames = os.listdir("pics")

with open("configs/messages.json", encoding="utf-8") as fh:
    bot_messages = json.load(fh)

with open("configs/commands.json", encoding="utf-8") as fh:
    bot_commands = json.load(fh)


def select_image(folderName: str):
    """
    Selects a random photo from photo bank and returns it to be sent

    :returns (str): Path to image

    :param folderName (str): Name of folder
    """
    folderName = folderName.lower()
    pathToPhotos = os.path.join("pics", folderName)

    if folderName == "list":
        return "list"

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
        spaceSplit = text[1].split(" ")

        if spaceSplit[0] in bot_commands:

            # reply functionality
            if bot_commands[spaceSplit[0]]["func"] == "reply":
                await message.reply(bot_commands[spaceSplit[0]]["reply"])

            # Sendpic functionality
            elif bot_commands[spaceSplit[0]]["func"] == "sendpic":
                selectImage = select_image(spaceSplit[1])
                if selectImage is None:
                    await message.reply("That's not an option, idiot 😡")
                elif selectImage == "list":
                    await message.reply(
                        "List of folders is: {}".format(pictureFolderNames))
                elif isinstance(selectImage, str):
                    await message.reply("Here is a {} picture".format(
                        spaceSplit[1]),
                                        file=discord.File(selectImage))

    # These are not commands, just silly things
    for key in bot_messages:
        if key in message.content:
            falseTrigger = True
            if "special" not in bot_messages[key] or (
                    bot_messages[key]["special"] == "endswith"
                    and message.content[-1] == key and key
                    not in message.content.rstrip(message.content[-1])):
                falseTrigger = False

            if not falseTrigger:
                if bot_messages[key]["type"] == "message":
                    await message.reply(bot_messages[key]["reply"])
                elif bot_messages[key]["type"] == "image":
                    await message.reply(
                        file=discord.File(bot_messages[key]["imagePath"]))
                elif bot_messages[key]["type"] == "react":
                    for value in bot_messages[key]["reactions"]:
                        await message.add_reaction(value)


@bot.event
async def on_message_edit(messageBefore, messageAfter):
    if messageBefore.content != messageAfter.content:
        await messageAfter.reply("I SAW THAT 👀")


if TOKEN is None:
    print("DISCORD_TOKEN environment variable is not set. Please set it.")
else:
    bot.run(TOKEN)
