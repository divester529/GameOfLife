import pygame, sys, time;
from simulation import GameOfLife

SCREEN_RES = (1280, 960)

def main():
    pygame.init()
    pygame.display.set_caption('Conway\'s Game Of Life')
    display = pygame.display.set_mode(SCREEN_RES, 0, 32)

    instance = GameOfLife(100, 100, display)

    while True:
        instance.getInput()

        if instance.isSimulating():
            instance.runSimulation()
            
        instance.drawGameboard()

        instance.tick()

main()