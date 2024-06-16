import datetime
import os
import re
import time

from collections import Counter
from itertools import groupby

import pyshark

FILE2 = os.path.join(os.getcwd(), "networklog.log")

FILE3 = os.path.join(os.getcwd(), "blist.log")

blacklist = list(open('D:/Tool/blist.log', 'r').read().split('\n'))
logfile = list(open('D:/Tool/networklog.log', 'r').read().split('\n'))

dtime = re.compile(r'[0-9]{0,3}\d+\:[0-9]{0,3}\d+')
ddate = re.compile(r'[0-9]{1,2}\d+\-[0-9]{1,2}\d+\-[0-9]{1,2}\d+')
# ip = re.compile(r'[0-9]{0,3}\d+\.[0-9]{0,3}\d+\.[0-9]{0,3}\.[0-9]{0,3}\d+')

networkInterface = "Wi-Fi"

# Capturing Object
capture = pyshark.LiveCapture(interface=networkInterface)

print("listening on %s" % networkInterface)
newip = []
c = Counter()


def entry_to_second(entry):
    return entry.split('.', 1)[0]


for packet in capture.sniff_continuously():

    try:
        # timestamp
        local = datetime.datetime.now()
        localt = str(local).split(".")[0]
        # get packet content
        protocol = packet.transport_layer
        src_addr = packet.ip.src  # src address
        src_port = packet[protocol].srcport  # src port
        dst_addr = packet.ip.dst  # dest address
        dst_port = packet[protocol].dstport  # dest port

        # Writing to the Text File
        with open(FILE2, "a") as file:
            file.write("\n")
            file.write(localt)
            file.write(" IP ")
            file.write(src_addr)
            file.write(":")
            file.write(src_port)
            file.write("  ")
            file.write(dst_addr)
            file.write(":")
            file.write(dst_port)
            file.write("  ")
            file.write(protocol)

        print("%s IP %s:%s <-> %s:%s (%s)" % (local, src_addr, src_port, dst_addr, dst_port, protocol))
        logfile = sorted(logfile, key=entry_to_second)  # <--- sort the logfile by the second
        for key, group in groupby(logfile, key=entry_to_second):
            for entry in group:
                c.update(re.findall(r'[0-9]{0,3}\d+\.[0-9]{0,3}\d+\.[0-9]{0,3}\.[0-9]{0,3}\d+', entry))
            for ip, cnt in c.items():
                if cnt > 10:
                    newip.append(ip)
                elif cnt > 100:  # <-- align elif with if. Indentation is critical in python
                    a = ip.rsplit(':', 1)[-1]  # <-- last part of ip (the :21 IF there is a :)
                    print(a)
            c.clear()
        newblist = blacklist + newip
        print(newblist)
        with open("D:/tool/blist.log", 'a') as f:
            f.write('\n'.join(set(newblist)) + '\n\n')
            f.close()

    except AttributeError as e:

        pass
    print(" ")
