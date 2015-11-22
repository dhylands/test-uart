#!/usr/bin/env python

"""Sends a pattern of incrementing numbers at a baud rate to see if the 
receiver can keep up.
"""

import argparse
import serial
import sys
import termios
import tty

def main():
    """The main program."""
    default_baud = 1000000
    default_port = '/dev/ttyUSB0'

    parser = argparse.ArgumentParser(
        prog="sender",
        usage="%(prog)s [options] [command]",
        description="Send a stream of data to the receiver.",
    )
    parser.add_argument(
        "-b", "--baud",
        dest="baud",
        action="store",
        type=int,
        help="Set the baudrate used (default = %d)" % default_baud,
        default=default_baud
    )
    default_port_help = ""
    if default_port:
        default_port_help = " (default '%s')" % default_port
    parser.add_argument(
        "-p", "--port",
        dest="port",
        help="Set the serial port to use" + default_port_help,
        default=default_port
    )
    args = parser.parse_args(sys.argv[1:])

    try:
        ser = serial.Serial(port=args.port,
                            baudrate=args.baud,
                            timeout=0.001,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            xonxoff=False,
                            rtscts=False,
                            dsrdtr=False)
    except serial.serialutil.SerialException:
        print("Unable to open port '%s'\r" % port_name)
        return

    ser_fd = ser.fileno()
    tty.setraw(ser_fd)
    new_settings = termios.tcgetattr(ser_fd)
    new_settings[6][termios.VTIME] = 0
    new_settings[6][termios.VMIN] = 1
    termios.tcsetattr(ser_fd, termios.TCSANOW, new_settings)

    buf = ''
    num_ints = 1024
    for i in range(num_ints):
        buf = buf + '{:04d}'.format(i)

    ser.write(buf)
    print("Write {} bytes".format(len(buf)))


main()
