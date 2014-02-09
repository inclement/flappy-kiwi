from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scatter import Scatter

from kivy.properties import ListProperty, NumericProperty

from kivy.clock import Clock
from kivy.vector import Vector

from kivy.animation import Animation

from random import random

class GameManager(ScreenManager):
    pass

class Game(FloatLayout):
    poles = ListProperty([])
    label_opacity = NumericProperty()
    num = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.update, 1./60)
        Clock.schedule_interval(self.spawn_pole, 2)

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
        self.ids.kiwi.velocity = 0.05
        self.label_opacity = 1.
        self.num = 0
        Animation.cancel_all(self)
        Animation(label_opacity=0, duration=1).start(self)

    def spawn_pole(self, *args):
        gap_height = random() * 0.7 + 0.15
        p1 = Pole(hfrac=gap_height+0.15, dist=1., x=1000)
        p2 = Pole(hfrac=gap_height-0.15-1.0, dist=1., x=1000)
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
                self.num += 0.50001

class Pole(Widget):
    velocity = NumericProperty(-0.1)
    dist = NumericProperty(0)
    hfrac = NumericProperty(0.5)
    def __init__(self, **kwargs):
        super(Pole, self).__init__(**kwargs)

    def update(self, dt):
        self.dist += self.velocity*dt

class Kiwi(Image):
    acceleration = NumericProperty(-0.07)
    velocity = NumericProperty(0)
    def on_touch_down(self, touch):
        self.velocity = 0.9

    def update(self, dt):
        self.velocity += self.acceleration
        self.height_frac += self.velocity*dt + 0.5*self.acceleration*dt**2
        if self.height_frac < -0.1:
            self.parent.reset()


class FlApp(App):
    def build(self):
        return GameManager()

if __name__ == "__main__":
    FlApp().run()
