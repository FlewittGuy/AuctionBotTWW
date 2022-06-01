from discord import Color
import json
from timeit import default_timer
import random
import asyncio
from discord.ext.commands.errors import ChannelNotFound, MissingRequiredArgument, MissingPermissions, CommandNotFound
import time
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.utils import get
from discord.ext.commands.errors import ChannelNotFound, MissingRequiredArgument


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=['<:haaa:855976143722512425>', '%'], intents=intents)


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
async def on_member_join(member):
    channel = client.get_channel(783542225170464838)

    user = get(client.get_all_members(), id=member.id)
    embed = discord.Embed(title=f"A new user has joined the server!", color=discord.Color.blue())
    embed.set_author(name=member.name, icon_url=user.avatar)
    embed.set_footer(text="Grab the merchant role in #reaction-roles to post in #trading-center")
    await channel.send(f"{member.mention}", embed=embed)

    with open("users.json", "r") as file:
        data = json.load(file)

    try:
       lvl = data["users"][str(member.id)]["lvl"]
       xp = data["users"][str(member.id)]["xp"]
    except KeyError:
        lvl = 0
        xp = 0

        start = default_timer()
        saveData(user_id=member.id, lvl=lvl, xp=xp, lastMessage=start)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="chess with Mr.Z"))


@client.event
async def on_message(message):
    global lvl, xp
    if message.author.bot:
        return

    with open("users.json", "r") as file:
        data = json.load(file)

    if str(message.author.id) in data["users"]:
        end = default_timer()
        last = int(data["users"][str(message.author.id)]["lastMessage"])
        time = end - last
        if time <= 60:
            if time < -1:
                start = default_timer()
                data["users"][str(message.author.id)]["lastMessage"] = start
                with open("users.json", "w") as file:
                    json.dump(data, file)
        else:
            start = default_timer()
            data["users"][str(message.author.id)]["lastMessage"] = start
            xpGain = random.randrange(15, 26)
            data["users"][str(message.author.id)]["xp"] += xpGain

            with open("users.json", "w") as file:
                json.dump(data, file)
    else:
        pass

    try:
        lvl = data["users"][str(message.author.id)]["lvl"]
        xp = data["users"][str(message.author.id)]["xp"]
    except KeyError:
        pass

    try:
        if message.channel.id not in [782978946735407154, 779391543156015116, 927400147158175814]:
            def sumIt():
                summed = 0
                for i in range(int(lvl) + 1):
                    nextLevel = 5 * (i ** 2) + 50 * i + 100
                    summed += nextLevel
                return summed

            if int(sumIt()) <= int(xp):
                data["users"][str(message.author.id)]["lvl"] += 1

                with open("users.json", "w") as file:
                    json.dump(data, file)

                msg = await message.reply(content=
                                          f"Congrats. You are now one step closer to beating Cat. You are now level {lvl + 1}"
                                          )
                await asyncio.sleep(5)
                await msg.delete()

                lvl = int(data["users"][str(message.author.id)]["lvl"])

                if lvl >= 1:
                    role = message.guild.get_role(931328684927881256)
                    await message.author.add_roles(role)

                if lvl >= 5:
                    role = message.guild.get_role(931328858857291797)
                    await message.author.add_roles(role)

                if lvl >= 10:
                    role = message.guild.get_role(931334495104282654)
                    await message.author.add_roles(role)

                if lvl >= 15:
                    role = message.guild.get_role(930800945217011722)
                    await message.author.add_roles(role)

                if lvl >= 20:
                    role = message.guild.get_role(931329139963752469)
                    await message.author.add_roles(role)

                if lvl >= 30:
                    role = message.guild.get_role(931332181538783322)
                    await message.author.add_roles(role)

                if lvl >= 40:
                    role = message.guild.get_role(931332403241300088)
                    await message.author.add_roles(role)

                if lvl >= 50:
                    role = message.guild.get_role(931332515581550693)
                    await message.author.add_roles(role)
            else:
                if lvl == 0:
                    if xp >= 100:
                        data["users"][str(message.author.id)][int("lvl")] += 1

                        with open("users.json", "w") as file:
                            json.dump(data, file)

                        msg = await message.reply(content=
                                                  f"Congrats. You are now one step closer to beating Cat. You are now level {lvl + 1}!"
                                                  )
                        await asyncio.sleep(5)
                        await msg.delete()

                        lvl = int(data["users"][str(message.author.id)]["lvl"])

                        if lvl >= 1:
                            role = message.guild.get_role(931328684927881256)
                            await message.author.add_roles(role)

                        if lvl >= 5:
                            role = message.guild.get_role(931328858857291797)
                            await message.author.add_roles(role)

                        if lvl >= 10:
                            role = message.guild.get_role(931334495104282654)
                            await message.author.add_roles(role)

                        if lvl >= 15:
                            role = message.guild.get_role(930800945217011722)
                            await message.author.add_roles(role)

                        if lvl >= 20:
                            role = message.guild.get_role(931329139963752469)
                            await message.author.add_roles(role)

                        if lvl >= 30:
                            role = message.guild.get_role(931332181538783322)
                            await message.author.add_roles(role)

                        if lvl >= 40:
                            role = message.guild.get_role(931332403241300088)
                            await message.author.add_roles(role)

                        if lvl >= 50:
                            role = message.guild.get_role(931332515581550693)
                            await message.author.add_roles(role)
        else:
            pass

    except NameError:
        pass

    if message.channel.id in [779391543156015116, 933799391658131477]:
        await message.add_reaction(f"✅")
        await message.add_reaction(f"🚫")

    role = get(message.author.guild.roles, name="Muted")
    if role in message.author.roles:
        await message.delete()

    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


class Trade:
    tradeNumber = 1


trade = Trade


@client.event
async def on_ready():
    print("It's Ez is now online!")


@client.command()
async def rank(ctx, member: discord.Member = None):
    try:
        if member is None:
            member = ctx.author

        with open("users.json", "r") as file:
            data = json.load(file)

        rankXp = data["users"][str(member.id)]["xp"]
        rankLevel = data["users"][str(member.id)]["lvl"]

        def sumIt():
            summed = 0
            for i in range(int(rankLevel) + 1):
                nextLevel = 5 * (i ** 2) + 50 * i + 100
                summed += nextLevel
            return summed

        em = discord.Embed(title="Here are your rank statistics!", color=discord.Color.green())
        em.add_field(name="Level", value=f"{rankLevel:,}", inline=True)
        em.add_field(name="XP", value=f"{rankXp:,}", inline=True)
        em.add_field(name="XP Until Next Level", value=f"{int(sumIt()) - int(rankXp):,}", inline=False)

        await ctx.reply(embed=em)
    except KeyError:
        pass


