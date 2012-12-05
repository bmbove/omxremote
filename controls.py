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
    print fifo_exists
    if fifo_exists == False:
        try:
            os.mkfifo('fifo')
        except OSError:
            os.remove('fifo')
            os.mkfifo('fifo')
    
    if os.path.isfile('omxremote.db') == False:
        
if __name__ == '__main__':
    startup_checks()
    #conn = sqlite3.connect("omxremote.db")
    #cursor = conn.cursor()
    #create table
    #cursor.execute("""CREATE TABLE library
    #                    (key, file, size)
    #                """)

    #cursor.execute("INSERT INTO library VALUES ('1', 'home/brian/Music/The Wallflowers - Cinderella.mp3', '383420')")
    #conn.commit()
    #sql = "SELECT file FROM library WHERE key=1"
    #for row in cursor.execute(sql):
    #    print row
    #    file = row[0]
    #print file
    if sys.argv[1] == 'start':
        start("/home/brian/Music/The Wallflowers - Cinderella.mp3")
    if sys.argv[1] == 'pause':
        pause()
    if sys.argv[1] == 'stop':
        os.system('echo -n "q" > fifo')


