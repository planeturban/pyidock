#!/usr/bin/env python

""" Tests for PyiDock.
"""

from pyidock import PyiDock
import time
from os import system

system("clear")
print "Init."
dock = PyiDock()
dock.connect()
print "Init done."


def printstatus():

    print "iPod information"
    start = time.time();
    ipodname = dock.get_ipod_name()
    print "Name:%14s (%f)" % (ipodname, (time.time() - start))
    start = time.time();
    songs = dock.get_type_count(5)
    print "Songs:% 13d (%f)" % (songs, (time.time() - start))
    start = time.time();
    artists = dock.get_type_count(2)
    print "Artists:% 11d (%f)" % (artists, (time.time() - start))
    start = time.time();
    albums = dock.get_type_count(3)
    print "Albums:% 12d (%f)" % (albums, (time.time() - start))
    start = time.time();
    playlists = dock.get_type_count(1)
    print "Playlists:% 9d (%f)" % (playlists, (time.time() - start))
    start = time.time();
    genres = dock.get_type_count(4)
    print "Genres:% 12d (%f)" % (genres, (time.time() - start))
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
    pos = dock.get_playlist_position()
    song = dock.get_song_title(pos)
    print "Song:     %-48s (%f)" % (song, (time.time() - start))
    print "    : %s/%s" % (status['positiontime'], status['lengthtime'])
    start = time.time();
    position = dock.get_playlist_position()
    print "Position: % -48d (%f)" % (position, (time.time() - start))
    start = time.time();
    artist = dock.get_song_artist(pos)
    print "Artist:   %-48s (%f)" % (artist, (time.time() - start))
    start = time.time();
    album = dock.get_song_album(pos)
    print "Album:    %-48s (%f)" % (album, (time.time() - start))



dock.set_playlist_to_all()
dock.set_shuffle("albums")
execute_time = 0

while True:
    start = time.time()
    printstatus()
    print "Time spent getting info: %f" % (time.time() - start)
    if execute_time:
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