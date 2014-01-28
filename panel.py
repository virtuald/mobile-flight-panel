from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import time

class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = time.asctime()

#class TimeApp(App):
#    def build(self):
#        crudeclock = IncrediblyCrudeClock()
#        Clock.schedule_interval(crudeclock.update, 1)
#        return crudeclock
        
        
class MyPanelWidget(BoxLayout):
    def send_spdbrk(self,*args):
        slider = self.ids.spdbrk
        brake_value = 2 - slider.value
        print 'spdbrk:', brake_value
        
    def send_throttle(self,*args):
        t1 = self.ids.t1.value
        t2 = self.ids.t2.value
        print 'throttles:', int(t1), int(t2)
    def send_flaps(self,*args):
        flaps = self.ids.flaps.value
        print 'flaps:', 4-flaps
              
            
            
        

class Panel(App):
    def build(self):
        return MyPanelWidget()

if __name__ == "__main__":
    Panel().run()

