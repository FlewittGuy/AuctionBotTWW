import discord
import asyncio
from discord.ext import tasks, commands
import aiohttp
import os
import sys
import io
import re
import time
from datetime import datetime, timedelta
import json
import pyautogui
import pytesseract as tess
from cv2 import cvtColor, inRange, bitwise_or, COLOR_BGR2HSV
from PIL import Image
import numpy as np
import inspect

# from timeit import default_timer as timer
# import traceback
# import logging

from misc import system_exit                        # Import our custom exit handler from misc.py; replaces sys.exit()

# Note: compile using: pyinstaller -F -i bot.ico bot.py
# Note: inspect.stack()[0][3] shows the current function name when printing errors; easier to rename functions

print("Auction Discord Bot 2.3\n")


my_id = 460513933741260800  # Bot owner's client_id (i.e. DarkStar#8280 = 923096402232475658)
owners = [460513933741260800, 923096402232475658]  # Multiple bot owners Flewitt#9028 & DarkStar#8280
bot_config_filename = "bot_config.json"  # Settings to configure the overall bot tasks
data_json_filename = "data.json"  # Method1 scanner.py interface file data.json

bot = commands.Bot(command_prefix='%', owner_ids=set(owners), case_insensitive=True)

TOKEN = 'YOUR TOKEN HERE'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="chess with Mr.Z"))


# Get the latest data from any config .json file; returns None if it fails
def get_json_data(file_name):
    try:
        with open(file_name, "r") as g:
            data = json.load(g)
            return data
    except (FileNotFoundError, OSError, json.decoder.JSONDecodeError) as e:
        # Print current function name + error; calling function is inspect.stack()[1][3]
        print(f"ERROR {inspect.stack()[0][3]}: {e}")
        return None


@bot.command(name='test1', help='Responds with some text')
@commands.is_owner()        # made it owner only for now to stop spamming
async def test1_handler(ctx):
    response = "Stop spamming the --test1 command"
    await ctx.send(response)


@bot.command(name='test2', help='Sends an image or file from the bot server')
@commands.is_owner()        # made it owner only for now to stop spamming
async def test2_handler(ctx):
    response = f"{ctx.author}\nSending an image or file from the bot server..."
    await ctx.send(response)

    # Example of bot sending a specific image file stored on the computer; check that file exists
    file_name = "images/demon.png"
    if os.path.isfile(file_name):
        await ctx.send(file=discord.File(file_name))
    else:
        await ctx.send(f"{ctx.author}\nFilename '{file_name}' does not exist on bot server")


@test2_handler.error
async def test2_handler_error(ctx, error):
    print(f"ERROR[--test2]: {error}")


@bot.command(name='test3', help='Gets an image or file from a web server using AIOHTTP and sends')
@commands.is_owner()        # made it owner only for now to stop spamming
async def test3_handler(ctx):
    response = f"{ctx.author}\nSending a copy of an image or file downloaded from a web server on the internet ..."
    await ctx.send(response)

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://slm-assets.secondlife.com/assets/10725048/lightbox/Devil.jpg?1417868056") as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())

            # Do any processing on file here etc. Image editing, OCR, web scraping, beautifulsoup, whatever...

            await ctx.send(file=discord.File(data, 'demon.png'))


@test3_handler.error
async def test3_handler_error(ctx, error):
    print(f"ERROR[--test3]: {error}")
    await ctx.send(f"{ctx.author}\nThere was an error retrieving the image or file from the server.")


