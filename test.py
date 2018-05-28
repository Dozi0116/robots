class Object():
    def __init__(self, x = -1, y = -1):
        self.x, self.y = x, y

    def get_position(self):
        return self.x, self.y

    def set_position(self, x = self.x, y = self.y):
        self.x, self.y = x, y

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y


class MoveObject(Object):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, x, y, absolute = False):
        if absolute == True:
            self.x = x
            self.y = y
        else: # relative move
            self.x += x
            self.y += y
            self.y += 0
class Robot

class Robot(MoveObject):
    def __init__(self, x, y):
        super().__init__(x, y)
