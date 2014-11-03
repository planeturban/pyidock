#!/usr/bin/env python
from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from pyidock import PyiDock

class ipod(resource.Resource):
    isLeaf = True
    numberRequests = 0
    lastCmd = "Unknown"
    endpoints = {'control': ['play', 'pause', 'stop', 'next', 'previous'],
                 'info': ['types', 'playlists', 'artists', 'albums', 'genres', 'songs', 'composers', 'audiobooks',
                          'podcasts'],
                 'index': ['playlists', 'songs'], 'nowplaying': '', 'status': ''}
    dock = PyiDock()
    dock.connect()
    dock.set_playlist_to_all()

    def render_GET(self, request):
        print request
        head = "<html><head><title>ipod</title><meta charset=\"UTF-8\"></head><body>"
        ret = ""
        uri = request.uri.split("/")
        uri.pop(0)
        cmd = uri.pop(0)
        redirect = ""
        if cmd == "control":
            if len(uri):
                if uri[0] == "play":
                    self.dock.play()
                    self.lastCmd = "pause"
                if uri[0] == "pause":
                    self.lastCmd = "pause"
                elif uri[0] == "stop":
                    self.lastCmd = "stop"
                elif uri[0] == "next":
                    self.dock.skip_forward()
                    self.lastCmd = "next"
                elif uri[0] == "previous" or uri[0] == "prev":
                    self.dock.skip_backwards()
                    self.lastCmd = "previous"
                ret = ""
                redirect = "/"
            else:
                for cmd in self.endpoints['control']:
                    ret = head
                    ret += "<a href='/control/%s'>%s</a><br>" % (cmd, cmd)
                    ret += "</body></html>"
        elif not cmd:
            ret = "Last command: %s<br>" % self.lastCmd
            for root in self.endpoints.keys():
                ret += "<ul><a href='%s'>%s</a><br>" % (root, root)
                for cmd in self.endpoints[root]:
                    ret = ret + "<ul><li><a href='%s/%s'>%s</a></ul>" % ( root, cmd, cmd)
                ret += "</ul>"
        elif cmd == "nowplaying":
            song = self.dock.get_playlist_position()
            title = self.dock.get_song_title(song)
            artist = self.dock.get_song_artist(song)
            album = self.dock.get_song_album(song)
            ret = head
            ret += "Artist: %s<br> Album: %s<br> Title: %s" % (artist, album, title)
            ret += "</body></html>"
        elif cmd == "info":
            if len(uri):
                ret = head
                if uri[0] == "types" or uri[0] == 0:
                    i = 0
                    for pl in self.dock.get_all_by_type(0):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "playlists" or uri[0] == 1:
                    i = 0
                    for pl in self.dock.get_all_by_type(1):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "artists":
                    i = 0
                    for pl in self.dock.get_all_by_type(2):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "albums":
                    i = 0
                    for pl in self.dock.get_all_by_type(3):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "genres":
                    i = 0
                    for pl in self.dock.get_all_by_type(4):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "songs":
                    i = 0
                    for pl in self.dock.get_all_by_type(5):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "composers":
                    i = 0
                    for pl in self.dock.get_all_by_type(6):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "audiobooks":
                    i = 0
                    for pl in self.dock.get_all_by_type(7):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "podcasts":
                    i = 0
                    for pl in self.dock.get_all_by_type(8):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "audiobooks":
                    i = 0
                    for pl in self.dock.get_all_by_type(9):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "smartplaylists":
                    i = 0
                    for pl in self.dock.get_all_by_type(10):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "geniusmixes":
                    i = 0
                    for pl in self.dock.get_all_by_type(11):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                if uri[0] == "itunesu":
                    i = 0
                    for pl in self.dock.get_all_by_type(12):
                        ret += "%d: %s<br>" % (i, pl)
                        i += 1
                ret += "</body></html>"
        elif cmd in self.endpoints.keys():
            ret = "Not implemeted.<br>"
        else:
            redirect = "/"
        if redirect:
            request.redirect(redirect)
        return ret


endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(ipod()))
reactor.run()