@bot.command(name='test4', help='Checks if a Minecraft username exists')
@commands.is_owner()        # made it owner only for now to stop spamming
async def test4_handler(ctx, username: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as resp:
            if resp.status == 200:
                data = io.BytesIO(await resp.read())
                json_file = json.load(data)
                await ctx.send(
                    f"{ctx.author}\nThe Minecraft username '{username}' exists.\n\nUsername: {json_file['name']}\nUUID: {json_file['id']}")
            elif resp.status == 204:
                await ctx.send(f"{ctx.author}\nThe Minecraft username '{username}' does not exist...")
            elif resp.status == 429:
                await ctx.send(f"{ctx.author}\nTry again in 10 minutes; the api.Mojang.com server is rate limited...")
            else:
                await ctx.send(f"{ctx.author}\nCould not get information about '{username}' from api.Mojang.com.")


@test4_handler.error
async def test4_handler_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author}\nYou forgot to supply the username...')
    else:
        print(f"ERROR[--test4]: {error}")
        await ctx.send(f"{ctx.author}\nThere was an error contacting the api.Mojang.com server...")


@bot.command(name='test5', help='Start & stop different types of background tasks (owner only)')
@commands.is_owner()
async def test5_handler(ctx):
    response = "Testing the --test5 command"

    global bot_task_list

    # Start or stop a background task that was created with loop.create_task() using our bot_task_list
    bot_process = 'example1'
    if bot_process in bot_task_list:
        if bot_task_list[bot_process] in asyncio.all_tasks():
            bot_task_list[bot_process].cancel()                  # stop
        await bot_task_list.pop(bot_process, None)                     # remove entry in bot_task_list dictionary
    else:
        bot_task_list[bot_process] = bot.loop.create_task(task_example1())  # start

    # Start or stop a @tasks.loop background task; runs every 10 seconds for 5 times
    bot_process = 'example2'
    if bot_process in bot_task_list:
        if bot_task_list[bot_process] in asyncio.all_tasks():
            bot_task_list[bot_process].cancel()                   # stop
        await bot_task_list.pop(bot_process, None)                      # remove entry in bot_task_list dictionary
    else:
        bot_task_list[bot_process] = task_example2.start()        # start

    await ctx.send(response)


@bot.command(name='test6', help='Miscellaneous Testing (owner only)')
@commands.is_owner()
async def test6_handler(ctx):
    response = "Testing the --test6 command"

    # Miscellaneous testing

    await ctx.send(response)


# Could use @commands.is_owner() here; did it differently as an example.
@bot.command(name='shutdown', help='Shutdown the bot (owner only)')
@commands.is_owner()        # made it owner only for now to stop spamming
async def shutdown_handler(ctx):
    if ctx.author.id == my_id:
        shutdown_embed = discord.Embed(title='Bot Update', description='I am now shutting down.', color=0x8ee6dd)
        await ctx.channel.send(embed=shutdown_embed)
        await bot.close()
        time.sleep(1)  # This allows the bot to shut down properly without exception errors (do not use asyncio here)
    else:
        error_embed = discord.Embed(title='Access Denied!', description='This command is owner only.', color=0xFF0000)
        error_embed.set_footer(text=ctx.author)
        await ctx.channel.send(embed=error_embed, delete_after=10.0)


@bot.command(name='stop', help='Stop specific bot process (owner only)')
@commands.is_owner()
async def stop_handler(ctx, bot_process: str):  # i.e. --stop scanner1
    global bot_task_list

    # Stop a background task that was created with loop.create_task() using our bot_task_list
    if bot_process in bot_task_list:
        if bot_task_list[bot_process] in asyncio.all_tasks():
            bot_task_list[bot_process].cancel()                      # cancel task
            await bot_task_list.pop(bot_process, None)                     # remove entry in bot_task_list dictionary

            print(f"INFO[--stop]: Process {bot_process} is stopping [{ctx.author}]")
            stop_embed = discord.Embed(title='Bot Update', description=f'Stopping bot process {bot_process}', color=0x8ee6dd)
            await ctx.channel.send(embed=stop_embed)

        else:
            await bot_task_list.pop(bot_process, None)    # remove entry for tasks that already finished (todo improve?)
            await ctx.channel.send(f"{ctx.author}\nTask {bot_process} is not currently running or has finished")
    else:
        await ctx.channel.send(f"{ctx.author}\nProcess {bot_process} is not a running process")


