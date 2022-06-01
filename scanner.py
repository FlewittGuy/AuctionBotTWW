import pytesseract as tess        # https://tesseract-ocr.github.io/tessdoc/
import pyautogui                  # https://pyautogui.readthedocs.io/en/latest/
from PIL import Image             # https://pillow.readthedocs.io/en/stable/
import argparse
import keyboard
import json
import re
import time
import win32gui
import numpy as np
from datetime import datetime
from timeit import default_timer as timer
from pywinauto import mouse                                      # https://pywinauto.readthedocs.io/en/latest/
from cv2 import cvtColor, inRange, bitwise_or, COLOR_BGR2HSV     # https://pypi.org/project/opencv-python/
import inspect
import sqlite3

# import sys
# from win32api import GetSystemMetrics
# import traceback
# import logging

from misc import system_exit                 # Import our custom exit handler from misc.py; replaces sys.exit()
from constants import *                      # Import project constant declarations from constants.py
from sqlite_db import *                      # Experimental: log detections into a SQLite database (just implemented)

# Note: compile using: pyinstaller -F -i scanner.ico scanner.py

# Pip3 Packages and Modules:
# pytesseract, opencv-python, pyautogui, pywin32, pillow, keyboard, timeit, numpy, pywinauto, inspect, psutil.
# Note: pywin32 includes both win32gui and win32api
#
# Tesseract installer for Windows:          https://github.com/UB-Mannheim/tesseract/wiki
# Python pywin32 documentation:             http://timgolden.me.uk/pywin32-docs/index.html
# MSDN Win32 Api winuser.h documentation:   https://docs.microsoft.com/en-us/windows/win32/api/winuser/

config_file = "data.json"  # Session file used by bot-scanner interface (generated)
items_file = "items.json"  # Items to track
scanner_config_file = "scanner_config.json"  # Scanner configuration settings
scanner_db_file = "scanner_data.db"  # Experimental logging of detects to a SQlite database

tess_directory = r'C:\Users\Libra\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
tess.pytesseract.tesseract_cmd = tess_directory


# Get command line options using argparse
parser = argparse.ArgumentParser(description='ThatOneGuy Roblox Standalone Scanner 1.0')
parser.add_argument('-d0', '--debug0',
                    action='store_true',
                    help='Debug: save timestamped item/serial pair for each detect pass after item event occurs')
parser.add_argument('-d1', '--debug1',
                    action='store_true',
                    help='Debug: save timestamped pre-item screen image for each pass')

args = parser.parse_args()

# Set to true when debugging actual item detections using command line -d0 option
# Writes 3 timestamped files for each item detection to the image_debug directory
# Disk intensive; writes multiple files
debug0 = args.debug0

# Set to true to save pre-item scan using command line -d1 option
# Allows troubleshooting area of screen being scanned for both item and serial text; saves to image_debug directory
# Disk intensive; writes multiple files
debug1 = args.debug1

pause_was_pressed = False        # Flag to exit scanner program on Pause key pressed


# Set a global keyboard hook to exit program on Pause key pressed (i.e. keyboard focus is in Roblox window)
def keyboard_handler(key):
    global pause_was_pressed
    pause_was_pressed = True


# Class used by detect() function; initial values are populated from items.json
class DetectData:
    def __init__(self, item, item_key, serial_min, serial_next, serial_coord, comment, detect_item, item_coord):
        self.item = item                         # "Spitfire Revolving Sniper"
        self.item_key = item_key                 # "Spit" Tess OCR keyword
        self.serial_min = serial_min             # 4677; last known good serial
        self.serial_next = serial_next           # 5; threshold for serial
        self.serial_coord = serial_coord         # [350, 418, 56, 25] = [x, y, width, height]
        self.serial_last = 0                     # Last detection using scanner
        self.serial_image_file = None            # Last detection filename
        self.serial_detect_time = None           # Last detection timestamp
        self.detect = detect_item                # Detect item True or False
        self.item_coord = item_coord             # Not really needed; scanner setting; = [x, y, width, height]
        self.comment = comment                   # "SPITFIRE!"


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


# Save a single key value to a config file (inefficient when saving multiple keys)
def save_data(file_name, key, key_value):
    with open(file_name) as g:
        data1 = json.load(g)
    data1[key] = key_value
    with open(file_name, "w") as g:
        json.dump(data1, g)


