from src.parameters import *
from src.player import Player
from src.board import Board
from src.position import Position
from src.load import is_legal_block
import pygame


class Game(object):
    WORLD_PATH = '../worlds/world1-1.txt'
    JUMP_SOUND_PATH = '../sounds/jump.wav'
    MAIN_THEME_PATH = '../sounds/main-theme.mp3'

    VELOCITY_SCALE = 50

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mario')
        pygame.mixer.music.load(Game.MAIN_THEME_PATH)
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.run = True
        self.player = Player()
        self.board = Board(Game.WORLD_PATH)
        self.position = Position(0, 0)
        self.jumpSound = pygame.mixer.Sound(Game.JUMP_SOUND_PATH)
        self.execute()

    def execute(self):
        while self.run:
            self.handle_events()
            self.ticking()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def make_move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.player.increase_velocity()
        else:
            self.player.decrease_velocity()
        if self.check_right():
            self.position.change_position(self.rescale_velocity(), 0)
        self.player.increase_walk_count()

    def rescale_velocity(self):
        return self.player.get_velocity() // Game.VELOCITY_SCALE

    def ticking(self):
        self.tps_delta += self.tps_clock.tick() / 1000.0
        while self.tps_delta > 1 / TPS_MAX:
            keys = pygame.key.get_pressed()
            if not self.player.get_is_jump():
                if self.check_down():
                    self.player.fall()
                else:
                    if keys[pygame.K_UP]:
                        self.player.begin_jump()
                        self.jumpSound.play()
                        self.set_player_height()
            else:
                self.set_player_height()
            self.make_move(keys)
            self.tps_delta -= 1 / TPS_MAX

    def set_player_height(self):
        if self.player.get_top_jump() and self.check_down():
            self.player.fall()
        if not self.player.get_top_jump() and not self.player.is_max_jump_count():
            self.player.jump()
        if not self.player.get_top_jump() and (self.player.is_max_jump_count() or not self.check_up()):
            self.player.gain_top_jump()
        if self.player.get_top_jump() and not self.check_down():
            self.player.end_fall()

    def check_up(self):
        return self.is_legal_point(0, -1) and self.is_legal_point(ELEMENT_SIZE - 1, -1)

    def check_down(self):
        return self.is_legal_point(0, ELEMENT_SIZE) and self.is_legal_point(ELEMENT_SIZE - 1, ELEMENT_SIZE)

    def check_right(self):
        return self.is_legal_point(ELEMENT_SIZE, 0) and self.is_legal_point(ELEMENT_SIZE, ELEMENT_SIZE - 1)

    def check_left(self):
        return self.is_legal_point(-1, 0) and self.is_legal_point(-1, ELEMENT_SIZE - 1)

    def is_legal_point(self, dx, dy):
        point = Position(self.player.get_position_x() + dx, self.player.get_position_y() + dy)
        point.change_position(self.position.get_x(), self.position.get_y())
        point.scale_position(ELEMENT_SIZE)
        return is_legal_block(self.board.get_block(point.get_x(), point.get_y()))

    def draw(self):
        self.screen.fill(SKY_COLOR)
        self.board.draw(self.screen, self.position)
        self.player.draw(self.screen)
        pygame.display.flip()


game = Game()
