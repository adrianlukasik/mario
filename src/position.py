class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_position(self):
        return self.x, self.y

    def change_position(self, x, y):
        self.x += x
        self.y += y

    def scale_position(self, scalar):
        self.x //= scalar
        self.y //= scalar