@stop_handler.error
async def stop_handler_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        # print(error.param.name)  # this is the name of the missing argument
        await ctx.send(f'{ctx.author}\nYou forgot to supply which bot process to stop...')
    elif isinstance(error, commands.NotOwner):
        await ctx.send(f'{ctx.author}\nThis command is owner only.')


@bot.command(name='start', help='Start specific bot process (owner only)')
@commands.is_owner()
async def start_handler(ctx, bot_process: str):  # i.e. --start scanner1
    global bot_task_list
    valid_process_list = ["scanner1", "scanner2", "example1", "example2"]

    if bot_process in valid_process_list:

        # Start a background task and update our bot_task_list
        if bot_process not in bot_task_list:
            if bot_process == 'scanner1':
                bot_task_list[bot_process] = bot.loop.create_task(scan_interface_task())

            elif bot_process == 'scanner2':
                bot_task_list[bot_process] = bot.loop.create_task(scan_background_task())

            elif bot_process == 'example1':
                bot_task_list[bot_process] = bot.loop.create_task(task_example1())

            elif bot_process == 'example2':
                task_example2.change_interval(seconds=20)       # Note: have not found a way to override the count...
                bot_task_list[bot_process] = task_example2.start()

            print(f"INFO[--start]: Process {bot_process} is starting [{ctx.author}]")
            start_embed = discord.Embed(title='Bot Update', description=f'Starting bot process {bot_process}', color=0x8ee6dd)
            await ctx.channel.send(embed=start_embed)
        else:
            await ctx.channel.send(f"{ctx.author}\nProcess {bot_process} is already started; use --stop to end process")
    else:
        await ctx.channel.send(f"{ctx.author}\nProcess {bot_process} is not a valid process")


@start_handler.error
async def start_handler_error(ctx, error):
    # Note check commands. for other possible exceptions to handle in any command error handler
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author}\nYou forgot to supply which bot process to start...')
    elif isinstance(error, commands.NotOwner):
        await ctx.send(f'{ctx.author}\nThis command is owner only.')


# The on_error exception handler receives unhandled exceptions thrown by @bot.event functions
# Use try except blocks in your event code to handle expected errors
@bot.event
async def on_error(event, *args, **kwargs):
    # Debugging; nothing is being handled here; see what exceptions get fired in our events

    message = args[0]  # Gets the error message object
    print(f"ERROR[on_error] Event:{event} Message:{message}")
    exc_type, value, traceback = sys.exc_info()
    print("     Exception type:", exc_type)
    print("     Exception value:", value)
    print("     Exception traceback object:", traceback)


