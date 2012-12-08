import cherrypy
import os
import sys
import stat
import jinja2
import controls
import sqlite3
import subprocess
import time

env = jinja2.Environment(loader = jinja2.FileSystemLoader('./templates'))

p = False
exit = 0

def startup_checks():

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
    def index(self, play = 0, stop = 0, quit = 0):
        global p
        global exit
        exit = quit
        conn = sqlite3.connect("omxremote.db")
        conn.text_factory = str
        cursor = conn.cursor()
        print play
        if play > 0:
            sql = "SELECT path FROM library WHERE key=" + play
            cursor.execute(sql)
            path = cursor.fetchone()
            p = controls.start(path[0], p)

        if stop > 0:
             controls.stop(p)
        if quit > 0:
            sys.exit("Exiting omxremote")

        template = env.get_template("index.html")
        sql = "SELECT key, path FROM library"
        cursor.execute(sql)
        row = cursor.fetchall()
        return template.render(files=row)

    index.exposed = True

startup_checks()

cherrypy.config.update(
    {'server.socket_host': '0.0.0.0'})
cherrypy.engine.signal_handler.subscribe()
cherrypy.tree.mount(omxremote(), '/')
cherrypy.engine.start()

while 1:
    if exit > 0:
        sys.exit("Exiting omxremote")
    try:
        if p.poll() != None:
            controls.update_status('stopped')
       # print p.poll()
    except:
        pass
    #time.sleep(1)
#cherrypy.quickstart(omxremote())
