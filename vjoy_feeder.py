#!/usr/bin/env python3
#
# Copyright (C) 2020 Dustin Spicuzza
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#
# This simple vJoy feeder application listens on a UDP socket for incoming
# joystick packets, which are immediately sent to the selected joystick.
#
# WARNING: only use this on a trusted network!
#
# Assumes that you have the vJoy device already setup and running. Refer to
# the vJoy documentation for details.
#

import argparse
import socket
import ctypes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", type=int, default=1)
    parser.add_argument("-p", "--port", type=int, default=27257)
    parser.add_argument(
        "--vjoy", default=R"C:\Program Files\vJoy\x64\vJoyInterface.dll"
    )

    args = parser.parse_args()

    device = args.device

    dll = ctypes.CDLL(args.vjoy)
    if not dll.AcquireVJD(device):
        print("Could not acquire device", device)
        exit(1)

    UpdateVJD = dll.UpdateVJD

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", args.port))

        listen_addr = s.getsockname()
        print("Listening for UDP joystick packets @ %s:%d" % listen_addr)

        buf = bytearray(96)
        cbuf = (ctypes.c_char * len(buf)).from_buffer(buf)
        known_addr = None

        while True:
            sz, addr = s.recvfrom_into(buf)
            if sz != 96:
                continue

            if buf[0] != 0x76 or buf[1] != 0x4A or buf[2] != 0x6F or buf[3] != 0x79:
                continue

            if addr != known_addr:
                print("Received data from", addr)
                known_addr = addr

            buf[0] = device
            buf[1] = 0x0
            buf[2] = 0x0
            buf[3] = 0x0

            UpdateVJD(device, cbuf)

    finally:
        dll.RelinquishVJD(device)


if __name__ == "__main__":
    main()