# Method2: Experimental single item scan detection in the bot itself i.e. Spitfire only etc.
# Background Tesseract OCR scanner task (todo mouse / click / pause key / Roblox stuff or rely on other click software)
async def scan_background_task():
    await bot.wait_until_ready()

    global bot_config_filename

    tess_directory = r'C:\Users\Libra\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    channel = 944574398466236446
    spitfire_role = 923367131129741342
    counter = 0

    # Get bot configuration settings from bot_config.json; returns None if failed
    data = get_json_data(bot_config_filename)
    if data is None:
        print(f"ERROR {inspect.stack()[0][3]}: cannot access bot_config.json file; stopping task")
        return  # End scan_background_task

    # Updated on first item detection; if bad high detection occurs on first detect it will create issues...
    serial_last = 0

    # Get single item to track in bot
    item_name = data['item_name']
    item_key = data['item_key']
    item_comment = data['item_comment']

    # Last known good item serial number
    # All detected serials must be higher than this value; from bot_config.json i.e. 4500
    serial_min = data['serial_item_min']

    # Threshold for next detected serial, or assume bad detection; from bot_config.json i.e. 5
    serial_next = data['serial_item_next']

    # Screen coordinates for the item & serial screenshots; from bot_config.json
    master_coord = data['master_coord']
    item_coord = data['item_coord']
    serial_coord = data['serial_coord']

    tess.pytesseract.tesseract_cmd = tess_directory

    channel = bot.get_channel(channel)

    while not bot.is_closed():

        print(f"[{counter}] Detect pass")

        # Take single screenshot that contains both item and serial (less chance of errors)
        slot0 = pyautogui.screenshot(region=master_coord)

        # Crop item_coord text out of the slot0 master screenshot
        x1 = master_coord
        x2 = item_coord
        xy_rect_item = [x2[0] - x1[0], x2[1] - x1[1], x2[0] - x1[0] + x2[2], x2[1] - x1[1] + x2[3]]
        slot1 = slot0.crop(xy_rect_item)

        # Experimental: Image processing to improve accuracy using OpenCV cv2
        # Creates a mask for the Magenta coloured text and applies to the screenshot

        img = np.array(slot1)                           # Convert screenshot (RGB) to numpy image array for OpenCV cv2
        hsv = cvtColor(img, COLOR_BGR2HSV)              # Convert image array to HSV (Hue, Saturation, Value)
        lower_range = np.array([134, 119, 100])         # Lower range magenta text (using imutils range-detector)
        upper_range = np.array([200, 212, 255])         # Upper range magenta text (using imutils range-detector)
        mask = inRange(hsv, lower_range, upper_range)   # Create mask on Magenta colored text (the range is finicky)
        new_slot1 = bitwise_or(img, img, mask=mask)     # Apply mask to our screenshot to remove background
        new_slot1 = Image.fromarray(new_slot1, 'RGB')   # Convert image array to an RGB image todo check if i need line

        text = tess.image_to_string(new_slot1)          # Submit modified image to Tesseract OCR

        if text.__contains__(item_key):

            timestamp = datetime.now()

            print(f"[{counter}] {item_comment} {str(timestamp)} Last serial: {serial_last}")

            # Crop serial_coord serial out of the slot0 master screenshot
            x2 = serial_coord
            xy_rect_serial = [x2[0] - x1[0], x2[1] - x1[1], x2[0] - x1[0] + x2[2], x2[1] - x1[1] + x2[3]]
            slot2 = slot0.crop(xy_rect_serial)

            # Possible preimage processing on serial number for better ocr (only if needed);
            # Seems to work pretty well w my test screenshots
            serial_text = tess.image_to_string(slot2, config='--psm 10 --oem 3 -c tessedit_char_whitelist=#0123456789')

            display = serial_text
            print(f"[{counter}] Serial detected by Tesseract: {display.strip()}")  # Strip linefeed

            serial_text = [int(s) for s in re.findall(r'\d+', serial_text)]
            print(f"[{counter}] Serial after processing     : {serial_text}")

            if len(serial_text) >= 1:
                if serial_text[0] > serial_last and serial_text[0] > serial_min:
                    if serial_last == 0 or serial_text[0] <= (serial_last + serial_next):
                        print(f"[{counter}] Bot is sending {serial_text[0]}\n")

                        # Create a discord.File object using an in-memory bytes buffer with the in-memory serial image
                        # No need to save the image to disk; send file with the embed
                        arr = io.BytesIO()
                        slot2.save(arr, format='PNG')
                        arr.seek(0)
                        file = discord.File(fp=arr, filename='serial.png')
                        ping = "Error"
                        ping = "Error"
                        if "Spitfire" in str(item_name):
                            ping = 918686580535869511
                            color = discord.Color.from_rgb(255, 121, 121)
                        elif "Chain Pistol" in str(item_name):
                            ping = 921566023809892392
                            color = discord.Color.from_rgb(255, 255, 0)
                        elif "Chain Carbine" in str(item_name):
                            ping = 921566032148172860
                            color = discord.Color.from_rgb(255, 188, 0)
                        elif "Paterson" in str(item_name):
                            ping = 921566054369595474
                            color = discord.Color.from_rgb(255, 255, 255)
                        elif "Prototype" in str(item_name):
                            ping = 921566015081578537
                            color = discord.Color.from_rgb(159, 81, 12)
                        elif "Lancaster" in str(item_name):
                            ping = 921565737141801000
                            color = discord.Color.from_rgb(95, 95, 95)
                        elif "Kukri" in str(item_name):
                            ping = 1
                            color = discord.Color.from_rgb(108, 19, 175)

                        em = discord.Embed(title=f"__**Notification**__", color=color)
                        em.add_field(name="**Time**", value=f"<t:{int(time.time())}>", inline=False)
                        em.add_field(name="**Item**", value=f"{item_name}", inline=True)
                        em.add_field(name="**Serial**", value=f"#{serial_text[0]}", inline=True)
                        em.set_footer(text=f"Go to #reaction-roles to be notified when any item you want appears in auction.")

                        serial_last = serial_text[0]
                        msg = await channel.send(content=f"<@&{ping}>", embed=em)
                        msg.publish()

                    else:
                        print(f"[{counter}] Ignore {serial_text[0]} Reason: > {serial_last} + {serial_next}\n")

                else:
                    print(f"[{counter}] Ignore {serial_text[0]} Reason: not > {serial_last} and > {serial_min}\n")

            else:
                print(f"[{counter}] Ignore {serial_text} Reason: Tesseract OCR returned no serial\n")

        counter += 1
        await asyncio.sleep(20)  # Task runs every 20 seconds


