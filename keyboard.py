# keyboard.py
import pygame

class Keyboard:
    def __init__(self):
        pygame.init()
        self.keys = pygame.key.get_pressed()

    def getKey(self, keyName):
        self.keys = pygame.key.get_pressed()
        keyInput = getattr(pygame, f"K_{keyName}")
        if self.keys[keyInput]:
            return True
        return False
