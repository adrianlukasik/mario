from src.parameters import *
from src.player import Player
from src.board import Board
from src.position import Position
import pygame


class Game(object):
    WORLD_PATH = '../worlds/world1-1.txt'

    def __init__(self):
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.run = True
        self.player = Player()
        self.board = Board(Game.WORLD_PATH)
        self.position = Position(0, 0)

    def execute(self):
        while self.run:
            self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def ticking(self):
        pass

    def draw(self):
        self.screen.fill(SKY_COLOR)
        self.board.draw(self.screen, self.position)
        self.player.draw(self.screen)
        pygame.display.flip()


game = Game()
