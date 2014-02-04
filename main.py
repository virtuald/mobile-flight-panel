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
   
host = "192.168.30.1"
port = 9009
#buf = 1024
addr = (host,port)
UDPSock = socket(AF_INET,SOCK_DGRAM)

max_view=10
      


class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = time.asctime()

#class TimeApp(App):
#    def build(self):
#        crudeclock = IncrediblyCrudeClock()
#        Clock.schedule_interval(crudeclock.update, 1)
#        return crudeclock
        
        
class MyPanelWidget(BoxLayout):
    t1s="0"    #throttle
    t2s="0"
    sbs="0"    #speedbrake
    fs="0"     #flaps
    gs="1"     #gear
    pbs="1"    #parking brake
    fovs="55"  #FOV zoom
    views="0"  #views
    etrims="0" #elev. trim  TODO
    tbs="0"    #toe brakes  TODO
    revs="0"   #reverser    TODO
    gear=True
    view=0
    
    
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
            out_flaps = 1.0
        self.fs = str(out_flaps)
        print 'flaps:', self.fs
        self.udp_tx()
        
    def send_etrim(self,*args):
        self.etrims = str(self.ids.etrim.value/100)
        print 'elev trim:', self.etrims
        self.udp_tx()
        
        
    def send_gear(self,*args):
        self.gear = self.ids.gear.state
        if (self.gear == "down"):
            self.ids.gear.text = "Gear\nDOWN"
            self.gs="1"
        else:
            self.ids.gear.text = "Gear\nUP"
            self.gs="0"
        print "gear", self.gear, self.gs
        self.udp_tx()
        
    def send_pb(self,*args):
        self.pb= self.ids.pb.state
        if (self.pb == 'down'):
            self.pbs = "1"
        else:
            self.pbs = "0"
        print "park brk", self.pb , self.pbs
        self.udp_tx()
        
    def send_rev(self,*args):
        self.rev= self.ids.rev.state
        if (self.rev == 'down'):
            self.revs = "1"
        else:
            self.revs = "0"
        print "reverser", self.rev , self.revs
        self.udp_tx()

    def send_tb(self,*args):
        self.tb= self.ids.tb.state
        if (self.tb == 'down'):
            self.tbs = "1"
        else:
            self.tbs = "0"
        print "Toe Brake", self.tb , self.tbs
        self.udp_tx()        
        

    def send_zoom(self,*args):
        self.zoom = self.ids.zoom.value
        self.fovs = str(int(102-(self.zoom)))
        print self.fovs
        self.udp_tx()
        
    def send_view(self,*args):
        if(self.view < max_view):
            self.view +=1
        else:
            self.view=0
        self.views = str(self.view)
        print self.views
        self.udp_tx()
        
    def reset_view(self,*args):
        self.view=0
        self.views = str(self.view)
        print self.views
        self.udp_tx()
        
             
        
           
    def udp_tx(self,*args):
        
        
        
        
        outline = self.sbs +","+\
                  self.t1s +","+\
                  self.t2s +","+\
                  self.etrims +","+\
                  self.fs   +","+\
                  self.fovs +","+\
                  self.pbs  +","+\
                  self.revs +","+\
                  self.tbs  +","+\
                  self.gs   +","+\
                  self.views+"\n"
                  
        print outline
        UDPSock.sendto(outline,addr)
            
        

class Panel(App):
    def build(self):
        return MyPanelWidget()

if __name__ == "__main__":
    Panel().run()

