import serial
from time import sleep

class PyiDock:

    """ Class for controlling iPod """
    def __init__(self, serialport = "/dev/tty.usbserial", serialspeed = 19200, timeout = 1):
        self.serialPort = serialport
        self.serialSpeed = serialspeed
        self.timeout = timeout
        self.queue = {}
        self.timedata = ""

    def connect(self):
        self.serial = serial.Serial(self.serialPort, baudrate=self.serialSpeed, timeout=self.timeout)
        sleep(1)
        self.serial.write(self.mkcmd(0, "0104")) # Enable AIR

    def disconnect(self):
        self.serial.close()

    def mkcmd(self, lingo, s):
        s = s.decode("hex")
        sum = 0
        s = chr(len(s) + 1) + chr(lingo) + s
        for ch in s:
            sum = sum + ord(ch)
        sum = 0x100 - (sum & 0xff)
        return chr(0xff) + chr(0x55) + s + chr(sum)

    def flush(self, what="all"):
        in_queue = True
        out_queue = True
        if what.lower() == "in":
            out_queue = False
        if what.lower() == "out":
            in_queue = False
        if in_queue:
            self.serial.flushInput()
        if out_queue:
            self.serial.flushOutput()

    def enqueue(self, cmd):
        if self.queue.has_key(cmd):
            count = self.queue[cmd]
        else:
            count = 0
        count += 1
        self.queue.update({cmd: count})

    def dequeue(self, cmd):
        count = 0
        if self.queue.has_key(cmd):
            count = self.queue[cmd]
        if count > 0:
            count -= 1
        self.queue.update({cmd: count})


    def to_hex(self, s):
        lst = []
        for ch in s:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0'+hv
            lst.append(hv)
        return reduce(lambda x,y:x+y, lst)

    def int_to_hex_str(self, x, length=4):
        if x > 4294967295:  # Boy, do you have a large library!
            x = 4294967295  # Probably redundant..
        length = length * 2
        return hex(x).split("x")[1].zfill(length)

    def read_response(self, fullmessage=False):
        ret = ()
        sleep(.15) # need to wait a while, just in case..
        while self.serial.inWaiting():
            if self.serial.read(2) == "ff55".decode("hex"):
                length = self.serial.read(1)
                lingo = self.serial.read()
                body = self.serial.read(int(self.to_hex(length), 16)-1)
                checksum = self.serial.read()
                message = "ff55".decode("hex") + length + lingo + body + checksum
                if self.mkcmd(int(self.to_hex(lingo)), self.to_hex(body)) == message:  # Valid response?
                    if message.startswith("ff5507040027".decode("hex")):  # if we're in pulling mode.
                        self.timedata = message
                    else:
                        if not fullmessage:
                            ret = ret + (body,)
                        else:
                            ret = ret +  (message, )
                    return ret

    def get_ipod_type(self):
        cmd = self.mkcmd(4, "0012")
        self.serial.write(cmd)

    def get_ipod_name(self):
        self.serial.write(self.mkcmd(4, "0014"))

    def set_playlist_to_all(self):
        self.serial.write(self.mkcmd(4, "0016"))

    def switch_to_type(self, itemtype=0, number=0):
        self.serial.write(self.mkcmd(4, "0017" + self.int_to_hex_str(itemtype, 1) + self.int_to_hex_str(number)))

    def get_type_count(self, itemtype=0):
        self.serial.write(self.mkcmd(4, "0018" + self.int_to_hex_str(itemtype,1)))

    def get_type_range(self, itemtype=0, count=0, offset=0):
        self.serial.write(self.mkcmd(4, "001A" + self.int_to_hex_str(itemtype, 1) + self.int_to_hex_str(offset) +
                                   self.int_to_hex_str(count)))

    def get_time_and_status(self):
        self.serial.write(self.mkcmd(4, "001C"))

    def get_playlist_position(self):
        self.serial.write(self.mkcmd(4, "001E"))

    def get_song_title(self, song=0):
        self.serial.write(self.mkcmd(4, "0020" + self.int_to_hex_str(song)))

    def get_song_artist(self, song=0):
        self.serial.write(self.mkcmd(4, "0022" + self.int_to_hex_str(song)))

    def get_song_album(self, song=0):
        self.serial.write(self.mkcmd(4, "0024" + self.int_to_hex_str(song)))

    def set_pulling_mode(self, mode=True):
        if mode:
            m = 1
        else:
            m = 0
        self.serial.write(self.mkcmd(4, "0026" + self.int_to_hex_str(m, 1)))

    def excute_playlist_switch(self, song=0xFFFFFFFF):
        self.serial.write(self.mkcmd(4, "0028" + self.int_to_hex_str(song)))

    def raw_control(self, cmd=1):
        self.flush()  # Let's clear the serial data...
        self.timedata = ""
        self.set_pulling_mode(False)
        self.serial.write(self.mkcmd(4, "0029" + self.int_to_hex_str(cmd, 1)))

    def play(self):
        self.serial.write(self.raw_control())

    def pause(self):
        self.serial.write(self.raw_control(2))

    def skip_forward(self):
        self.serial.write(self.raw_control(3))

    def skip_backwards(self):
        self.serial.write(self.raw_control(4))

    def forward(self):
        self.serial.write(self.raw_control(5))

    def reverse(self):
        self.serial.write(self.raw_control(6))

    def stop_fr(self):
        self.serial.write(self.raw_control(7))

    def get_shuffle(self):
        self.serial.write(self.mkcmd(4, "002c"))

    def set_shuffle(self, mode="songs"):
        if mode.lower() == "off":
            cmd = 0
        if mode.lower() == "songs":
            cmd = 1
        if mode.lower() == "albums":
            cmd = 2
        self.serial.write(self.mkcmd(4, self.int_to_hex_str(cmd, 1)))

    def get_repeat(self):
        self.serial.write(self.mkcmd(4, "002f"))

    def set_repeat(self, mode="one"):
        if mode.lower() == "off":
            cmd = 0
        if mode.lower() == "one":
            cmd = 1
        if mode.lower() == "all":
            cmd = 2
        self.serial.write(self.mkcmd(4, "0031" + self.int_to_hex_str(cmd, 1)))

    def get_playlist_songs(self):
        self.serial.write(self.mkcmd(4, "0035"))

    def set_song_in_playlist(self, song=0):
        self.serial.write(self.mkcmd(4, "0037" + self.int_to_hex_str(song)))

    
