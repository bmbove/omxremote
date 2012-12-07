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
    update_status('playing')

def pause():
    os.system('echo -n "p" > fifo')

def stop():
    os.system('echo -n "q" > fifo')
    update_status('stopped')

def update_status(status):
    conn = sqlite3.connect("omxremote.db")
    cursor = conn.cursor()
    sql = "UPDATE status SET status='" + status + "'"
    cursor.execute(sql)
    conn.commit()

def get_status():
    conn = sqlite3.connect("omxremote.db")
    cursor = conn.cursor()
    result = cursor.execute("SELECT status FROM status")
    return result.fetchone()[0]

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


