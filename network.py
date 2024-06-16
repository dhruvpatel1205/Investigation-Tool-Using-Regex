import os
import pyshark
import time
import datetime

FILE2 = os.path.join(os.getcwd(), "networklog.log")

networkInterface = "Wi-Fi"

# Capturing Object
capture = pyshark.LiveCapture(interface=networkInterface)

print("listening on %s" % networkInterface)

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
    except AttributeError as e:

        pass
    print(" ")