# Return a single key value from a config file
def load_data_key(file_name, key):
    with open(file_name) as g:
        data1 = json.load(g)
    key_value = data1[key]
    return key_value


# Original function: not currently used in scanner; passing directly to Tess instead
def save_screenshot(x1, x2, x3, x4, img):
    ss = pyautogui.screenshot(region=(x1, x2, x3, x4))
    ss.save(img)


def click_at(x1, y1):
    mouse.click(button='left', coords=(x1, y1))


def detect(counter, master_coord, item_coord, item_list):

    print(f"[{counter}] Detect pass")

    status_code = 0

    # No need to save screen image to file unless we detect item (or are debugging)
    # Pass in-memory image directly to Tesseract OCR for processing

    # Take single screenshot that contains both item and serial (less chance of errors)
    slot0 = pyautogui.screenshot(region=master_coord)

    # Crop item_coord text out of the slot0 master screenshot
    x1 = master_coord
    x2 = item_coord
    xy_rect_item = [x2[0] - x1[0], x2[1] - x1[1], x2[0] - x1[0] + x2[2], x2[1] - x1[1] + x2[3]]
    slot1 = slot0.crop(xy_rect_item)

    # Experimental: Image processing to improve accuracy using OpenCV cv2
    # Creates a mask for the Magenta coloured text and applies to the cropped item screenshot

    img = np.array(slot1)                           # Convert screenshot (RGB) to numpy image array for OpenCV cv2
    hsv = cvtColor(img, COLOR_BGR2HSV)              # Convert image array to HSV (Hue, Saturation, Value)
    lower_range = np.array([134, 119, 100])         # Lower range magenta text (using imutils range-detector) (119 vs 120 detects fiddle)
    upper_range = np.array([200, 212, 255])         # Upper range magenta text (using imutils range-detector)
    mask = inRange(hsv, lower_range, upper_range)   # Create mask on Magenta colored text (the range needed is finicky)
    new_slot1 = bitwise_or(img, img, mask=mask)     # Apply mask to our screenshot to remove background
    new_slot1 = Image.fromarray(new_slot1, 'RGB')   # Convert image array to an RGB image todo check if i need line..

    text = tess.image_to_string(new_slot1)          # Submit modified image to Tesseract OCR

    display = text
    print(f"[{counter}] Detect [{display.strip()}]")        # Strip linefeed to print

    # Save timestamped copy of all pre-item detection images for debugging only...
    if debug1:
        slot0.save(f"image_debug/{time.strftime('%Y%m%d_%H%M%S')}_pre_item.png")

    # Check if text contains any DetectData p0 item_keys in the item_list; first match wins.
    p1 = None
    item_list_no = 0
    for p0 in item_list:
        if text.__contains__(p0.item_key) and p0.detect:
            p1 = p0
            break
        item_list_no += 1

    # If a p1 match was found; look for serial number corresponding to that type of item
    if p1 is not None:

        status_code = 1

        detect_time = datetime.now()
        time_stamp = detect_time.strftime('%Y%m%d_%H%M%S')

        print(f"\n[{counter}] {p1.comment} {str(detect_time)} Last serial: {p1.serial_last}")  # Comment i.e. SPITFIRE!

        # Crop serial_coord serial out of the slot0 master screenshot
        x1 = master_coord
        x2 = p1.serial_coord
        xy_rect_serial = [x2[0] - x1[0], x2[1] - x1[1], x2[0] - x1[0] + x2[2], x2[1] - x1[1] + x2[3]]
        slot2 = slot0.crop(xy_rect_serial)

        # Save timestamped copy of master / item / serial detection images for debugging only...
        if debug0:
            file_debug_stamp = f"image_debug/{time_stamp}_"
            slot0.save(f"{file_debug_stamp}master.png")
            slot1.save(f"{file_debug_stamp}item.png")
            slot2.save(f'{file_debug_stamp}serial.png')

        # Possible preimage processing on serial number for better ocr; not needed (should probably remove background).
        # Current settings seem to work well

        # https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
        serial_text = tess.image_to_string(slot2, config='--psm 10 --oem 3 -c tessedit_char_whitelist=#0123456789')

        display = serial_text
        print(f"[{counter}] Serial detected by Tesseract: {display.strip()}")   # Strip linefeed to print

        serial_text = [int(s) for s in re.findall(r'\d+', serial_text)]         # Return list of integers found
        print(f"[{counter}] Serial after processing     : {serial_text}")

        if len(serial_text) >= 1:
            if serial_text[0] > p1.serial_last and serial_text[0] > p1.serial_min:
                if p1.serial_last == 0 or serial_text[0] <= (p1.serial_last + p1.serial_next):
                    print(f"[{counter}] Scanner is saving {serial_text[0]}\n")

                    status_code = 2
                    p1.serial_last = serial_text[0]

                    serial_file_name = f"image_scan/{time_stamp}_serial.png"    # keep; used by bot etc.
                    item_file_name = f"image_scan/{time_stamp}_item.png"        # debug: comment out line if not needed

                    slot1.save(item_file_name)                                  # debug: comment out line if not needed
                    slot2.save(serial_file_name)
                    p1.serial_image_file = serial_file_name
                    p1.serial_detect_time = detect_time.isoformat()

                    session = get_json_data(config_file)
                    if session is None:
                        print(f"ERROR: There was a problem reading the '{config_file}' file. Exiting scanner.")
                        system_exit(1)

                    data1 = session['detect_items'][p1.item]
                    data1['serial'] = serial_text[0]
                    data1['serial_detect_time'] = detect_time.isoformat()   # Needs to be in isoformat to save to json
                    data1['serial_image_file'] = serial_file_name

                    # Could have potential collisions with the bot reading here... not handled
                    # Could replace section with a database that supports concurrent access i.e. SQLite or MySQL
                    # Note: I have not seen any collisions yet
                    try:
                        with open(config_file, "w") as g:
                            json.dump(session, g)
                    except OSError as e:
                        print(f"ERROR: There was a problem writing the '{config_file}' file. Exiting scanner.")
                        system_exit(1)

                    # Experimental: log the detection info into a SQLite database...
                    # ---------------------------------------------------------
                    global session_key
                    global session_timestamp
                    conn = sqlite3.connect(scanner_db_file)
                    conn.execute(f"INSERT INTO scanner_detect (session_key, session_start, item, serial, serial_detect_time, serial_image_file) \
                            VALUES ({session_key}, '{session_timestamp}', '{p1.item}', {serial_text[0]}, '{detect_time.isoformat()}', '{serial_file_name}')")
                    conn.commit()
                    conn.close()
                    # ---------------------------------------------------------

                else:
                    status_code = 100
                    print(f"[{counter}] Ignore {serial_text[0]} Reason: > {p1.serial_last} + {p1.serial_next}\n")

            else:
                status_code = 101
                print(f"[{counter}] Ignore {serial_text[0]} Reason: not > {p1.serial_last} and > {p1.serial_min}\n")

        else:
            status_code = 102
            print(f"[{counter}] Ignore {serial_text} Reason: Tesseract OCR returned no serial\n")

        # Save the modified p1 DetectData object back into the item_list
        # todo in this case the p1 obj directly modified the item_list object so line probably not needed...
        item_list[item_list_no] = p1

    counter += 1
    return counter, status_code, item_list       # Return the modified item_list


