#
# Test program to see how fast we can receive data
#

import pyb

def run(baud=1000000):
    uart = pyb.UART(6, baud, timeout=10000, timeout_char=10)
    buf_len = 4096
    buf = bytearray(buf_len)
    print('buf_len = ', len((buf)))
    num_bytes = uart.readinto(buf)
    print('Read {} bytes'.format(num_bytes))
    for i in range(0, buf_len, 4):
        expected = bytearray('{:04d}'.format(i // 4))
        found = buf[i:i+4]
        if found != expected:
            print("Offset {} found '{}' expecting '{}'".format(i, found, expected))
            break
    else:
        print('All bytes matched')

run()

