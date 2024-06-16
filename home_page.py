import datetime
import os
import re
import time
from collections import Counter
from itertools import groupby
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import pyshark
import threading

FILE = os.path.join(os.getcwd(), "networkinfo.log")
FILE3 = os.path.join(os.getcwd(), "blist.log")
FILE2 = os.path.join(os.getcwd(), "networklog.log")
# Global flag
running = True


# suspect and Network
def suspe():
    def entry_to_second(entry):
        return entry.split('.', 1)[0]

    with open(FILE3, 'r') as file:
        data = file.read()
    with open(FILE2, 'r') as file:
        data1 = file.read()
    bl = ScrolledText(frame1, fg="green", bg="black")
    bl.pack(fill=BOTH, expand=TRUE)
    bl.insert(END, data)
    bl.configure(state="disabled")

    nl = ScrolledText(frame2, fg="green", bg="black")
    nl.pack(fill=BOTH, expand=TRUE)
    nl.insert(END, data1)
    nl.configure(state="disabled")

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
                    elif cnt > 100:
                        a = ip.rsplit(':', 1)[-1]
                        print(a)
                c.clear()
            newbl = blacklist + newip
            print(newbl)
            with open("D:/tool/blist.log", 'a') as f:
                f.write('\n'.join(set(newbl)) + '\n\n')
                f.close()
        except AttributeError as e:

            pass
        print(" ")


# GUI Window
root = Tk()
root.title("Home Page")
root.winfo_screenwidth()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

# menubar = Menu(root, background='blue', fg='white')
# help = Menu(menubar, tearoff=0)
# help.add_command(label="About us")
# help.add_separator()
# help.add_command(label="Contact Us")

# menubar.add_cascade(label="Help", menu=help)

# root.config(menu=menubar, bg="grey")

# Suspected IP Frame
frame1 = LabelFrame(root, bg="black", fg="green", text="Suspected-IP")
frame1.place(x=0, y=100, width=1300, height=240)

# Network Log Frame
frame2 = LabelFrame(root, bg="black", fg="green", text="Network Log")
frame2.place(x=0, y=400, width=700, height=240)

frame4 = Frame(root, bg="blue")
frame4.place(x=0, y=0, width=1366, height=90)

title = Label(frame4, text="Investigation Tool", font=("times new roman", 35, "bold", "italic"), bg="blue",
              fg="Black").place(x=490, y=18)

btn_Start = Button(root, text="Start", font=("open sans", 18, "bold"), fg="white",
                   bg="green", cursor="hand2", command=threading.Thread(target=suspe).start)
btn_Start.place(x=950, y=430, width=180, height=40)
btn_exit = Button(root, text="Exit", command=root.destroy, font=("open sans", 18, "bold"), fg="white",
                  bg="green", cursor="hand2")
btn_exit.place(x=750, y=430, width=180, height=40)

btn_stop = Button(root, text="Stop", font=("open sans", 18, "bold"), fg="white",
                  bg="green", cursor="hand2")
btn_stop.place(x=750, y=550, width=180, height=40)

root.mainloop()
