from src.load import *
from src.parameters import *
from src.position import *


class Board(object):
    # Board images.
    BRICK = load_board_image('brick.png')
    FLOOR = load_board_image('floor.png')
    PYRAMID = load_board_image('pyramid.png')
    QUESTION_MARK = load_board_image('qm.png')
    LEFT_BODY_PIPE = load_board_image('left_body_pipe.png')
    LEFT_HEAD_PIPE = load_board_image('left_head_pipe.png')
    RIGHT_BODY_PIPE = load_board_image('right_body_pipe.png')
    RIGHT_HEAD_PIPE = load_board_image('right_head_pipe.png')

    def __init__(self, path_world):
        self.blocks = get_list_blocks(path_world)

    def draw(self, screen, game_position):
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                block = self.blocks[i][j]
                position = Position(j * ELEMENT_SIZE - game_position.get_x(), i * ELEMENT_SIZE)
                if block == 'b':
                    screen.blit(Board.BRICK, position.get_position())
                elif block == '#':
                    screen.blit(Board.FLOOR, position.get_position())
                elif block == 'p':
                    screen.blit(Board.PYRAMID, position.get_position())
                elif block == '?':
                    screen.blit(Board.QUESTION_MARK, position.get_position())
                elif block == 't':
                    if self.blocks[i - 1][j] == 't':
                        if self.blocks[i][j + 1] == 't':
                            screen.blit(Board.LEFT_BODY_PIPE, position.get_position())
                        else:
                            screen.blit(Board.RIGHT_BODY_PIPE, position.get_position())
                    else:
                        if self.blocks[i][j + 1] == 't':
                            screen.blit(Board.LEFT_HEAD_PIPE, position.get_position())
                        else:
                            screen.blit(Board.RIGHT_HEAD_PIPE, position.get_position())
