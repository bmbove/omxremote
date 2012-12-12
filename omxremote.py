#!/usr/bin/python
import cherrypy
import os
import sys
import jinja2
import controls
import sqlite3
import subprocess
import time
import signal

current_dir = os.path.dirname(os.path.abspath(__file__))

def signal_handler(signal, frame):
    print 'Ctrl+C caught... Exiting!'
    cherrypy.engine.stop()
    cherrypy.engine.exit()
    sys.exit(0)

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
    config_dict = {'port':'8080', 'executable':'/usr/bin/mplayer', 'cmd_args':'-fs', 'pause_key':'p', 'stop_key':'q', 'vol_up_key':'0', 'vol_down_key':'9', 'ff_key':']', 'rw_key':'['}
    for key in config_dict:
        cursor.execute("INSERT OR IGNORE INTO config (name, value) VALUES (?, ?)", [key, config_dict[key]])
    conn.commit()

def load_config():
    global config_dict 
    config_dict = {'name':'value'}
    conn = sqlite3.connect("remote.db")
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute("SELECT name, value FROM config")
    
    for row in cursor.fetchall():
        if row[0] =='port':
            value = int(row[1])
        else:
            value = row[1]
        config_dict[row[0]] = value 

class omxremote:
    def remcontrols(self, play = 0, pause=0, stop = 0, quit = 0, vol_up = 0, vol_down = 0, ff = 0, rw = 0, next_file = 0, prev_file = 0):
        global p
        if pause > 0:
            controls.send_cmd(p, config_dict['pause_key'])
            if controls.get_status() == 'playing':
                controls.update_status("paused", controls.get_playing())
            else:
                controls.update_status("playing", controls.get_playing())

        if stop > 0:     
            p = controls.send_cmd(p, config_dict['stop_key'])
            controls.update_status("stopped")

        if vol_up > 0:
            for i in range(7):
                controls.send_cmd(p, config_dict['vol_up_key'])

        if vol_down > 0:
            for i in range(7):
                controls.send_cmd(p, config_dict['vol_down_key'])

        if ff > 0:
            controls.send_cmd(p, config_dict['ff_key'])
        
        if rw > 0:
            controls.send_cmd(p, config_dict['rw_key'])
        if play > 0:
            p = controls.start(config_dict['executable'], config_dict['cmd_args'], play, p)
        
        return controls.get_playing()

    def index(self, quit = 0):
        global exit
        global env
        global config_dict
        exit = quit

        conn = sqlite3.connect("remote.db")
        cursor = conn.cursor()

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

    def playlist(self):
        return "playlist"

    def settings(self, pause_key='', stop_key='', vol_up_key='', vol_down_key='', ff_key='', rw_key='', remove = '', add = '', add_dir = '', submit = '', port = '', recurse = '0', cmd_args = '', executable = ''):
        conn = sqlite3.connect("remote.db")
        cursor = conn.cursor()
        
        if add_dir != '':
            cursor.execute("INSERT INTO library_paths (path, recurse, monitor) VALUES (?, ?, ?)", [add_dir, recurse, 1])
            conn.commit()
            controls.add_path_to_library(add_dir)

        if port != '':
            cursor.execute("UPDATE config SET value=? WHERE name='port'", [port])
            conn.commit()
        if remove != '':
            cursor.execute("SELECT path, recurse FROM library_paths WHERE key=?", [remove])
            row = cursor.fetchone()
            path = row[0]
            path_recurse = row[1] 
            cursor.execute("DELETE FROM library_paths WHERE key=?", [remove])
            if path_recurse == 1:
                cursor.execute("DELETE FROM library WHERE path LIKE ?", ['%' + path + '%']) 
            else:
                cursor.execute("DELETE FROM library WHERE path=?", [path])
            conn.commit()
        if cmd_args != '':
            cursor.execute("UPDATE config SET value=? WHERE name='cmd_args'", [cmd_args])
            conn.commit()
            config_dict['cmd_args'] = cmd_args
        if executable != '':
            cursor.execute("UPDATE config SET value=? WHERE name='executable'", [executable])
            conn.commit()
            config_dict['executable'] = executable

        if stop_key != '':
            cursor.execute("UPDATE config SET value=? WHERE name='stop_key'", [stop_key])
            conn.commit()
            config_dict['stop_key'] = stop_key     

        if vol_up_key != '':
            cursor.execute("UPDATE config SET value=? WHERE name='vol_up_key'", [vol_up_key])
            conn.commit()
            config_dict['vol_up_key'] = vol_up_key     

        if vol_down_key != '':
            cursor.execute("UPDATE config SET value=? WHERE name='vol_down_key'", [vol_down_key])
            conn.commit()
            config_dict['vol_down_key'] = vol_down_key     

        if ff_key != '':
            cursor.execute("UPDATE config SET value=? WHERE name='ff_key'", [ff_key])
            conn.commit()
            config_dict['ff_key'] = ff_key     

        if rw_key != '':
            cursor.execute("UPDATE config SET value=? WHERE name='rw_key'", [rw_key])
            conn.commit()
            config_dict['rw_key'] = rw_key     

        if pause_key != '':
            cursor.execute("UPDATE config SET value=? WHERE name='pause_key'", [pause_key])
            conn.commit()
            config_dict['pause_key'] = pause_key     

        cursor.execute("SELECT path, key, recurse FROM library_paths")
        lib_paths = cursor.fetchall()
        template = env.get_template("settings.tpl")
        return template.render(playing=controls.get_playing(),lib_paths = lib_paths, config_dict = config_dict) 
    index.exposed = True
    style.exposed = True
    music.exposed = True
    videos.exposed = True
    settings.exposed = True
    playlist.exposed = True
    remcontrols.exposed = True

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
    cherrypy.config.update('cherrypy.config')
    cherrypy.config.update({'server.socket_port': config_dict['port'],
                            })
    cherrypy.engine.signal_handler.subscribe()
    cherrypy.tree.mount(omxremote(), '/', 'site.config')
    cherrypy.engine.start()

    while 1:
        if exit > 0:
            cherrypy.engine.stop()
            cherrypy.engine.exit()
            sys.exit("Exiting omxremote")
        try:
            if all( p.poll() != None, get_status() != 'stopped'):
                controls.update_status('stopped')
        except:
            pass
        time.sleep(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