@client.command(aliases=["directmessage", "direct-message", "message", "msg"])
@commands.has_any_role(930668875266281482, 786158305457602600, 787525291723063316, 778254251674566697,
                       782962913815822346, 908158086387224627, 931924123419025428, 931923591765848104)
async def dm(ctx, member: discord.Member = None, *, message=None):
    if message is None and member is None:
        embed = discord.Embed(title="Direct Message", description="Directly message someone a message."
                              , color=discord.Color.blue())
        embed.set_footer(text="Why was this message prompted?\nYou didn't supply any information on who to direct "
                              "message or what to say.")
        embed.add_field(name="Example", value="%dm @<member> <text>\n%msg @<member> <text>\n%directmessage @<member> "
                                              "<text>\n%message @<member> <text>")
        await ctx.reply(embed=embed)
    elif message is None:
        embed = discord.Embed(title="Direct Message", description="Directly message someone a message."
                              , color=discord.Color.red())
        embed.set_footer(text="Why was this message prompted?\nYou didn't supply a message to send.")
        embed.add_field(name="Example", value="%dm @<member> <text>\n%msg @<member> <text>\n%directmessage @<member> "
                                              "<text>\n%message @<member> <text>")
        await ctx.reply(embed=embed)
    elif member is None:
        embed = discord.Embed(title="Direct Message", description="Directly message someone a message."
                              , color=discord.Color.red())
        embed.set_footer(text="Why was this message prompted?\nYou didn't supply a member to message.")
        embed.add_field(name="Example", value="%dm @<member> <text>\n%msg @<member> <text>\n%directmessage @<member> "
                                              "<text>\n%message @<member> <text>")
        await ctx.reply(embed=embed)
    else:
        await ctx.message.delete()
        channel = await member.create_dm()
        await channel.send(f"**{ctx.author} sent you a message:**\n{message}")

    await ctx.message.delete()



@client.command()
@commands.has_any_role("Staff", "Admin", "Manager", "Moderator", "Owner", "Bot Developer",  "Perms", 930668875266281482,)
async def temp(ctx):
    global em0
    em0 = discord.Embed(title="Auction Item Deals")
    em0.set_footer(text="Test")

    global deal1
    deal1 = await ctx.send(embed=em0)
    print(em0 )


@client.command()
@commands.has_any_role("Staff", "Admin", "Manager", "Moderator", "Owner", "Bot Developer", "Perms", 930668875266281482)
async def deal(ctx):
    positive = Button(label="Yes", style=discord.ButtonStyle.green)
    negative = Button(label="No", style=discord.ButtonStyle.red)

    async def positive_callback(interaction):
        if interaction.user == ctx.author:
            auction = Button(label="Auction Items", style=discord.ButtonStyle.primary)
            negative = Button(label="Cancel", style=discord.ButtonStyle.red, row=2)

            auction.callback = auction_callback
            negative.callback = negative_callback

            view = View()
            view.add_item(auction)
            view.add_item(negative)

            em1 = discord.Embed(title="What type of item do you want to trade for?", color=Color.blue())
            await msg.edit(view=view, embed=em1)
        else:
            await interaction.response.send_message(
                f"This isn't your interaction {interaction.user.mention}! If you wish to make a deal, type **%deal*",
                ephemeral=True
            )

    async def negative_callback(interaction):
        if interaction.user == ctx.author:
            no = discord.Embed(title="You chose not to make a deal.", color=Color.red())
            await interaction.response.edit_message(view=None, embed=no)
        else:
            await interaction.response.send_message(
                f"This isn't your interaction {interaction.user.mention}! If you wish to make a deal, type **%deal**",
                ephemeral=True
            )

    async def auction_callback(interaction):
        if interaction.user == ctx.author:
            spitfire = Button(label="Spitfire", style=discord.ButtonStyle.primary)
            negative = Button(label="Cancel", style=discord.ButtonStyle.red, row=2)

            spitfire.callback = spitfire_callback
            negative.callback = negative_callback

            view = View()
            view.add_item(spitfire)
            view.add_item(negative)

            em1 = discord.Embed(title="What item do you want to trade for?", color=Color.blue())
            await msg.edit(view=view, embed=em1)
        else:
            await interaction.response.send_message(
                f"This isn't your interaction {interaction.user.mention}! If you wish to make a deal, type **%deal*",
                ephemeral=True
            )

    async def spitfire_callback(interaction):
        if interaction.user == ctx.author:
            global item
            item = "Spitfire"

            temp = Button(label="Temp", style=discord.ButtonStyle.grey)

            temp.callback = submit_callback

            view = View()
            view.add_item(temp)

            em1 = discord.Embed(title="What maximum serial do you want", color=Color.blue())
            await msg.edit(view=view, embed=em1)
        else:
            await interaction.response.send_message(
                f"This isn't your interaction {interaction.user.mention}! If you wish to make a deal, type **%deal*",
                ephemeral=True
            )

    async def submit_callback(interaction):
        if interaction.user == ctx.author:
            channel = client.get_channel(916743381353386045)
            msg_id = deal1.id

            em0.add_field(name=f"Trade {trade.tradeNumber}",
                          value=f">>> <@!{ctx.author.id}>\n**Trading**\nNot finished yet lol\n\n**Looking For**\n{item}",
                          )

            msg2 = await channel.fetch_message(msg_id)
            await msg2.edit(embed=em0)

            trade.tradeNumber += 1
        else:
            await interaction.response.send_message(
                f"This isn't your interaction {interaction.user.mention}! If you wish to make a deal, type **%deal*",
                ephemeral=True
            )

    positive.callback = positive_callback
    negative.callback = negative_callback

    view = View()
    view.add_item(positive)
    view.add_item(negative)

    em1 = discord.Embed(title="Would you like to make a deal?", color=Color.blue())
    msg = await ctx.reply(view=view, embed=em1)

