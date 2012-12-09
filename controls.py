#!/usr/bin/python
import sys
import time
import os
import sqlite3
import stat
import subprocess

conn = sqlite3.connect("remote.db")
cursor = conn.cursor()

def start(executable, file_key, p):
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()
    try:
        while p.poll() == None:
            stop(p)
    except:
        pass
    cursor.execute("SELECT path, name FROM library WHERE key=?", [file_key])
    path = cursor.fetchone()

    cmd_tup = [executable, path[0]]
    p = subprocess.Popen(cmd_tup, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    update_status('playing', path[1])
    while p.poll() != None:
        time.sleep(1)
    return p

def pause(p):
    try:
        p.stdin.write("p")
    except:
        pass

def stop(p):
    try:
        p.terminate()
    except:
        pass
    update_status("stopped")
    return p

def update_status(status, name='None'):
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()
    while get_status() != status:
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
