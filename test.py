#!/usr/bin/env python

"""
Tests for PyiDock.
"""

from pyidock import PyiDock
import time
from os import system

#system("clear")

print "Init."
start = time.time()

dock = PyiDock(serialspeed=57600)
dock.connect()
dock.set_playlist_to_all()

def index():
    c = dock.get_type_count(0)  # I know there are 12, now.
    strings = dock.get_type_range(0, c)
    strings[0] = "Name"
    ipodname = dock.get_ipod_name()
    i = 0
    info = {}
    for s in strings:
        if i:
            info[i] = {'string': s, 'data': dock.get_type_count(i)}
        else:
            info[0] = {'string': "Name", 'data': ipodname}
        i+=1
    return info


info = index()
print "Init done."
print "%f" % (time.time() - start)

def printstatus():

    print "iPod information"
    print "% 15s: %16s" % (info[0]['string'], info[0]['data'])
    for i in range(1, len(info), 1):
        print "% 15s: %16d" % (info[i]['string'], info[i]['data'])
    start = time.time();
    print "----------------"
    print "Playlists:"
    start = time.time();
    i = 0;
    start = time.time();
    for pl in dock.get_type_range(1, info[1]['data']):
        print "           [%d] %s" % (i, pl)
        i += 1
    end = time.time() - start;
    print "           (%f)" % end


    start = time.time();
    playlistsongs = dock.get_playlist_songs()
    print "Songs in pl: % 6d (%f)" % (playlistsongs, (time.time() - start))
    print "----------------"



    start = time.time();
    shuffle = dock.get_shuffle()
    print "Shuffle:% 11s (%f)" % (shuffle, (time.time() - start))
    start = time.time();
    repeat = dock.get_repeat()
    print "Repeat:% 12s (%f)" % (repeat, (time.time() - start))
    start = time.time();
    status = dock.get_time_and_status()
    print "State:% 13s (%f)" % (status['status'], (time.time() - start))
    print "----------------"
    start = time.time();
    if status['status'] != "stop": # can't get playlist if stopped.
        pos = dock.get_playlist_position()
        song = dock.get_song_title(pos)
        print "Song:     %-48s (%f)" % (song, (time.time() - start))
        print "          %s/%s" % (status['positiontime'], status['lengthtime'])
        start = time.time();
        position = dock.get_playlist_position()
        print "Position:% -48d (%f)" % (position, (time.time() - start))
        start = time.time();
        artist = dock.get_song_artist(pos)
        print "Artist:   %-48s (%f)" % (artist, (time.time() - start))
        start = time.time();
        album = dock.get_song_album(pos)
        print "Album:    %-48s (%f)" % (album, (time.time() - start))


execute_time = 0


while True:
    start = time.time()
    printstatus()
    print dock.laststatus

    print "Time spent getting info: %f" % (time.time() - start)
    if execute_time:
        print "Time spent executing: %f" % execute_time
    cmd = raw_input("Command: ")
#    system("clear")

    cmd_start = time.time()
    if cmd == "play":
        if dock.get_time_and_status()['status'] == "stop":
            dock.execute_playlist_switch()
        else:
            dock.play()
    if cmd == "pause":
        dock.pause()
    if cmd == "n":
        dock.skip_forward()
    if cmd == "p":
        dock.skip_backwards()
    if cmd == "ts":
        dock.toggle_shuffle()
    if cmd == "tr":
        dock.toggle_repeat()
    if cmd == "cl":
        dock.disconnect()
        exit()
    if cmd.startswith("gpd"):
        dock.goto_podcast(int(cmd.split()[1]))
    if cmd.startswith("gab"):
        dock.goto_audiobook(int(cmd.split()[1]))
    if cmd.startswith("sw"):
        dock.set_song_in_playlist(int(cmd.split()[1]))
    if cmd.startswith("gpl"):
        dock.switch_to_type(1, int(cmd.split()[1]))
        time.sleep(1)
        dock.execute_playlist_switch()
    execute_time = time.time() - cmd_start
    time.sleep(.1)