if __name__ == '__main__':

    print("ThatOneGuy Roblox Standalone Scanner 1.0\n")

    count = 0

    # Experimental: log all detections into a SQlite database...  Use DB Browser for SQLite to browse
    initialize_scanner_data_db(scanner_db_file)

    # Get overall scanner configuration settings from scanner_config.json
    scanner_data = get_json_data(scanner_config_file)
    if scanner_data is None:
        print(f"ERROR: There was a problem reading the '{scanner_config_file}' file. Exiting scanner.")
        system_exit(1)

    # Screen coordinates to detect items; modify scanner_config.json and items.json w different screen coordinates

    xy_master_coord = scanner_data['master_coord_xy']
    xy_item_coord = scanner_data['item_coord_xy']

    # Get the item list to detect from items.json; modify details, coordinates and whether to detect the item or not
    # Manually update last known good item serial number for each item.
    # All detected serials for the specific item must be higher than this value; i.e. 4500
    # Manually update threshold range for the next detected serial for each item
    # Otherwise assume bad detection i.e 5

    detect_item_list = []
    items = get_json_data(items_file)
    if items is None:
        print(f"ERROR: There was a problem reading the '{items_file}' file. Exiting scanner.")
        system_exit(1)

    # Create a custom DetectData object for each item to detect; assign all items to the array detect_item_list
    # DetectData serial_last defaults to 0 for each item; updated on first item detection.
    # If a bad high detection serial OCR occurs on first detect it will create issues...

    for i in items:
        # DetectData(item, item_key, serial_min, serial_next, serial_coord, comment, detect_item, xy_item_coord):
        if items[i][5]:   # only load items we want to track
            pobj = DetectData(i, items[i][0], items[i][1], items[i][2], items[i][3], items[i][4], items[i][5], xy_item_coord)
            detect_item_list.append(pobj)

    if len(detect_item_list) == 0:
        print(f"You must track at least one item from 'items.json' by setting detect to true. Exiting scanner.")
        system_exit(1)

    # Initialize data.json for new session with items we want to find; manually set true or false in items.json
    # Unique session key each time scanner starts; used by bot for session control

    session_key = timer()
    session_timestamp = datetime.now().isoformat()
    session_dict = {"session_key": session_key, "session_start": session_timestamp, "detect_items": ""}

    new_dict = {}
    for i in items:        # Loop through items and build our initial data.json file
        if items[i][5]:    # If items[i][5] is True we will track this item; manually set true or false in items.json
            new_dict[i] = {"serial": 0, "serial_detect_time": "", "serial_image_file": ""}

    session_dict['detect_items'] = new_dict
    try:
        with open(config_file, "w") as f:
            json.dump(session_dict, f)
    except OSError as e:
        print(f"ERROR: There was a problem initializing the '{config_file}' file. Exiting scanner.")
        system_exit(1)

    # Note: xy coordinates will change on diff size screens if Roblox not 800x600; manually modify scanner_config.json
    slot_location_xy = scanner_data['slot_location_xy']

    # Run Roblox at 800 x 600 (816 x 638)
    roblox_screen_xy = scanner_data['roblox_screen_xy']

    print(f"Sleeping for 10 seconds... You will lose control of the mouse after that...\n")

    time.sleep(10)  # Time for the user to do things before mouse moves...

    print(f"Press Pause key to stop scanner.\n")

    # Experimental: Position Roblox in top left corner sized to 800x600 (816 x 638)
    # Note: Logan's original locations will not work with this running... see xy_screenshot.py
    # screen_width = GetSystemMetrics(0)
    # screen_height = GetSystemMetrics(1)
    hwnd = win32gui.FindWindow(None, 'Roblox')

    if hwnd == 0:
        print(f"ThatOneGuy Scanner program requires Roblox to be running...")
        print(f"The user needs to be playing the game 'The Secret Game - Secret Level'.")
        print(f"The user needs to be pre-positioned looking at the Secret display.")
        print(f"The scanner program will automatically position and size the Roblox window.")
        system_exit(0)

    win32gui.ShowWindow(hwnd, SW_SHOWNORMAL)        # SW_SHOWNORMAL = 1 (from constants.py)
    # win32gui.SetForegroundWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0 - 8, 0, roblox_screen_xy[0], roblox_screen_xy[1], True)     # 8 is left border

    # Need to use a global key hook since keyboard focus is in Roblox window
    keyboard.hook_key('pause', keyboard_handler, suppress=False)

    while count >= 0:

        # Performs a single cycle through the Robolox slot locations
        for index, xy in enumerate(slot_location_xy):

            print(f"[{count}] Moving mouse to slot location {index}:{xy}...")

            time.sleep(0.1)

            # Click slot location 2-5 times before calling detect (2 seems to work; todo)
            for i in range(2):
                click_at(xy[0], xy[1])

            time.sleep(2)       # Wait for right-hand panel; needs to be 2-3 seconds for refresh

            # Returns status codes in status_return
            #  0 = No detection
            #  1 = Detected item but no serial number
            #  2 = Detected new item and new serial number; saved to data.json
            #  100,101,102 Detected item but serial ignored for various reasons

            count, status_return, detect_item_list = detect(count, xy_master_coord, xy_item_coord, detect_item_list)

            time.sleep(1)        # Insert delay because we can; output is smoother

            # Note the previous call to detect will finish before exiting to allow a clean exit
            if pause_was_pressed:
                keyboard.unhook_key('pause')
                print(f"\nPause key was pressed. Stopping scanner...")

                system_exit(0)  # Custom exit handler