"""
@client.command(aliases=["ga", "host giveaway", "host ga"])
@commands.has_any_role("Staff", "Admin", "Manager", "Moderator", "Owner", "Bot Developer", "Perms", 930668875266281482)
async def giveaway(ctx):
    class Vars:
        item = ""

    var = Vars

    positive = Button(label="Yes", style=discord.ButtonStyle.green)
    negative = Button(label="No", style=discord.ButtonStyle.red)

    serial = []
    hours = []
    level = []

    async def positive_callback(interaction):
        if interaction.user == ctx.author:
            spitfire = Button(label="Spitfire", style=discord.ButtonStyle.primary)
            kukri = Button(label="Kukri", style=discord.ButtonStyle.primary)
            paterson = Button(label="Paterson Navy", style=discord.ButtonStyle.primary)
            prototype = Button(label="Prototype Pistol", style=discord.ButtonStyle.primary)
            lancaster = Button(label="Lancaster", style=discord.ButtonStyle.primary)
            gccarbine = Button(label="Guycot Chain Carbine", style=discord.ButtonStyle.primary)
            gcpistol = Button(label="Guycot Chain Pistol", style=discord.ButtonStyle.primary)
            guitar = Button(label="Guitar", style=discord.ButtonStyle.primary)
            accordion = Button(label="Accordion", style=discord.ButtonStyle.primary)
            fiddle = Button(label="Fiddle", style=discord.ButtonStyle.primary)
            trumpet = Button(label="Trumpet", style=discord.ButtonStyle.primary)
            drum = Button(label="Drum", style=discord.ButtonStyle.primary)
            harmonica = Button(label="Harmonica", style=discord.ButtonStyle.primary)
            flute = Button(label="Flute", style=discord.ButtonStyle.primary)
            bmk = Button(label="Black Markey Key", style=discord.ButtonStyle.primary)
            cancel = Button(label="Never-mind", style=discord.ButtonStyle.red)

            async def spitfire_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Spitfire"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def kukri_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Kukri"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def paterson_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Paterson Navy"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def prototype_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Prototype Pistol"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def lancaster_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Prototype Pistol"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def gccarbine_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Guycot Chain Carbine"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def gcpistol_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Guycot Chain Pistol"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def guitar_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Guitar"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def accordion_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Accordion"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def fiddle_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Fiddle"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def trumpet_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Trumpet"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def drum_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Drum"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def harmonica_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Harmonica"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def flute_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Flute"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def bmk_callback(interaction):
                if interaction.user == ctx.author:
                    var.item = "Black Market Key"

                    one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
                    two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
                    three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
                    four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
                    five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
                    six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
                    seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
                    eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
                    nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
                    next = Button(label="Next", style=discord.ButtonStyle.green, row=4)
                    zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
                    back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
                    cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

                    async def one_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(1)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def two_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(2)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def three_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(3)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def four_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(4)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def five_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(5)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def six_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(6)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def seven_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(7)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def eight_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(8)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def nine_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(9)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def zero_callback(interaction):
                        if interaction.user == ctx.author:
                            serial.append(0)

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())
                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    async def back_callback(interaction):
                        if interaction.user == ctx.author:
                            try:
                                serial.pop()
                            except IndexError:
                                await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                            em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                                description=f"What is the serial number of your {var.item}?",
                                                color=Color.blue())

                            await interaction.response.edit_message(view=view, embed=em3)
                        else:
                            await ctx.send(
                                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                            )

                    one.callback = one_callback
                    two.callback = two_callback
                    three.callback = three_callback
                    four.callback = four_callback
                    five.callback = five_callback
                    six.callback = six_callback
                    seven.callback = seven_callback
                    eight.callback = eight_callback
                    nine.callback = nine_callback
                    next.callback = level_callback
                    zero.callback = zero_callback
                    back.callback = back_callback
                    cancel.callback = negative_callback

                    view = View()
                    view.add_item(one)
                    view.add_item(two)
                    view.add_item(three)
                    view.add_item(four)
                    view.add_item(five)
                    view.add_item(six)
                    view.add_item(seven)
                    view.add_item(eight)
                    view.add_item(nine)
                    view.add_item(next)
                    view.add_item(zero)
                    view.add_item(back)
                    view.add_item(cancel)

                    em3 = discord.Embed(title=f"Serial: {''.join(map(str, serial))}",
                                        description=f"What is the serial number of your {var.item}?",
                                        color=Color.blue())

                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            bmk.callback = bmk_callback
            flute.callback = flute_callback
            harmonica.callback = harmonica_callback
            drum.callback = drum_callback
            trumpet.callback = trumpet_callback
            fiddle.callback = fiddle_callback
            accordion.callback = accordion_callback
            guitar.callback = guitar_callback
            gcpistol.callback = gcpistol_callback
            gccarbine.callback = gccarbine_callback
            lancaster.callback = lancaster_callback
            prototype.callback = prototype_callback
            paterson.callback = paterson_callback
            kukri.callback = kukri_callback
            spitfire.callback = spitfire_callback
            cancel.callback = negative_callback

            view = View()
            view.add_item(spitfire)
            view.add_item(kukri)
            view.add_item(paterson)
            view.add_item(prototype)
            view.add_item(lancaster)
            view.add_item(gccarbine)
            view.add_item(gcpistol)
            view.add_item(guitar)
            view.add_item(accordion)
            view.add_item(fiddle)
            view.add_item(trumpet)
            view.add_item(drum)
            view.add_item(harmonica)
            view.add_item(flute)
            view.add_item(bmk)
            view.add_item(cancel)

            em2 = discord.Embed(title="Pick a item to give away!", color=Color.blue())

            await interaction.response.edit_message(view=view, embed=em2)

        else:
            await ctx.send(
                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
            )

    async def level_callback(interaction):
        if interaction.user == ctx.author:
            one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
            two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
            three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
            four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
            five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
            six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
            seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
            eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
            nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
            submit = Button(label="Next", style=discord.ButtonStyle.green, row=4)
            zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
            back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
            cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

            async def one_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(1)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def two_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(2)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def three_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(3)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def four_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(4)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def five_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(5)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def six_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(6)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def seven_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(7)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def eight_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(8)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def nine_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(9)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def zero_callback(interaction):
                if interaction.user == ctx.author:
                    level.append(0)

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def back_callback(interaction):
                if interaction.user == ctx.author:
                    try:
                        level.pop()
                    except IndexError:
                        await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                    em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                        description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            one.callback = one_callback
            two.callback = two_callback
            three.callback = three_callback
            four.callback = four_callback
            five.callback = five_callback
            six.callback = six_callback
            seven.callback = seven_callback
            eight.callback = eight_callback
            nine.callback = nine_callback
            submit.callback = next_callback
            zero.callback = zero_callback
            back.callback = back_callback
            cancel.callback = negative_callback

            view = View()
            view.add_item(one)
            view.add_item(two)
            view.add_item(three)
            view.add_item(four)
            view.add_item(five)
            view.add_item(six)
            view.add_item(seven)
            view.add_item(eight)
            view.add_item(nine)
            view.add_item(submit)
            view.add_item(zero)
            view.add_item(back)
            view.add_item(cancel)

            em3 = discord.Embed(title=f"Level: {''.join(map(str, level))}",
                                description=f"What should be the minimum MEE6 level requirement to join the giveaway?",
                                color=Color.blue())

            await interaction.response.edit_message(view=view, embed=em3)
        else:
            await ctx.send(
                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
            )

    async def next_callback(interaction):
        if interaction.user == ctx.author:
            one = Button(label="1", style=discord.ButtonStyle.primary, row=1)
            two = Button(label="2", style=discord.ButtonStyle.primary, row=1)
            three = Button(label="3", style=discord.ButtonStyle.primary, row=1)
            four = Button(label="4", style=discord.ButtonStyle.primary, row=2)
            five = Button(label="5", style=discord.ButtonStyle.primary, row=2)
            six = Button(label="6", style=discord.ButtonStyle.primary, row=2)
            seven = Button(label="7", style=discord.ButtonStyle.primary, row=3)
            eight = Button(label="8", style=discord.ButtonStyle.primary, row=3)
            nine = Button(label="9", style=discord.ButtonStyle.primary, row=3)
            submit = Button(label="Next", style=discord.ButtonStyle.green, row=4)
            zero = Button(label="0", style=discord.ButtonStyle.primary, row=4)
            back = Button(label="Undo", style=discord.ButtonStyle.grey, row=4)
            cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=4)

            async def one_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(1)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def two_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(2)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def three_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(3)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def four_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(4)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def five_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(5)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def six_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(6)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def seven_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(7)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def eight_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(8)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def nine_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(9)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def zero_callback(interaction):
                if interaction.user == ctx.author:
                    hours.append(0)

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            async def back_callback(interaction):
                if interaction.user == ctx.author:
                    try:
                        hours.pop()
                    except IndexError:
                        await ctx.send(f"There are no numbers to remove {ctx.author.mention}!")

                    em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                        description=f"How long do you want to allow people to join your giveaway?",
                                        color=Color.blue())
                    await interaction.response.edit_message(view=view, embed=em3)
                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            one.callback = one_callback
            two.callback = two_callback
            three.callback = three_callback
            four.callback = four_callback
            five.callback = five_callback
            six.callback = six_callback
            seven.callback = seven_callback
            eight.callback = eight_callback
            nine.callback = nine_callback
            submit.callback = submit_callback
            zero.callback = zero_callback
            back.callback = back_callback
            cancel.callback = negative_callback

            view = View()
            view.add_item(one)
            view.add_item(two)
            view.add_item(three)
            view.add_item(four)
            view.add_item(five)
            view.add_item(six)
            view.add_item(seven)
            view.add_item(eight)
            view.add_item(nine)
            view.add_item(submit)
            view.add_item(zero)
            view.add_item(back)
            view.add_item(cancel)

            em3 = discord.Embed(title=f"Hours: {''.join(map(str, hours))}",
                                description=f"How long do you want to allow people to join your giveaway?",
                                color=Color.blue())

            await interaction.response.edit_message(view=view, embed=em3)
        else:
            await ctx.send(
                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
            )

    async def submit_callback(interaction):
        if interaction.user == ctx.author:
            submit = Button(label="Submit", style=discord.ButtonStyle.green, row=1)
            cancel = Button(label="Never-mind", style=discord.ButtonStyle.red, row=1)

            if hours[0] == 0:
                hours[0] = 1

            if level[0] == 0:
                level[0] = 1

            strings = [str(integer) for integer in hours]
            intMaker = "".join(strings)
            countdown = int(intMaker)

            strings2 = [str(levels) for levels in level]
            intMaker2 = "".join(strings2)
            levelReq = int(intMaker2)

            async def confirm_callback(interaction):
                if interaction.user == ctx.author:
                    channel = client.get_channel(868867431060373514)  # Giveaway: 868867431060373514 | Commands: 782978946735407154

                    em4 = discord.Embed(
                        title=f"{ctx.author.display_name} is giving away a __{var.item}__!",
                        color=Color.blue())
                    em4.set_footer(text="To join the giveaway just react to this message.")
                    em4.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                    em4.add_field(name="Host", value=f"<@!{ctx.author.id}>", inline=False)
                    em4.add_field(name="Level requirement", value=f"{''.join(map(str, level))}", inline=True)
                    em4.add_field(name="Serial", value=f"{''.join(map(str, serial))}", inline=True)
                    em4.add_field(name="Time left", value=f"{''.join(map(str, hours))}:00:00", inline=False)
                    ga = await channel.send(embed=em4)
                    await ga.add_reaction(f"<:haaa:855976143722512425>")

                    joined = []

                    @client.event
                    async def on_reaction_add(reaction, user):
                        if user != client.user:
                            if user != ctx.author:
                                if str(reaction.emoji) == f"<:haaa:855976143722512425>":
                                    with open("users.json", "r") as file:
                                        data = json.load(file)
                                    try:
                                        if int(data["users"][str(user.id)]["lvl"]) >= levelReq:
                                            if joined.__contains__(user.id):
                                                pass
                                            else:
                                                joined.append(user.id)
                                    except KeyError:
                                        await user.send("You have not migrated your MEE6 data. You can migrate by typing any message in chat.")
                                        await reaction.remove(user)
                                    else:
                                        try:
                                            await user.send(f"You must be at least level {''.join(map(str, level))} too join that giveaway!")
                                        except discord.errors.Forbidden:
                                            pass
                                        await reaction.remove(user)
                            else:
                                try:
                                    await user.send(
                                        f"You can't join your own giveaway!")
                                except discord.errors.Forbidden:
                                    pass
                                await reaction.remove(user)

                    @client.event
                    async def on_raw_reaction_remove(payload):
                        member = payload.user_id
                        try:
                            joined.remove(member)
                        except ValueError:
                            pass

                    em3 = discord.Embed(title=f"Submitted",
                                        description=f"You should now see your giveaway in <#868867431060373514>",
                                        color=Color.green())
                    await interaction.response.edit_message(view=None, embed=em3)

                    total_seconds = countdown * 3600 + 0 * 60 + 0
                    total = 0

                    final = total_seconds - total
                    while final > 0:
                        await asyncio.sleep(1)
                        final -= 1
                        final -= client.latency
                        timer = datetime.timedelta(seconds=round(final, 0))

                        em4 = discord.Embed(
                            title=f"{ctx.author.display_name} is giving away a __{var.item}__!",
                            color=Color.blue())
                        em4.set_footer(text="To join the giveaway just react to this message.")
                        em4.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                        em4.add_field(name="Host", value=f"<@!{ctx.author.id}>", inline=False)
                        em4.add_field(name="Level requirement", value=f"{''.join(map(str, level))}", inline=True)
                        em4.add_field(name="Serial", value=f"{''.join(map(str, serial))}", inline=True)
                        em4.add_field(name="Time left", value=f"{timer}", inline=False)
                        await ga.edit(embed=em4)

                    try:
                        winner = random.choice(joined)
                        em5 = discord.Embed(
                            title=f"{ctx.author.display_name} gave away a {var.item}!",
                            color=Color.green())
                        em5.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                        em5.add_field(name="Serial", value=f"{''.join(map(str, serial))}", inline=False)
                        em5.add_field(name="Host", value=f"<@!{ctx.author.id}>", inline=True)
                        em5.add_field(name="Winner", value=f"<@!{winner}>", inline=True)
                        em5.set_footer(
                            text=f"Contact the host through direct messages to claim your prize.\nIf any complications arise contact a moderator or above.\nIf you do not claim your prize withing 3 hours you will not receive it.")
                        await ga.edit(content=f"<@!{winner}>", embed=em5)
                        await ga.reply(f"<@!{winner}>")
                    except IndexError:
                        em5 = discord.Embed(
                            title=f"Nobody joined the giveaway.",
                            description=f"To join the giveaway just react to this message.",
                            color=Color.red())
                        em5.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                        em5.add_field(name="Host", value=f"<@!{ctx.author.id}>")
                        em5.add_field(name="Item", value=f"{var.item}")
                        em5.add_field(name="Serial", value=f"{''.join(map(str, serial))}")
                        await ga.edit(embed=em5)

                else:
                    await ctx.send(
                        f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
                    )

            submit.callback = confirm_callback
            cancel.callback = negative_callback

            view = View()
            view.add_item(submit)
            view.add_item(cancel)

            em3 = discord.Embed(
                title=f"Confirm you want to give away your {var.item} with the serial {''.join(map(str, serial))}",
                description=f"As soon as you press submit there is no going back.",
                color=Color.blue())
            em3.add_field(name="Serial", value=f"{''.join(map(str, serial))}", inline=True)
            em3.add_field(name="Hours the giveaway will last", value=f"{''.join(map(str, hours))}", inline=True)
            em3.add_field(name="Minimum level requirement", value=f"{''.join(map(str, level))}", inline=True)

            await interaction.response.edit_message(view=view, embed=em3)
        else:
            await ctx.send(
                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
            )

    async def negative_callback(interaction):
        if interaction.user == ctx.author:
            em3 = discord.Embed(title="You chose not to host a giveaway.", color=Color.red())

            await interaction.response.edit_message(view=None, embed=em3)
        else:
            await ctx.send(
                f"This isn't your GUI {interaction.user.mention}! If you wish to host a giveaway type **%giveaway**"
            )

    positive.callback = positive_callback
    negative.callback = negative_callback

    view = View()
    view.add_item(positive)
    view.add_item(negative)

    em1 = discord.Embed(title="Would you like to host a giveaway?", color=Color.blue())
    await ctx.reply(view=view, embed=em1)
"""

