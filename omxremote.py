import cherrypy
import os
import sys
import stat
import jinja2
import controls
import sqlite3
import subprocess
import time

current_dir = os.path.dirname(os.path.abspath(__file__))

def startup_checks():
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()

    # Check if sqlite db file exists. If not... initialize it.
    cursor.execute("CREATE TABLE IF NOT EXISTS library (key INTEGER PRIMARY KEY AUTOINCREMENT, name, path UNIQUE, type, size)")
    cursor.execute("CREATE TABLE IF NOT EXISTS status (key PRIMARY KEY, status, name)")
    cursor.execute("INSERT OR REPLACE INTO status VALUES ('0', 'stopped', 'None')")
    cursor.execute("CREATE TABLE IF NOT EXISTS library_paths (key PRIMARY KEY, path, recurse, monitor)")
    cursor.execute("CREATE TABLE IF NOT EXISTS playlists (key PRIMARY KEY, name, file_keys)")
    cursor.execute("CREATE TABLE IF NOT EXISTS config (key PRIMARY KEY, port, executable)")
    cursor.execute("INSERT OR IGNORE INTO config VALUES (?, ?, ?)", [0, 8080, '/usr/bin/mplayer'])
    conn.commit()

def load_config():
    global port
    global executable
    conn = sqlite3.connect("remote.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM config")
    row = cursor.fetchone()
    port = row[1]
    executable = row[2]

class omxremote:
    def index(self, pause = 0, play = 0, stop = 0, quit = 0):
        global p
        global exit
        global env
        exit = quit

        conn = sqlite3.connect("remote.db")
        cursor = conn.cursor()

        if play > 0:
            p = controls.start(executable, play, p)

        if stop > 0:
             controls.stop(p)

        if quit > 0:
            sys.exit("Exiting omxremote")

        if pause > 0:
            controls.pause(p)

        template = env.get_template("index.tpl")
        sql = "SELECT key, path FROM library"
        cursor.execute(sql)
        row = cursor.fetchall()
        return template.render(playing=controls.get_playing())

    def style(self):
        f = open('templates/style.css', 'r')
        cherrypy.response.headers['Content-Type'] = 'text/css'
        return f.read()
 
    def music(self):
        conn = sqlite3.connect("remote.db")
        cursor = conn.cursor()
        template = env.get_template("filelist.tpl")
        sql = "SELECT key, name FROM library WHERE type='.mp3' OR type='.flac' OR type='.wav'"
        cursor.execute(sql)
        row = cursor.fetchall()
        return template.render(playing=controls.get_playing(), files = row)
    
    def videos(self):
        conn = sqlite3.connect("remote.db")
        cursor = conn.cursor()
        template = env.get_template("filelist.tpl")
        sql = "SELECT key, name FROM library WHERE type='.mp4' OR type='.avi' OR type='.mkv'"
        cursor.execute(sql)
        row = cursor.fetchall()
        return template.render(playing=controls.get_playing(), files = row)

    def settings(self):
        return "settings"

    def search(self):
        return "search"
    index.exposed = True
    style.exposed = True
    music.exposed = True
    videos.exposed = True
    settings.exposed = True
    search.exposed = True


def main():
    global env
    env = jinja2.Environment(loader = jinja2.FileSystemLoader('./templates'))

    # Define globals
    global p
    p = False
    global exit
    exit = 0
    global port
    port = 0
    global executable
    executable = ''

    startup_checks()
    load_config()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print os.path.join(current_dir, 'templates', 'images')
    print current_dir
    cherrypy.config.update('cherrypy.config')
    cherrypy.config.update({'server.socket_port': port,
                            })
    cherrypy.engine.signal_handler.subscribe()
    cherrypy.tree.mount(omxremote(), '/', 'site.config')
    cherrypy.engine.start()

    while 1:
        if exit > 0:
            sys.exit("Exiting omxremote")
        try:
            if all( p.poll() != None, get_status() != 'stopped'):
                controls.update_status('stopped')
        except:
            pass
        time.sleep(1)

if __name__ == "__main__":
    main()





