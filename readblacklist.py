import time
import os

FILE3 = os.path.join(os.getcwd(), "blist.log")


def follow(FILE3):
    # seek the end of the file
    FILE3.seek(0, os.SEEK_END)

    # start infinite loop
    while True:
        # read last line of file
        line = FILE3.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue

        yield line


if __name__ == '__main__':

    logfile = open(FILE3, "r")
    loglines = follow(logfile)
    # iterate over the generator
    for line in loglines:
        print(line)
