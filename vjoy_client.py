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


import socket
import struct
import time
import threading


class VJoyClient:
    """

    Sends virtual joystick data as UDP packets to the vjoy_feeder application.

    typedef struct _JOYSTICK_POSITION
    {
        BYTE    bDevice; // Index of device. 1-based
        LONG    wThrottle;
        LONG    wRudder;
        LONG    wAileron;
        LONG    wAxisX;
        LONG    wAxisY;
        LONG    wAxisZ;
        LONG    wAxisXRot;
        LONG    wAxisYRot;
        LONG    wAxisZRot;
        LONG    wSlider;
        LONG    wDial;
        LONG    wWheel;
        LONG    wAxisVX;
        LONG    wAxisVY;
        LONG    wAxisVZ;
        LONG    wAxisVBRX;
        LONG    wAxisVBRY;
        LONG    wAxisVBRZ;
        LONG    lButtons;   // 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
        DWORD   bHats;      // Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
        DWORD   bHatsEx1;   // 16-bit of continuous HAT switch
        DWORD   bHatsEx2;   // 16-bit of continuous HAT switch
        DWORD   bHatsEx3;   // 16-bit of continuous HAT switch
    } JOYSTICK_POSITION, *PJOYSTICK_POSITION;
    """

    AXIS_X = 4
    AXIS_Y = 5
    AXIS_Z = 6
    AXIS_XROT = 7
    AXIS_YROT = 8
    AXIS_ZROT = 9
    AXIS_SLIDER = 10
    AXIS_DIAL = 11

    def __init__(self, server, port) -> None:

        self.lock = threading.Condition()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (server, port)

        self.updated = False
        self.raw_data = [0] * 24

        # packet signature, device cannot be selected over the network
        self.raw_data[0] = 0x796F4A76

        self.packer = struct.Struct("<IlllllllllllllllllllIIII")

        self.thread = threading.Thread(target=self.send_thread, daemon=True)
        self.thread.start()

    def get_server(self):
        return self.addr

    def set_server(self, server, port):
        with self.lock:
            self.addr = (server, port)
            self.updated = True
            self.lock.notify()

    def set_axis(self, axis, value):
        # print("axis", axis, value)
        intval = max(0x1, min(0x8000, int((value * 0x4000) + 0x4000)))
        with self.lock:
            self.raw_data[axis] = intval
            self.updated = True
            self.lock.notify()

    def set_buttons(self, *args):
        # for index, value in args:
        #     print("button", index, value)

        with self.lock:
            for index, value in args:
                if value:
                    self.raw_data[19] |= 1 << index
                else:
                    self.raw_data[19] &= ~(1 << index)

            self.updated = True
            self.lock.notify()

    def set_button(self, index, value):
        # print("button", index, value)
        with self.lock:
            if value:
                self.raw_data[19] |= 1 << index
            else:
                self.raw_data[19] &= ~(1 << index)

            self.updated = True
            self.lock.notify()

    def send_thread(self):

        sock = self.sock
        lock = self.lock

        raw_data = self.raw_data
        packer = self.packer
        buf = bytearray(packer.size)

        while True:
            with lock:
                lock.wait_for(lambda: self.updated)
                packer.pack_into(buf, 0, *raw_data)
                self.updated = False

            try:
                sock.sendto(buf, self.addr)
            except IOError:
                pass

            # Limit sends to one per ms
            time.sleep(0.001)
