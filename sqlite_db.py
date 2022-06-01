# Experimental: log detection and notification info into a SQLite database instead of a .log text file
# Use SQLite DB Browser to browse the rows

import sqlite3
import os
import sys


def initialize_scanner_data_db(database_name):
    if os.path.isfile(database_name):
        print(f"Scanner is using existing SQLite scanner database {database_name}...\n")
    else:
        print(f"SQLite scanner database not found: initializing new database '{database_name}'...\n")
        create_scanner_data_db(database_name)


def create_scanner_data_db(database_name):
    conn = sqlite3.connect(database_name)

    conn.execute('''CREATE TABLE scanner_detect (
                id INTEGER NOT NULL UNIQUE,
                session_key         REAL NOT NULL,
                session_start       TEXT NOT NULL,
                item                TEXT NOT NULL,
                serial              INT NOT NULL,
                serial_detect_time  TEXT NOT NULL,
                serial_image_file   TEXT NOT NULL,
                PRIMARY KEY(id AUTOINCREMENT));''')

    # Not used; could potentially replace data.json (single row)
    conn.execute('''CREATE TABLE "bot_interface" (
                id	INTEGER NOT NULL UNIQUE,
                session_key         REAL NOT NULL,
                session_start       TEXT NOT NULL,
                json                TEXT NOT NULL,
                PRIMARY KEY(id));''')

    # Not used; could log send notifications in bot; may need to use aiosqlite?
    conn.execute('''CREATE TABLE "bot_log" (
                id  INTEGER NOT NULL UNIQUE,
                notification_time   TEXT NOT NULL,
                item                TEXT NOT NULL,
                serial              INT NOT NULL,
                serial_detect_time  TEXT NOT NULL,
                serial_image_file   TEXT NOT NULL,
                session_key         REAL NOT NULL,
                PRIMARY KEY(id AUTOINCREMENT));''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    sys.exit(0)