# Method1: Background task scan_interface using data.json
# Separate scanner.py program updating data.json
async def scan_interface_task():
    await bot.wait_until_ready()

    global data_json_filename

    channel = 944574398466236446
    spitfire_role = 923367131129741342
    counter = 0

    data = get_json_data(data_json_filename)
    if data is None:
        print(f"ERROR {inspect.stack()[0][3]}: cannot access data.json file; stopping task")
        return  # End scan_interface_task

    last_session = data['session_key']          # Get the unique scanner session key
    last_detect_items = data['detect_items']    # Get a copy of the current data.json file
    print(f"Scan interface task initialized using session key: {last_session}")

    channel = bot.get_channel(channel)

    while not bot.is_closed():

        print(f"[{counter}] Detect pass using data.json")

        # Could have collision here if scanner writing data.json at same time as bot reading
        # Could replace section with a database that supports concurrent access i.e. SQLite or MySQL
        # Could replace with an AIOHTTP Client (i.e. bot is client / scanner is server) etc.
        # I have not seen any collisions, seems to work pretty well.

        data = get_json_data(data_json_filename)  # Returns None if failed; get data next pass...

        if data is not None:
            if data['session_key'] == last_session:
                for i in data['detect_items']:
                    item_new = data['detect_items'][i]
                    item_last = last_detect_items[i]

                    if item_new['serial'] > item_last['serial']:
                        print(f"[{counter}] Bot is sending [{item_new['serial_detect_time']}] '{i}' Serial: {item_new['serial']}")

                        # Use try except blocks for normal error handling in tasks
                        try:
                            file = discord.File(item_new['serial_image_file'], filename='serial.png')
                        except FileNotFoundError as e:
                            file = None
                            print(f"ERROR {inspect.stack()[0][3]}: {e}")

                        ping = "Error"
                        if "Spitfire" in str(i):
                            ping = 918686580535869511
                            color = discord.Color.from_rgb(255, 121, 121)
                        elif "Chain Pistol" in str(i):
                            ping = 921566023809892392
                            color = discord.Color.from_rgb(255, 255, 0)
                        elif "Chain Carbine" in str(i):
                            ping = 921566032148172860
                            color = discord.Color.from_rgb(255, 188, 0)
                        elif "Paterson" in str(i):
                            ping = 921566054369595474
                            color = discord.Color.from_rgb(255, 255, 255)
                        elif "Prototype" in str(i):
                            ping = 921566015081578537
                            color = discord.Color.from_rgb(159, 81, 12)
                        elif "Lancaster" in str(i):
                            ping = 921565737141801000
                            color = discord.Color.from_rgb(95, 95, 95)
                        elif "Kukri" in str(i):
                            ping = 967380212226605087
                            color = discord.Color.from_rgb(108, 19, 175)

                        em = discord.Embed(title=f"__**Notification**__", color=color)
                        em.add_field(name="**Time**", value=f"<t:{int(time.time())}>", inline=False)
                        em.add_field(name="**Item**", value=f"{i}", inline=True)
                        em.add_field(name="**Serial**", value=f"#{item_new['serial']}", inline=True)
                        em.set_footer(text=f"Go to #reaction-roles to be notified when any item you want appears in auction.")

                        item_last['serial'] = item_new['serial']
                        item_last['serial_detect_time'] = item_new['serial_detect_time']
                        item_last['serial_image_file'] = item_new['serial_image_file']
                        msg = await channel.send(content=f"<@&{ping}>", embed=em)
                        msg.publish()

                    else:
                        pass  # ignore

            else:
                # Re-initialize session data with new session data; scanner was restarted
                data = get_json_data(data_json_filename)
                if data is None:
                    print(f"ERROR {inspect.stack()[0][3]}: cannot access data.json file; stopping task")
                    return  # End scan_interface_task

                print(f"Scan interface task session key changed: Last: {last_session} New Session: {data['session_key']}")
                last_session = data['session_key']
                last_detect_items = data['detect_items']
                # Session changed up to 30 seconds ago; we want to send anything the scanner picked up in that period
                # They will get sent next loop...
                for i in last_detect_items:
                    last_detect_items[i]['serial'] = 0
                    last_detect_items[i]['serial_detect_time'] = ""
                    last_detect_items[i]['serial_image_file'] = ""

        else:
            print(f"ERROR {inspect.stack()[0][3]}: no data.json data: skip loop")

        counter += 1
        await asyncio.sleep(30)  # Task runs every 30 seconds


