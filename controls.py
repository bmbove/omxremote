#!/usr/bin/python
import time
import os
import sqlite3
import subprocess

conn = sqlite3.connect("remote.db")
cursor = conn.cursor()

def start(executable, file_key, p):
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

    cmd_tup = [executable, '-fs', path[0]]
    pipe = subprocess.PIPE

    if executable == '/usr/bin/omxplayer':
        try:
            os.remove('fifo')
            os.mkfifo('fifo')
        except:
            sys.exit("Could not create pipe 'fifo'")
        cmd_tup = [exectuable, '-o hdmi', path[0], '< fifo', '&']
        pipe = os.open('fifo', os.O_RDONLY|os.O_NONBLOCK)

    p = subprocess.Popen(cmd_tup, stdin=pipe)
    if executable == '/usr/bin/omxplayer':
        pipe_write = os.open('fifo', os.O_WRONLY|os.O_NONBLOCK)
        pipe_write.write('.')
    while get_playing() != path[1]:
        update_status('playing', path[1])
    while p.poll() != None:
        time.sleep(1)
    return p

def send_cmd(p, cmd):
    #pipe_write = os.open('fifo', os.O_WRONLY|os.O_NONBLOCK)
    try:
        p.stdin.write(cmd)
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
    if recurse == 1:
        dirs = os.walk(path)
        for directory in dirs:
            for filename in directory[2]:
                if os.path.splitext(filename)[1] in file_exts:
                    #print directory[0].strip() + "/" + filename.strip()
                    full_path = directory[0].strip() + "/" + filename.strip()
                    name = os.path.splitext(filename)[0]
                    ext = os.path.splitext(filename)[1]
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