@client.command()
@commands.has_any_role("Perms", 782962913815822346, 886057517136896013, 778090965042724885, 931924123419025428,
                       931923591765848104, 930668875266281482)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member is None:
        pass
    elif reason is None:
        appealable = Button(label="Yes", style=discord.ButtonStyle.green)
        unappealable = Button(label="No", style=discord.ButtonStyle.red)


        async def appealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been banned in The Marketplace",
                                    description="Basically, you can't be there.",
                                    color=discord.Color.blue())
                embed.add_field(name="Reason", value="No reason provided")
                embed.add_field(name="Appeal", value="[Here](https://discord.gg/GgQTsV6hmK)")
                await member.send(embed=embed)

                await member.ban(reason="No reason provided.")

                embed = discord.Embed(title=f"{member} has been successfully banned.",
                                  description="They can no longer join this server.",
                                  color=discord.Color.green())
                embed.add_field(name="Reason", value="No reason provided")
                embed.add_field(name="Appealable", value="The user is allowed to appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        async def unappealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been banned in The Marketplace",
                                      description="Basically, you can't be there.",
                                      color=discord.Color.blue())
                embed.add_field(name="Reason", value="No reason provided")
                embed.add_field(name="Appeal", value="You are not allowed to appeal.")
                await member.send(embed=embed)

                await member.ban(reason="No reason provided.")

                embed = discord.Embed(title=f"{member} has been successfully perm muted.",
                                      description="They can no longer talk in this server.",
                                      color=discord.Color.green())
                embed.add_field(name="Reason", value="No reason provided.")
                embed.add_field(name="Appealable", value="This user cannot appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        appealable.callback = appealable_callback
        unappealable.callback = unappealable_callback

        view = View()
        view.add_item(appealable)
        view.add_item(unappealable)

        embed = discord.Embed(title=f"Should {member} be allowed to appeal this permanent mute?",
                              description="Appeal means allowed to ask for forgiveness or prove innocence :P",
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed, view=view)
    else:
        appealable = Button(label="Yes", style=discord.ButtonStyle.green)
        unappealable = Button(label="No", style=discord.ButtonStyle.red)

        async def appealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been banned in The Marketplace",
                                      description="Basically, you can't be there.",
                                      color=discord.Color.blue())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appeal", value="[Here](https://discord.gg/GgQTsV6hmK)")
                await member.send(embed=embed)

                await member.ban(reason=reason)

                embed = discord.Embed(title=f"{member} has been successfully banned.",
                                      description="They can no longer join this server.",
                                      color=discord.Color.green())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appealable", value="The user is allowed to appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        async def unappealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been banned in The Marketplace",
                                      description="Basically, you can't be there.",
                                      color=discord.Color.blue())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appeal", value="You are not allowed to appeal.")
                await member.send(embed=embed)

                await member.ban(reason=reason)

                embed = discord.Embed(title=f"{member} has been successfully perm muted.",
                                      description="They can no longer talk in this server.",
                                      color=discord.Color.green())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appealable", value="This user cannot appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        appealable.callback = appealable_callback
        unappealable.callback = unappealable_callback

        view = View()
        view.add_item(appealable)
        view.add_item(unappealable)

        embed = discord.Embed(title=f"Should {member} be allowed to appeal this ban?",
                              description="Appeal means allowed to ask for forgiveness or prove innocence :P",
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed, view=view)


