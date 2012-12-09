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
    cursor.execute("CREATE TABLE IF NOT EXISTS status (key INTEGER PRIMARY KEY AUTOINCREMENT, status, name)")
    cursor.execute("INSERT OR REPLACE INTO status VALUES ('0', 'stopped', 'None')")
    cursor.execute("CREATE TABLE IF NOT EXISTS library_paths (key INTEGER PRIMARY KEY AUTOINCREMENT, path, recurse, monitor)")
    cursor.execute("CREATE TABLE IF NOT EXISTS playlists (key INTEGER PRIMARY KEY AUTOINCREMENT, name UNIQUE, file_keys)")
    cursor.execute("CREATE TABLE IF NOT EXISTS config (key INTEGER PRIMARY KEY AUTOINCREMENT, name UNIQUE, value)")
    cursor.execute("INSERT OR IGNORE INTO config (name, value) VALUES (?, ?)", ['port', '8080'])
    cursor.execute("INSERT OR IGNORE INTO config (name, value) VALUES (?, ?)", ['executable', '/usr/bin/mplayer'])
    conn.commit()

def load_config():
    global config_dict 
    config_dict = {'name':'value'}
    conn = sqlite3.connect("remote.db")
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute("SELECT name, value FROM config")
    
    for row in cursor.fetchall():
        print row
        if row[0] =='port':
            value = int(row[1])
        else:
            value = row[1]
        config_dict[row[0]] = value 

class omxremote:
    def index(self, pause = 0, play = 0, stop = 0, quit = 0):
        global p
        global exit
        global env
        global config_dict
        exit = quit

        conn = sqlite3.connect("remote.db")
        cursor = conn.cursor()

        if play > 0:
            p = controls.start(config_dict['executable'], play, p)

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

    def search(self):
        return "search"

    def settings(self, remove = '', add = '', add_dir = '', submit = '', port = ''):
        conn = sqlite3.connect("remote.db")
        cursor = conn.cursor()
        
        if add_dir != '':
            cursor.execute("INSERT INTO library_paths (path, recurse, monitor) VALUES (?, ?, ?)", [add_dir, 1, 1])
            conn.commit()
            controls.add_path_to_library(add_dir)

        if port != '':
            cursor.execute("UPDATE config SET value=? WHERE name='port'", [port])
            conn.commit()
        if remove != '':
            cursor.execute("DELETE FROM library_paths WHERE key=?", [remove])
            conn.commit()

        cursor.execute("SELECT path, key FROM library_paths")
        lib_paths = cursor.fetchall()
        template = env.get_template("settings.tpl")
        return template.render(playing=controls.get_playing(),lib_paths = lib_paths, port = config_dict['port']) 
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
    global config_dict

    startup_checks()
    load_config()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print os.path.join(current_dir, 'templates', 'images')
    print current_dir
    cherrypy.config.update('cherrypy.config')
    cherrypy.config.update({'server.socket_port': config_dict['port'],
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





