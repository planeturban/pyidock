#!/usr/bin/env python

"""
Tests for PyiDock.
"""

from pyidock import PyiDock
import time
from os import system

#system("clear")

print "Init."
playlist = []
artist = []
album = []
genre = []
song = []
composer = []

dock = PyiDock()
dock.connect()
dock.set_playlist_to_all()

start = time.time()
playlists = dock.get_type_count(1)
artists = dock.get_type_count(2)
albums = dock.get_type_count(3)
genres = dock.get_type_count(4)
songs = dock.get_type_count(5)
composers = dock.get_type_count(6)
"""
print "Playlists"
for i in range(0, playlists , 1):
    playlist.append(dock.get_type_range(1, 1, i))
print "Artists"
for i in range(0, artists, 1):
    artist.append(dock.get_type_range(2, 1, i))
print "Albums"
for i in range(0, albums, 1):
    album.append(dock.get_type_range(3, 1, i))
print "Genres"
for i in range(0, genres, 1):
    genre.append(dock.get_type_range(4, 1, i))
print "Songs"
for i in range(0, songs, 1):
    song.append(dock.get_type_range(5, 1, i))
"""


print "Init done."
print "%f" % (time.time() - start)

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
    print "Audiobooks:% 12d" % dock.get_type_count(7)
    print "Podcasts:% 12d" % dock.get_type_count(8)
    print "9:% 12d" % dock.get_type_count(9)

    start = time.time();
    albums = dock.get_type_count(3)
    print "Albums:% 12d (%f)" % (albums, (time.time() - start))
    start = time.time();
    playlists = dock.get_type_count(1)
    print "Playlists:% 9d (%f)" % (playlists, (time.time() - start))
    pls = []
    start = time.time();
    for i in range(0, playlists , 1):
        pls.append(dock.get_type_range(1, 1, i))
    end = time.time() - start;
    i = 0;
    for pl in pls:
        print "           [%d] %s" % (i, pl)
        i += 1
    print "           (%f)" % end
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