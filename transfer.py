from discord.ext import commands
import json
from timeit import default_timer
import asyncio
from discord.ext.commands import CommandNotFound
import discord

client = commands.Bot(command_prefix=['<:haaa:855976143722512425>', '%'])


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="chess with Mr.Z"))


def saveData(user_id, lvl, xp, lastMessage):
    user = {user_id: {"lvl": lvl, "xp": xp, "lastMessage": lastMessage}}
    with open("users.json", "r") as file:
        data = json.load(file)

    if str(user_id) in data["users"]:
        pass
    else:
        if lvl == None:
            lvl = 0
            user = {user_id: {"lvl": lvl, "xp": xp, "lastMessage": lastMessage}}

        if xp == None:
            xp = 0
            user = {user_id: {"lvl": lvl, "xp": xp, "lastMessage": lastMessage}}

        data["users"].update(user)

        with open("users.json", "w") as file:
            json.dump(data, file)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    with open("users.json", "r") as f:
        data = json.load(f)

    try:
        lvl = data["users"][str(message.author.id)]["lvl"]
        xp = data["users"][str(message.author.id)]["xp"]
    except KeyError:
        lvl = 0
        xp = 0

        start = default_timer()
        saveData(user_id=message.author.id, lvl=lvl, xp=xp, lastMessage=start)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


client.run('OTI2ODI4MDI4OTk3MzA0MzUw.YdBV3Q.ti2uyFD95unyC9h9zByYWLVjDDg')
