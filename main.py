from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from kivy.properties import ListProperty, NumericProperty

from kivy.clock import Clock
from kivy.vector import Vector

from random import random

class Game(FloatLayout):
    poles = ListProperty([])

    def update(self, dt):
        self.ids.kiwi.update(dt)
        self.update_poles(dt)
        self.remove_poles()
        self.check_collisions()

    def check_collisions(self):
        for pole in self.poles:
            if self.ids.kiwi.collide_widget(pole):
                self.reset()

    def reset(self, *args):
        for pole in self.poles:
            if pole in self.children:
                self.remove_widget(pole)
        self.poles = []
        self.ids.kiwi.height_frac = 0.5

    def spawn_pole(self, *args):
        gap_height = random() * 0.7 + 0.15
        p1 = Pole(hfrac=gap_height+0.15, dist=1.)
        p2 = Pole(hfrac=gap_height-0.15-1.0, dist=1.)
        self.poles.append(p1)
        self.poles.append(p2)
        self.add_widget(p1)
        self.add_widget(p2)

    def update_poles(self, dt):
        for pole in self.poles:
            if pole in self.children:
                pole.update(dt)

    def remove_poles(self):
        for pole in self.poles:
            if pole in self.children and pole.dist < -0.2:
                self.remove_widget(pole)

class Pole(Widget):
    velocity = NumericProperty(-0.1)
    dist = NumericProperty(0)
    hfrac = NumericProperty(0.5)
    def __init__(self, **kwargs):
        super(Pole, self).__init__(**kwargs)

    def update(self, dt):
        print 'pole update', self.velocity, self.size
        print 'start', self.dist
        self.dist += self.velocity*dt
        print 'now', self.dist

class Kiwi(Image):
    acceleration = NumericProperty(-0.07)
    velocity = NumericProperty(0)
    def on_touch_down(self, touch):
        self.velocity = 0.9

    def update(self, dt):
        self.velocity += self.acceleration
        self.height_frac += self.velocity*dt + 0.5*self.acceleration*dt**2
        if self.height_frac < 0.:
            self.parent.reset()



class FlApp(App):
    def build(self):
        g = Game()
        Clock.schedule_interval(g.update, 1./60)
        Clock.schedule_interval(g.spawn_pole, 2)
        return g

if __name__ == "__main__":
    FlApp().run()
