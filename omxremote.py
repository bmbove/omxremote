import cherrypy
import os
import sys
import stat
import jinja2
import controls
import sqlite3

env = jinja2.Environment(loader = jinja2.FileSystemLoader('./templates'))

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
    conn = sqlite3.connect("omxremote.db")
    cursor = conn.cursor()
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='library'"
    cursor.execute(sql)
    cursor.fetchall()
    if cursor.rowcount == 0:
        cursor.execute("CREATE TABLE library (key INTEGER PRIMARY KEY AUTOINCREMENT, name, path UNIQUE, type, size)")
        conn.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS status (key PRIMARY KEY, status)")
    cursor.execute("INSERT OR REPLACE INTO status VALUES ('0', 'stopped')")
    conn.commit()

class omxremote:
    def index(self, play = 0, stop = 0):
        conn = sqlite3.connect("omxremote.db")
        conn.text_factory = str
        cursor = conn.cursor()
        print play
        if play > 0:
            if controls.get_status()  == 'playing':
                controls.stop()

            sql = "SELECT path FROM library WHERE key=" + play
            cursor.execute(sql)
            path = cursor.fetchone()
            controls.start(path[0])
            controls.pause()

        if stop > 0:
            controls.stop()

        template = env.get_template("index.html")
        sql = "SELECT key, path FROM library"
        cursor.execute(sql)
        row = cursor.fetchall()
        return template.render(files=row)

    index.exposed = True

startup_checks()

cherrypy.quickstart(omxremote())

