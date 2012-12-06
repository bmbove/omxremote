#!/usr/bin/python
import sys
import time
import os
import sqlite3
import stat

def start(file):
    cmd = 'mplayer "' + file + '" < fifo > /dev/null 2>&1 &'
    os.system(cmd)
    os.system('echo -n . > fifo')

def pause():
        os.system('echo -n "p" > fifo')

def startup_checks():

    # Check if pipe exists. If not, create it.
    try:
        fifo_exists = stat.S_ISFIFO(os.stat('fifo').st_mode)
    except OSError as e:
        fifo_exists = False 
    if fifo_exists == False:
        try:
            os.mkfifo('fifo')
        except OSError:
            os.remove('fifo')
            os.mkfifo('fifo')
    
    # Check if sqlite db file exists. If not... initialize it.
    if os.path.isfile('omxremote.db') == False:
        conn = sqlite3.connect("omxremote.db")
        cursor = conn.cursor()
        sql = "CREATE TABLE library (key INTEGER PRIMARY KEY AUTOINCREMENT, name, path UNIQUE, type, size)"
        cursor.execute(sql)
        conn.commit()
    else:
        conn = sqlite3.connect("omxremote.db")
        cursor = conn.cursor()
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='library'"
        cursor.execute(sql)
        cursor.fetchall()
        if cursor.rowcount == 0:
            cursor.execute("CREATE TABLE library (key INTEGER PRIMARY KEY AUTOINCREMENT, name, path UNIQUE, type, size)")
            conn.commit()

def add_path_to_library(path, recurse = 1):
    file_exts = ['.mp3', '.avi', '.mp4', '.mkv', '.flac']
    conn = sqlite3.connect("omxremote.db")
    cursor = conn.cursor()
    dirs = os.walk(path)
    if recurse == 1:
        for directory in dirs:
            for filename in directory[2]:
                if os.path.splitext(filename)[1] in file_exts:
                    #print directory[0].strip() + "/" + filename.strip()
                    path = directory[0].strip() + "/" + filename.strip()
                    name = os.path.splitext(filename)[0]
                    ext = os.path.splitext(filename)[1]
                    size = os.path.getsize(path)
                    try:
                        cursor.execute("INSERT INTO library (name, path, type, size) VALUES ( ?, ?, ?, ?)", (name, path, ext, size))
                    except sqlite3.IntegrityError:
                            continue
    conn.commit()


if __name__ == '__main__':
    startup_checks()

    if sys.argv[1] == 'start':
        start("/home/brian/Music/The Wallflowers - Cinderella.mp3")
    if sys.argv[1] == 'pause':
        pause()
    if sys.argv[1] == 'stop':
        os.system('echo -n "q" > fifo')
    if sys.argv[1] == 'next':
        os.system('echo -n "" > fifo')
    #add_path_to_library("/home/brian/usb")


