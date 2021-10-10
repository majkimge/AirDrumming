import pygame
import os
import time

dirname = os.path.dirname(__file__)
hi_hat_filename = os.path.join(dirname, 'sounds/hi_hat.ogg')
snare_filename = os.path.join(dirname, 'sounds/snare.ogg')

pygame.mixer.init()

while True:
        pygame.mixer.music.load(hi_hat_filename)
        pygame.mixer.music.load(snare_filename)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(hi_hat_filename))
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(snare_filename))
        time.sleep(1)

pygame.mixer.music.play()
