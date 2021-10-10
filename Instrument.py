import pygame
import numpy


# TODO make inside immutable

class Instrument:

    def __init__(self, sound_path, left_corner, right_corner, channel):
        self.right_corner = right_corner
        self.left_corner = left_corner
        self.sound_path = sound_path
        self.inside = [False, False]
        self.channel = channel

    def corners(self):
        return self.left_corner, self.right_corner

    def inside_info(self):
        return self.inside

    def enter(self, stick_id):
        self.inside[stick_id] = True

    def leave(self, stick_id):
        self.inside[stick_id] = False

    def is_inside(self, x, y):
        return (self.left_corner[0] < x < self.right_corner[0] and
                self.left_corner[1] < y < self.right_corner[1])

    def play(self, volume):
        #pygame.mixer.init()
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.Channel(self.channel).play(pygame.mixer.Sound(self.sound_path))
        pygame.mixer.Channel(self.channel).set_volume(min(1, 0.5 + volume))
        pygame.mixer.music.play()
