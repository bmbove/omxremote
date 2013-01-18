#!/usr/bin/python
import time
import os
import sqlite3
import subprocess
import sys

conn = sqlite3.connect("remote.db")
cursor = conn.cursor()

def playlist_add(key):
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_keys FROM playlists WHERE key = 1")
    row = cursor.fetchone()
    new_keys = str(row[0]) + str(key)
    cursor.execute("UPDATE playlists SET file_keys = ? WHERE key = 0", [new_keys])
    conn.commit()

def start(executable, cmd_args, file_key, p):
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()

    try:
        while p.poll() == None:
            send_cmd(p, "q")
            update_status("stopped")
    except:
        pass

    cursor.execute("SELECT path, name FROM library WHERE key=?", [file_key])
    path = cursor.fetchone()
    try:
        os.remove('fifo')
    except:
        pass
    try:
        os.mkfifo('fifo')
    except:
        sys.exit("Could not create pipe 'fifo'")
    cmd_tup = [executable]
    path_list = [path[0]]
    cmd_tup = cmd_tup + cmd_args.split(' ')
    cmd_tup = cmd_tup + path_list
    print cmd_tup
    pipe = os.open('fifo', os.O_NONBLOCK)

    p = subprocess.Popen(cmd_tup, stdin=pipe)

    while get_playing() != path[1]:
        update_status('playing', path[1])

    while p.poll() != None:
        time.sleep(1)
    return p

def send_cmd(p, cmd):
    try:
        with open("fifo","w") as fp:
            fp.write(cmd)
    except:
        pass
    return p

def update_status(status, name='None'):
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()
    while (get_status() != status and get_playing() != name):
        cursor.execute("UPDATE status SET status=?, name=?", [status, name])
        conn.commit()

def get_status():
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()
    result = cursor.execute("SELECT status FROM status")
    return result.fetchone()[0]

def get_playing():
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()
    result = cursor.execute("SELECT name FROM status")
    return result.fetchone()[0]

def process_status(p):
    try:
        return p.poll()
    except:
        return True 

def add_path_to_library(path, recurse = 1):
    file_exts = ['.mp3', '.avi', '.mp4', '.mkv', '.flac']
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()
    recurse = 1
    if recurse == 1:
        for root, dirs, files in os.walk(path):
            print "Root:"
            print root
            print "Dirs:"
            print dirs
            print "Files:"
            print files
            for filename in files:
                if os.path.splitext(filename)[1] in file_exts:
                    name = os.path.splitext(filename)[0]
                    full_path = root + "/" + filename.strip()
                    ext = os.path.splitext(filename)[1]
                    print full_path
                    size = os.path.getsize(full_path)
                    try:
                        cursor.execute("INSERT INTO library (name, path, type, size) VALUES ( ?, ?, ?, ?)", [name, full_path, ext, size])
                    except sqlite3.IntegrityError:
                        continue
    else:
        for filename in os.listdir(path):
            if os.path.splitext(filename)[1] in file_exts:
                full_path = path.stip() + filename.strip()
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1]
                size = os.path.getsize(full_path)
                try:
                    cursor.execute("INSERT INTO library (name, path, type, size) VALUES (?, ?, ?, ?)", [name, full_path, ext, size])
                except:
                    pass
    conn.commit()
