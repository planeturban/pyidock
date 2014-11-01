# PyiDock

Class for controlling iPod in air mode.
AAP documentation at https://nuxx.net/wiki/Apple_Accessory_Protocol

## Sample code

```python
from pyidock import PyiDock
from time import time

start = time()
dock = PyiDock()
dock.connect()
numberOfSongs = int(dock.get_type_count(5))  # type 5 is songs.
songs = dock.get_type_range(5, numberOfSongs, 0)
dock.disconnect()
end = time()
avg = (end - start) / len(songs)

print "%d songs in %f. %f average per song." % ( len(songs), (end - start)
```

## Circut
```
+5V ---------+                                                           #
             |                                                           #
             |            +------------------- pin 27 (data+)            # This
             |            |                                              # is
             |            |            +------ pin 16 (GND)              # for
             |            |            |                                 # charging.
             +--| 33k |---+---| 47k |--+                                 # Read
             |                                                           # more
             +--| 33k |---+---| 22k |--+                                 # at
             |            |            |                                 # pinouts.ru/PortableDevices/ipod_pinout.shtml
             |            |            +------ pin 15 (GND)              #
             |            |                                              #
             |            +------------------- pin 25 (data-)            #
             |                                                           #
             +-------------------------------- pin 23 (USB +5V in)       #

             +-------------------------------- pin 11 (Serial GND)
             |
             +--| 560k |---------------------- pin 21 (Dock identifier)
             |
GND ---------+
```

TX/RX on 13/12

Charging works with 6th gen ipod nano but not 7th gen ipod classic (120GB).



