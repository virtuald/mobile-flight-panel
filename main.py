from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import time
import sys
from socket import *
   
host = "localhost"
port = 9009
#buf = 1024
addr = (host,port)
UDPSock = socket(AF_INET,SOCK_DGRAM)



class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = time.asctime()

#class TimeApp(App):
#    def build(self):
#        crudeclock = IncrediblyCrudeClock()
#        Clock.schedule_interval(crudeclock.update, 1)
#        return crudeclock
        
        
class MyPanelWidget(BoxLayout):
    t1s="0"
    t2s="0"
    sbs="0"
    fs="0"
    gs="0"
    def send_spdbrk(self,*args):
        slider = self.ids.spdbrk
        self.sbs = str((2 - slider.value)/2)
        print 'spdbrk:', self.sbs
        self.udp_tx()
        
    def send_throttle(self,*args):
        t1 = self.ids.t1.value
        t2 = self.ids.t2.value
        self.t1s = str(t1/100)
        self.t2s = str(t2/100)
        print 'throttles:', self.t1s,self.t2s
        self.udp_tx()
      
    def send_flaps(self,*args):
        flaps = self.ids.flaps.value
        if (flaps == 4):
	  out_flaps = 0
	if (flaps == 3):
	  out_flaps = 0.25
	if (flaps == 2):
	  out_flaps = 0.375
	if (flaps == 1):
	  out_flaps = 0.5
	if (flaps == 0):
	  out_flaps = 0.875
	self.fs = str(out_flaps)
        print 'flaps:', self.fs
        self.udp_tx()
              
    def udp_tx(self,*args):
	outline = self.sbs +","+ self.fs +","+ self.gs +","+ self.t1s +","+ self.t2s + "\n"
	print outline
	UDPSock.sendto(outline,addr)
            
        

class Panel(App):
    def build(self):
        return MyPanelWidget()

if __name__ == "__main__":
    Panel().run()

