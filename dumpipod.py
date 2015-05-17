__author__ = 'ube'
from pyidock import PyiDock


dock = PyiDock()

dock.connect()

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


i = 1
index = index()
print index

while i != 13:
    f = open(str(i) + " " + index[i]['string'] + ".db", "a")
    for q in dock.get_all_by_type(i):
        f.write(q + "\n")
    i = i + 1
    f.close()
dock.disconnect()