# ---------------------------------------------------------------------------------------------------
# This is one example of a background task; this does absolutely nothing...
async def task_example1():
    await bot.wait_until_ready()
    counter = 0

    while not bot.is_closed():
        print(f"[{counter}] INFO task_example1 is running...")
        counter += 1

        # add your code here

        await asyncio.sleep(15)  # Task runs every 15 seconds


# ---------------------------------------------------------------------------------------------------
# This is a different example of a background task using @tasks.loop and a different way of starting
# Repeat task after every 10 seconds; exit after 5 loops; has a before and after function if needed
@tasks.loop(seconds=10, count=5)
async def task_example2():
    # Do stuff
    print(f"[{task_example2.current_loop}] INFO task_example2 is running... ")


@task_example2.before_loop
async def task_example2_before_loop():
    # Initialize
    print("INFO: task_example2: I am starting...")


@task_example2.after_loop
async def task_example2_after_loop():
    # Cleanup
    print("INFO: task_example2: I am finished...")
# ---------------------------------------------------------------------------------------------------


# Custom Task Manager dictionary; used to start and stop custom background tasks
# Note: I should replace this with a custom TaskManager Class and methods todo ...
bot_task_list = {}

# You can have multiple background tasks running at the same time; create a loop for each one.
# Note: Choose which scan process to run i.e. Method 1 or Method 2 (only run one of these at a time)

# Method1: Background scan_interface_task using data.json (working)
bot_task_list['scanner1'] = bot.loop.create_task(scan_interface_task())
# bot.loop.create_task(scan_interface_task())

# Method2: Experimental spitfire scan detection in the bot itself (todo mouse / click / pause / Roblox stuff or rely on other click software)
#bot_task_list['scanner2'] = bot.loop.create_task(scan_background_task())

# Example background task #1; (see --test5, --start, --stop)
# bot_task_list['example1'] = bot.loop.create_task(task_example1())

# Example background task #2; (see --test5, --start, --stop)
# bot_task_list['example2'] = task_example2.start()


# The bot.run() call blocks until closed using --shutdown (or program is terminated) etc.
# Note: The discord token is stored in the Windows environment table

bot.run(TOKEN)

# Note: Could implement batch file bot --restart command using sys.exit() codes etc..
print("ThatOneGuy is exiting...")
system_exit(0)
