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


import os.path

from kivy.app import App

from kivy.core.text import LabelBase
from kivy.factory import Factory
from kivy.resources import resource_add_path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

import vjoy_client

PORT = 27257
DEFAULT_HOST = "10.24.23.10"


class SettingsPopup(Popup):
    def __init__(self, vjoy):
        super().__init__()
        self.vjoy = vjoy

    def on_ok(self):
        self.vjoy.set_server(self.ids.ip.text, PORT)
        self.dismiss()


class FlightPanel(BoxLayout):

    axis_map = {
        "t1": vjoy_client.VJoyClient.AXIS_X,
        "t2": vjoy_client.VJoyClient.AXIS_Y,
        "trim": vjoy_client.VJoyClient.AXIS_Z,
    }

    button_map = {
        "spdbrk_ret": 1,
        "spdbrk_half": 2,
        "spdbrk_full": 3,
        "flaps_ret": 4,
        "flaps_1": 5,
        "flaps_2": 6,
        "flaps_3": 7,
        "flaps_4": 8,
        "gearup": 10,
        "geardown": 11,
        "misc1": 12,
        "misc2": 13,
        "misc3": 14,
        "misc4": 15,
        "alt+": 16,
        "alt-": 17,
        "heading+": 18,
        "heading-": 19,
    }

    def __init__(self, server, port) -> None:
        super().__init__()
        self.vjoy = vjoy_client.VJoyClient(server, port)

    def set_button(self, name):
        self.vjoy.set_button(self.button_map[name], True)

    def unset_button(self, name):
        self.vjoy.set_button(self.button_map[name], False)

    def show_popup(self):
        p = SettingsPopup(self.vjoy)
        host, _ = self.vjoy.get_server()
        p.ids.ip.text = host
        p.open()

    def send_spdbrk(self):
        spdbrk = self.ids.spdbrk.value
        self.vjoy.set_buttons(
            (self.button_map["spdbrk_ret"], spdbrk == 2),
            (self.button_map["spdbrk_half"], spdbrk == 1),
            (self.button_map["spdbrk_full"], spdbrk == 0),
        )

    def send_throttle(self):
        t1 = self.ids.t1.value / 100.0
        t2 = self.ids.t2.value / 100.0

        self.vjoy.set_axis(self.axis_map["t1"], t1)
        self.vjoy.set_axis(self.axis_map["t2"], t2)

    def send_flaps(self):
        flaps = self.ids.flaps.value

        self.vjoy.set_buttons(
            (self.button_map["flaps_ret"], flaps == 4),
            (self.button_map["flaps_1"], flaps == 3),
            (self.button_map["flaps_2"], flaps == 2),
            (self.button_map["flaps_3"], flaps == 1),
            (self.button_map["flaps_4"], flaps == 0),
        )

    def send_etrim(self):
        # min/max is 40%
        value = (self.ids.etrim.value - 50) / -125.0
        self.vjoy.set_axis(self.axis_map["trim"], value)


class LastWidget(Widget):
    pass


class BoxLastLayout(BoxLayout):
    def do_layout(self, *args):
        children = self.children
        hints = sum(c.size_hint_x for c in children[1:])
        children[0].size_hint_x = 1.0 - hints
        super().do_layout(*args)


class Panel(App):
    def build(self):
        root = os.path.join(os.path.dirname(__file__))

        # Register shiny font
        font_path = os.path.join(root, 'assets', 'FuturaRenner-Regular.ttf')
        LabelBase.register("Futura", font_path)

        # Set images directory
        resource_add_path(os.path.join(root, "images"))

        Factory.register(cls=BoxLastLayout, classname="BoxLastLayout")
        return FlightPanel(DEFAULT_HOST, 27257)


if __name__ == "__main__":
    Panel().run()
