import os
import sys
import socket
import datetime
import time

FILE = os.path.join(os.getcwd(), "networkinfo.log")


# creating log file in the current directory using GETCWD


def ping():
    try:
        socket.setdefaulttimeout(3)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = "www.google.com"
        port = 443

        server_address = (host, port)
        s.connect(server_address)

    except OSError as error:
        return False


    else:
        s.close()

        return True


def calculate_time(start, stop):
    difference = stop - start
    seconds = float(str(difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]


def f_check():
    # to check an internet connection
    if ping():
        # if ping returns true
        live = "\nCONNECTION ACQUIRED\n"
        print(live)
        connection_acquired_time = datetime.datetime.now()
        acquiring_message = "connection acquired at: " + \
                            str(connection_acquired_time).split(".")[0]
        print(acquiring_message)

        with open(FILE, "a") as file:

            file.write(live)
            file.write(acquiring_message)

        return True
    else:
        # if ping returns false
        not_live = "\nCONNECTION NOT ACQUIRED\n"
        print(not_live)

        with open(FILE, "a") as file:

            file.write(not_live)
        return False


def main():
    # main function to call functions
    monitor_start_time = datetime.datetime.now()
    monitoring_date_time = "monitoring started at: " + \
                           str(monitor_start_time).split(".")[0]

    if f_check():
        # if true
        print(monitoring_date_time)
        # monitoring will only start when
        # the connection will be acquired
    else:
        # if false
        while True:

            # infinite loop to see if the connection is acquired
            if not ping():

                # if connection not acquired
                time.sleep(1)
            else:

                # if connection is acquired
                f_check()
                print(monitoring_date_time)
                break

    with open(FILE, "a") as file:
        file.write("\n")
        file.write(monitoring_date_time + "\n")

    while True:

        # infinite loop, as we are monitoring
        # the network connection till the machine runs
        if ping():

            # if true: the loop will execute after every 5 seconds
            time.sleep(5)

        else:
            # if false: fail message will be displayed
            down_time = datetime.datetime.now()
            fail_msg = "disconnected at: " + str(down_time).split(".")[0]
            print(fail_msg)

            with open(FILE, "a") as file:
                # writes into the log file
                file.write(fail_msg + "\n")

            while not ping():
                # will run till ping() return true
                time.sleep(1)

            up_time = datetime.datetime.now()

            # connection restored
            uptime_message = "connected again: " + str(up_time).split(".")[0]

            down_time = calculate_time(down_time, up_time)

            # calling time calculating
            # function, printing down time
            unavailablity_time = "connection was unavailable for: " + down_time

            print(uptime_message)
            print(unavailablity_time)

            with open(FILE, "a") as file:

                # Printing Unavailability
                file.write(uptime_message + "\n")
                file.write(unavailablity_time + "\n")


main()
