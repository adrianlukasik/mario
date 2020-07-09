from src.parameters import *
from src.position import *
from src.load import *


class Player(object):
    ACCELERATION = 1
    VELOCITY_MAX = 200 * ACCELERATION
    JUMP_MAX = 4 * ELEMENT_SIZE
    # GRAVITY_ACCELERATION = 1

    # Mario images.
    WALK_RIGHT = [load_mario_image('r1.png'), load_mario_image('r2.png'), load_mario_image('r3.png')]
    STAND_RIGHT = load_mario_image('r.png')
    JUMP_RIGHT = load_mario_image('r_jump.png')
    WALK_LEFT = [load_mario_image('l1.png'), load_mario_image('l2.png'), load_mario_image('l3.png')]
    STAND_LEFT = load_mario_image('l.png')
    JUMP_LEFT = load_mario_image('l_jump.png')

    def __init__(self):
        self.position = Position(WIDTH // 2, HEIGHT - 3 * ELEMENT_SIZE)
        self.key = pygame.K_RIGHT
        self.velocity = 0
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 0
        # self.fallingSpeed = 0

    def set_key(self, key):
        self.key = key

    def increase_velocity(self):
        if self.velocity < Player.VELOCITY_MAX:
            self.velocity += Player.ACCELERATION

    def decrease_velocity(self):
        if self.velocity > 0:
            self.velocity -= Player.ACCELERATION

    def jump(self):
        self.position.change_position(0, -1)

    def fall(self):
        self.position.change_position(0, 1)

    def draw(self, screen):
        if self.isJump:
            if self.key == pygame.K_RIGHT:
                screen.blit(Player.JUMP_RIGHT, self.position.get_position())
            else:
                screen.blit(Player.JUMP_LEFT, self.position.get_position())
        elif self.velocity == 0:
            if self.key == pygame.K_RIGHT:
                screen.blit(Player.STAND_RIGHT, self.position.get_position())
            else:
                screen.blit(Player.STAND_LEFT, self.position.get_position())
        elif self.key == pygame.K_RIGHT:
            self.walkCount %= 24
            screen.blit(Player.WALK_RIGHT[self.walkCount // 8], self.position)
        else:
            self.walkCount %= 24
            screen.blit(Player.WALK_LEFT[self.walkCount // 8], self.position)
