#!/usr/bin/env python

""" Tests for PyiDock.
"""

from pyidock import PyiDock
import time
from os import system
import datetime


def read_fifo(filename):
    while True:
        with open(filename) as fifo:
            yield fifo.read()

system("clear")
print "Init."
dock = PyiDock()
dock.connect()
print "Init done."

def printstatus():

    ipodname = dock.get_ipod_name()
    playlists = dock.get_type_count(1)
    artists = dock.get_type_count(2)
    albums = dock.get_type_count(3)
    genres = dock.get_type_count(4)
    songs = dock.get_type_count(5)
    repeat = dock.get_repeat()
    shuffle = dock.get_shuffle()
    pos = dock.get_playlist_position()
    song = dock.get_song_title(pos)
    artist = dock.get_song_artist(pos)
    album = dock.get_song_album(pos)
    status = dock.get_time_and_status()
    position = dock.get_playlist_position()
    playlistsongs = dock.get_playlist_songs()

    print "iPod information"
    print "Name: % 5s" % ipodname
    print "Songs:      % 4d" % songs
    print "Playlists:  % 4d" % playlists
    print "Artists:    % 4d" % artists
    print "Albums:     % 4d" % albums
    print "Genres:     % 4d" % genres
    print "Songs in pl: % 4d" %playlistsongs
    print "----------------"
    print "Shuffle:    % 3s" % shuffle
    print "Repeat:     % 3s" % repeat
    print "State:      % 4s" % status['status']
    print "----------------"
    print "Song: %s" % song
    print "Position: %d" % position
    print "    : %s/%s" % (status['positiontime'], status['lengthtime'])
    print "Artist: %s" % artist
    print "Album: %s" % album


dock.set_playlist_to_all()
dock.set_shuffle("albums")
execute_time = 0

while True:
    start = time.time()
    printstatus()
    print "Time spent getting info: %f" % (time.time() - start)
    if ( execute_time):
        print "Time spent executing: %f" % execute_time
    cmd = raw_input("Command: ")
    system("clear")
    cmd_start = time.time()
    if cmd == "play":
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
    execute_time = time.time() - cmd_start
    time.sleep(.1)