@client.command()
@commands.has_any_role("Perms", 782962913815822346, 886057517136896013, 778090965042724885, 931924123419025428,
                       931923591765848104, 930668875266281482)
async def kick(ctx, user: discord.User = None, *, reason=None):
    if user is None:
        embed = discord.Embed(title="%ban",
                              description="Kick someone from this server",
                              color=discord.Color.blue())
        embed.add_field(name="Commands",
                        value="`%kick <@user or id> <reason>` | Bans a use and allows them to appeal.")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_footer(text="Reason can be left unfilled but user cannot.")
        await ctx.send(embed=embed)

    elif reason is None:
        embed = discord.Embed(title="You have been kicked from The Marketplace",
                              description="Basically, you arent in that server anymore.",
                              color=discord.Color.blue())
        embed.add_field(name="Reason", value="No reason provided")
        embed.add_field(name="Join back", value="[Here](https://discord.gg/APhXvymCsP)")
        await user.send(embed=embed)
    else:
        embed = discord.Embed(title="You have been kicked from The Marketplace",
                                  description="Basically, you arent in that server anymore.",
                                  color=discord.Color.blue())
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Join back", value="[Here](https://discord.gg/APhXvymCsP)")
        await user.send(embed=embed)

    embed = discord.Embed(title=f"{user.name} was kicked successfully.",
                          color=discord.Color.green())
    embed.add_field(name="Reason", value=reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(embed=embed)


@client.command()
@commands.has_any_role(782962913815822346, 787525291723063316, 778254251674566697, 819612121226674236,
                       778090965042724885, 786158305457602600, 848398461602627664, 930668875266281482,
                       931924123419025428, 931923591765848104)
async def whois(ctx, member: discord.Member = None, dm: bool = False):
    if member is None:
        embed = discord.Embed(title="%whois", description="Get the information of a user in this server.",
                              color=Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands",
                        value="`%whois <@user or id>` | Gives information on the user.\n`%whois <@user or id> true` | "
                              "Directly messages you information on the user.",
                        inline=False)
        await ctx.reply(embed=embed)
    elif not dm:
        roles = ""
        get_roles = [role.id for role in member.roles]
        for i in range(len(get_roles)):
            if get_roles[i] not in [847962669797474334, 778090710301802506]:
                roles += f"<@&{str(get_roles[i])}> "
        created_at = member.created_at.strftime("%b %d, %Y")

        embed = discord.Embed(title=f"Who is {member.display_name}",
                              color=Color.blue())
        embed.set_author(name=member.display_name, icon_url=member.avatar)
        embed.set_footer(text="You can get only use %whois if you are a Trial Moderator or above. Plus previous "
                              "moderators, and Flewitt :P")
        embed.add_field(name="User's Profile",
                        value=f"<@!{member.id}>",
                        inline=True)
        embed.add_field(name="Server Display-name",
                        value=f"{member.display_name}",
                        inline=True)
        embed.add_field(name="Discord Username",
                        value=f"{member.name}",
                        inline=True)
        embed.add_field(name="User's discriminator",
                        value=f"{member.discriminator}",
                        inline=True)
        embed.add_field(name="User's full username",
                        value=f"{member}",
                        inline=True)
        embed.add_field(name="User's ID",
                        value=f"{member.id}",
                        inline=True)
        embed.add_field(name="Discord join date",
                        value=created_at,
                        inline=True,
                        )
        embed.add_field(name="Server join date",
                        value=member.joined_at.strftime("%b %d, %Y"),
                        inline=True
                        )
        embed.add_field(name="User's roles",
                        value=f"{roles}",
                        inline=False
                        )
        embed.set_image(url=member.avatar)
        await ctx.reply(embed=embed)
    elif dm:
        roles = ""
        get_roles = [role.name for role in member.roles]
        for i in range(len(get_roles)):
            if get_roles[i] not in ["@everyone"]:
                roles += f"{str(get_roles[i])} "
        created_at = member.created_at.strftime("%b %d, %Y")

        embed = discord.Embed(title=f"Who is {member.display_name}",
                              color=Color.blue())
        embed.set_author(name=member.display_name, icon_url=member.avatar)
        embed.set_footer(text="You can get only use %whois if you are a Trial Moderator or above. Plus previous "
                              "moderators, and Flewitt :P")
        embed.add_field(name="User's Profile",
                        value=f"<@!{member.id}>",
                        inline=True)
        embed.add_field(name="Server Display-name",
                        value=f"{member.display_name}",
                        inline=True)
        embed.add_field(name="Discord Username",
                        value=f"{member.name}",
                        inline=True)
        embed.add_field(name="User's discriminator",
                        value=f"{member.discriminator}",
                        inline=True)
        embed.add_field(name="User's full username",
                        value=f"{member}",
                        inline=True)
        embed.add_field(name="User's ID",
                        value=f"{member.id}",
                        inline=True)
        embed.add_field(name="Discord join date",
                        value=created_at,
                        inline=True,
                        )
        embed.add_field(name="Server join date",
                        value=member.joined_at.strftime("%b %d, %Y"),
                        inline=True
                        )
        embed.add_field(name="User's roles",
                        value=f"{roles}",
                        inline=False
                        )
        embed.set_image(url=member.avatar)
        await ctx.author.send(embed=embed)


@client.command(aliases=['levelroles'])
async def levelrole(ctx):
    with open("users.json", "r") as file:
        data = json.load(file)

    msg = await ctx.reply("Giving you your level roles. This may take a few seconds.")

    lvl = int(data["users"][str(ctx.author.id)]["lvl"])

    if lvl >= 1:
        role = ctx.guild.get_role(931328684927881256)
        await ctx.author.add_roles(role)

    if lvl >= 5:
        role = ctx.guild.get_role(931328858857291797)
        await ctx.author.add_roles(role)

    if lvl >= 10:
        role = ctx.guild.get_role(931334495104282654)
        await ctx.author.add_roles(role)

    if lvl >= 15:
        role = ctx.guild.get_role(930800945217011722)
        await ctx.author.add_roles(role)

    if lvl >= 20:
        role = ctx.guild.get_role(931329139963752469)
        await ctx.author.add_roles(role)

    if lvl >= 30:
        role = ctx.guild.get_role(931332181538783322)
        await ctx.author.add_roles(role)

    if lvl >= 40:
        role = ctx.guild.get_role(931332403241300088)
        await ctx.author.add_roles(role)

    if lvl >= 50:
        role = ctx.guild.get_role(931332515581550693)
        await ctx.author.add_roles(role)

    await msg.edit("You have received your level roles.")
    await asyncio.sleep(5)
    await msg.delete()


@client.command()
async def ping(ctx):
    await ctx.reply(f"{round(client.latency * 1000)}ms")


@client.command()
@commands.has_any_role("Perms", 782962913815822346, 886057517136896013, 778090965042724885,
                       930668875266281482, 787525291723063316, 931924123419025428, 931923591765848104)
async def pmute(ctx, member: discord.Member, *, reason=None):
    if member is None:
        pass
    elif reason is None:
        appealable = Button(label="Yes", style=discord.ButtonStyle.green)
        unappealable = Button(label="No", style=discord.ButtonStyle.red)


        async def appealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been permanently muted in The Marketplace",
                                    description="Basically, you cant talk there.",
                                    color=discord.Color.blue())
                embed.add_field(name="Reason", value="No reason provided")
                embed.add_field(name="Appeal", value="[Here](https://discord.gg/GgQTsV6hmK)")
                await member.send(embed=embed)

                role = get(ctx.author.guild.roles, name="Muted")
                await member.add_roles(role)

                embed = discord.Embed(title=f"{member} has been successfully perm muted.",
                                  description="They can no longer talk in this server.",
                                  color=discord.Color.green())
                embed.add_field(name="Reason", value="No reason provided")
                embed.add_field(name="Appealable", value="The user is allowed to appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        async def unappealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been permanently muted in The Marketplace",
                                      description="Basically, you cant talk there.",
                                      color=discord.Color.blue())
                embed.add_field(name="Reason", value="No reason provided.")
                embed.add_field(name="Appeal", value="You cannot appeal this.")
                await member.send(embed=embed)

                role = get(ctx.author.guild.roles, name="Muted")
                await member.add_roles(role)

                embed = discord.Embed(title=f"{member} has been successfully perm muted.",
                                      description="They can no longer talk in this server.",
                                      color=discord.Color.green())
                embed.add_field(name="Reason", value="No reason provided.")
                embed.add_field(name="Appealable", value="This user cannot appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        appealable.callback = appealable_callback
        unappealable.callback = unappealable_callback

        view = View()
        view.add_item(appealable)
        view.add_item(unappealable)

        embed = discord.Embed(title=f"Should {member} be allowed to appeal this permanent mute?",
                              description="Appeal means allowed to ask for forgiveness or prove innocence :P",
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed, view=view)
    else:
        appealable = Button(label="Yes", style=discord.ButtonStyle.green)
        unappealable = Button(label="No", style=discord.ButtonStyle.red)

        async def appealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been permanently muted in The Marketplace",
                                      description="Basically, you cant talk there.",
                                      color=discord.Color.blue())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appeal", value="[Here](https://discord.gg/GgQTsV6hmK)")
                await member.send(embed=embed)

                role = get(ctx.author.guild.roles, name="Muted")
                await member.add_roles(role)

                embed = discord.Embed(title=f"{member} has been successfully perm muted.",
                                      description="They can no longer talk in this server.",
                                      color=discord.Color.green())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appealable", value="The user is allowed to appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        async def unappealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been permanently muted in The Marketplace",
                                  description="Basically, you cant talk there.",
                                  color=discord.Color.blue())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appeal", value="You cannot appeal this.")
                await member.send(embed=embed)

                role = get(ctx.author.guild.roles, name="Muted")
                await member.add_roles(role)

                embed = discord.Embed(title=f"{member} has been successfully perm muted.",
                                  description="They can no longer talk in this server.",
                                  color=discord.Color.green())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appealable", value="This user cannot appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        appealable.callback = appealable_callback
        unappealable.callback = unappealable_callback

        view = View()
        view.add_item(appealable)
        view.add_item(unappealable)

        embed = discord.Embed(title=f"Should {member} be allowed to appeal this permanent mute?",
                              description="Appeal means allowed to ask for forgiveness or prove innocence :P",
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed, view=view)


@client.command()
@commands.has_any_role("Perms", 782962913815822346, 886057517136896013, 778090965042724885,
                       930668875266281482, 787525291723063316, 931924123419025428, 931923591765848104)
async def mute(ctx, member: discord.Member, days, hours, mins, *, reason=None):
    try:
            days = int(days)
            hours = int(hours)
            mins = int(mins)
    except ValueError:
        embed = discord.Embed(title="%mute",
                              description="Mute someone from talking in this server for a certain time.",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands",
                        value="`%mute <@user or id> <days> <hours> <minutes> <reason>` | Mutes someone for a certain time.")
        await ctx.send(embed=embed)
        return


    if member is None:
        pass
    elif reason is None:
        appealable = Button(label="Yes", style=discord.ButtonStyle.green)
        unappealable = Button(label="No", style=discord.ButtonStyle.red)


        async def appealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title=f"You have been muted in The Marketplace.",
                                    description="Basically, you cant talk there.",
                                    color=discord.Color.blue())
                embed.add_field(name="Reason", value="No reason provided")
                embed.add_field(name="Appeal", value="[Here](https://discord.gg/GgQTsV6hmK)")
                embed.add_field(name="Time", value=f"{days} days, {hours} hours and {mins} minutes.")
                embed.set_footer(text="If you are not muted after the time you are supposed to be unmuted give or take 30 mins. Contact a moderator or Flewitt")
                await member.send(embed=embed)

                role = get(ctx.author.guild.roles, name="Muted")
                await member.add_roles(role)
                await asyncio.sleep((days * 86400) + (hours * 3600) + (mins * 60))
                await member.remove_roles(role)

                embed = discord.Embed(title=f"{member} has been successfully muted.",
                                  description="They can no longer talk in this server.",
                                  color=discord.Color.green())
                embed.add_field(name="Reason", value="No reason provided")
                embed.add_field(name="Appealable", value="The user is allowed to appeal.")
                embed.add_field(name="Time", value=f"{days} days, {hours} hours and {mins} minutes.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        async def unappealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been muted in The Marketplace",
                                      description="Basically, you cant talk there.",
                                      color=discord.Color.blue())
                embed.add_field(name="Reason", value="No reason provided.")
                embed.add_field(name="Appeal", value="You cannot appeal this.")
                embed.add_field(name="Time", value=f"{days} days, {hours} hours and {mins} minutes.")
                embed.set_footer(text="If you are not muted after the time you are supposed to be unmuted give or take 30 mins. Contact a moderator or Flewitt")
                await member.send(embed=embed)

                role = get(ctx.author.guild.roles, name="Muted")
                await member.add_roles(role)
                await asyncio.sleep((days * 86400) + (hours * 3600) + (mins * 60))
                await member.remove_roles(role)

                embed = discord.Embed(title=f"{member} has been successfully muted.",
                                      description="They can no longer talk in this server.",
                                      color=discord.Color.green())
                embed.add_field(name="Reason", value="No reason provided.")
                embed.add_field(name="Appealable", value="This user cannot appeal.")
                embed.add_field(name="Time", value=f"{days} days, {hours} hours and {mins} minutes.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        appealable.callback = appealable_callback
        unappealable.callback = unappealable_callback

        view = View()
        view.add_item(appealable)
        view.add_item(unappealable)

        embed = discord.Embed(title=f"Should {member} be allowed to appeal this mute?",
                              description="Appeal means allowed to ask for forgiveness or prove innocence :P",
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed, view=view)
    else:
        appealable = Button(label="Yes", style=discord.ButtonStyle.green)
        unappealable = Button(label="No", style=discord.ButtonStyle.red)

        async def appealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been muted in The Marketplace",
                                      description="Basically, you cant talk there.",
                                      color=discord.Color.blue())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appeal", value="[Here](https://discord.gg/GgQTsV6hmK)")
                embed.add_field(name="Time", value=f"{days} days, {hours} hours and {mins} minutes.")
                embed.set_footer(text="If you are not muted after the time you are supposed to be unmuted give or take 30 mins. Contact a moderator or Flewitt")
                await member.send(embed=embed)

                role = get(ctx.author.guild.roles, name="Muted")
                await member.add_roles(role)
                await asyncio.sleep((days * 86400) + (hours * 3600) + (mins * 60))
                await member.remove_roles(role)

                embed = discord.Embed(title=f"{member} has been successfully muted.",
                                      description="They can no longer talk in this server.",
                                      color=discord.Color.green())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appealable", value="The user is allowed to appeal.")
                embed.add_field(name="Time", value=f"{days} days, {hours} hours and {mins} minutes.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        async def unappealable_callback(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(title="You have been muted in The Marketplace",
                                  description="Basically, you cant talk there.",
                                  color=discord.Color.blue())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appeal", value="You cannot appeal this.")
                embed.add_field(name="Time", value=f"{days} days, {hours} hours and {mins} minutes.")
                embed.set_footer(text="If you are not muted after the time you are supposed to be unmuted give or take 30 mins. Contact a moderator or Flewitt")
                await member.send(embed=embed)

                role = get(ctx.author.guild.roles, name="Muted")
                await member.add_roles(role)
                await asyncio.sleep((days * 86400) + (hours * 3600) + (mins * 60))
                await member.remove_roles(role)

                embed = discord.Embed(title=f"{member} has been successfully muted.",
                                  description="They can no longer talk in this server.",
                                  color=discord.Color.green())
                embed.add_field(name="Reason", value=reason)
                embed.add_field(name="Appealable", value="This user cannot appeal.")
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message("You arent allowed to press this button.", ephemeral=True)

        appealable.callback = appealable_callback
        unappealable.callback = unappealable_callback

        view = View()
        view.add_item(appealable)
        view.add_item(unappealable)

        embed = discord.Embed(title=f"Should {member} be allowed to appeal this mute?",
                              description="Appeal means allowed to ask for forgiveness or prove innocence :P",
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed, view=view)


@client.command()
@commands.has_any_role("Perms", 782962913815822346, 886057517136896013, 778090965042724885,
                       930668875266281482, 787525291723063316, 931924123419025428, 931923591765848104)
async def unmute(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title="%unmute",
                              description="Unmute someone from this server, allows them to talk basically.",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands", value="`%unmute <@user or id>` | Unmutes someone.")
        await ctx.send(embed=embed)
    else:
        role = get(ctx.author.guild.roles, name="Muted")
        await member.remove_roles(role)

        embed = discord.Embed(title=f"{member} has been successfully unmuted.",
                              description="They can talk in this server now.",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

        embed = discord.Embed(title=f"You were unmuted in The Marketplace",
                              description="You can talk in this server now.",
                              color=discord.Color.blue())

        await member.send(embed=embed)


@client.command()
@commands.has_any_role("Perms", 782962913815822346, 886057517136896013, 778090965042724885, 931924123419025428,
                       931923591765848104)
async def unban(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title="%unban",
                              description="Unbans someone from this server, allows them to join basically.",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands", value="`%unban <@user or id>` | Unbans someone.")
        await ctx.send(embed=embed)
    else:
        await member.unban()

        embed = discord.Embed(title=f"{member} has been successfully unbanned.",
                              description="They can join this server now.",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

        embed = discord.Embed(title=f"You were unbanned in The Marketplace",
                              description="You can join this server now.",
                              color=discord.Color.blue())
        embed.add_field(name="Server", value="(Here)[https://discord.gg/APhXvymCsP]")

        await member.send(embed=embed)


@client.command()
@commands.has_any_role("Perms", 886057517136896013, 778090965042724885, 930668875266281482, 931924123419025428,
                       931923591765848104)
async def say(ctx, channel: discord.TextChannel = None, *, message=None):
    if message is None:
        embed = discord.Embed(title="Say command",
                              description="Say something through It's Ez in a certain channel",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.set_footer(text="Why was this message prompted? It's because you left message unfilled.")
        embed.add_field(name="Format", value="%say <#channel or id> <message>")
        await ctx.send(embed=embed)
    else:
        await channel.send(message)

    await ctx.message.delete()


@client.command()
@commands.has_any_role("Perms", 886057517136896013, 778090965042724885, 930668875266281482, 931924123419025428,
                       931923591765848104)
async def embed(ctx, channel: discord.TextChannel = None, *, message=None):
    if message is None:
        embed = discord.Embed(title="Say command",
                              description="Say something through It's Ez in a certain channel",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.set_footer(text="Why was this message prompted? It's because you left message unfilled.")
        embed.add_field(name="Format", value="%embed <#channel or id> <message>")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="",
                              description=f"{message}",
                              color=discord.Color.random())
        await channel.send(embed=embed)

    await ctx.message.delete()


@say.error
async def say_error(ctx, error):
    if isinstance(error, ChannelNotFound):
        embed = discord.Embed(title="%say",
                              description="Say something through It's Ez in a certain channel.",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands", value="`%say <#channel or id> <message>` | Says something in a specified "
                                               "channel")
        await ctx.send(embed=embed)
    await ctx.message.delete()


@embed.error
async def embed_error(ctx, error):
    if isinstance(error, ChannelNotFound):
        embed = discord.Embed(title="%embed",
                              description="Say something through It's Ez in a certain channel in an embed.",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands", value="`%embed <#channel or id> <message>` | Says something through a embed "
                                               "in a specified channel")
        await ctx.send(embed=embed)
    await ctx.message.delete()


@pmute.error
async def pmute_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="%pmute",
                              description="Permanently mute someone from talking in this server.",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands", value="`%pmute <@user or id> <reason>` | Permanently mutes someone")
        await ctx.send(embed=embed)


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="%mute",
                              description="Mute someone from talking in this server for a certain time.",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands", value="`%mute <@user or id> <days> <hours> <minutes> <reason>` | Mutes someone for a certain time.")
        await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="%ban",
                              description="Ban someone from this server.",
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.add_field(name="Commands", value="`%ban <@user or id> <reason>` | Bans someone")
        await ctx.send(embed=embed)


@dm.error
async def invoke_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        pass


client.run('OTI2ODI4MDI4OTk3MzA0MzUw.YdBV3Q.ti2uyFD95unyC9h9zByYWLVjDDg')
