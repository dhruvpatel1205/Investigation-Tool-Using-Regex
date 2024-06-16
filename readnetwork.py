import time
import os

FILE2 = os.path.join(os.getcwd(), "networklog.log")


def follow(FILE2):
    # seek the end of the file
    FILE2.seek(0, os.SEEK_END)

    # start infinite loop
    while True:
        # read last line of file
        line = FILE2.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue

        yield line


if __name__ == '__main__':

    logfile = open(FILE2, "r")
    loglines = follow(logfile)
    # iterate over the generator
    for line in loglines:
        print(line)
