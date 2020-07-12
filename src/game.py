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
        self.position = Position((0, 0))
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not self.player.get_is_jump():
                self.player.begin_jump()
                self.jumpSound.play()

    def make_move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.player.set_key(pygame.K_RIGHT)
            self.player.increase_velocity()
        elif keys[pygame.K_LEFT]:
            self.player.set_key(pygame.K_LEFT)
            self.player.change_player_position((-1, 0))
        else:
            self.player.decrease_velocity()
        rescale_velocity = self.get_rescale_velocity()
        while not self.check_right(rescale_velocity):
            rescale_velocity -= 1
        self.position.change_position(rescale_velocity, 0)
        self.player.increase_walk_count()

    def get_rescale_velocity(self):
        return self.player.get_velocity() // Game.VELOCITY_SCALE

    def ticking(self):
        self.tps_delta += self.tps_clock.tick() / 1000.0
        while self.tps_delta > 1 / TPS_MAX:
            keys = pygame.key.get_pressed()
            if not self.player.get_is_jump():
                if self.check_down():
                    self.player.begin_jump()
                    self.player.gain_top_jump()
                    self.player.fall()
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
        p1 = self.player.get_top_right_corner()
        p2 = self.player.get_top_left_corner()
        return self.is_legal_point(p1[0], p1[1] - 1) and self.is_legal_point(p2[0], p2[1] - 1)

    # Będzie można poprawić żeby nie spadać o stałą odległość tylko uwzględniając przyspieszenie grawitacyjne.
    def check_down(self):
        p1 = self.player.get_bottom_right_corner()
        p2 = self.player.get_bottom_left_corner()
        return self.is_legal_point(p1[0], p1[1] + 1) and self.is_legal_point(p2[0], p2[1] + 1)

    def check_right(self, distance):
        p1 = self.player.get_top_right_corner()
        p2 = self.player.get_bottom_right_corner()
        return self.is_legal_point(p1[0] + distance, p1[1]) and self.is_legal_point(p2[0] + distance, p2[1])

    def is_legal_point(self, x, y):
        point = Position((x, y))
        point.change_position(self.position.get_x(), self.position.get_y())
        point.scale_position(ELEMENT_SIZE)
        return is_legal_block(self.board.get_block(point.get_x(), point.get_y()))

    def draw(self):
        self.screen.fill(SKY_COLOR)
        self.board.draw(self.screen, self.position)
        self.player.draw(self.screen)
        pygame.display.flip()


game = Game()
