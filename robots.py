class Object():
    def __init__(self, x = -1, y = -1):
        self._x, self._y = x, y

    @property
    def position(self):
        return self._x, self._y

    @x.setter
    @y.setter
    def position(self, x = self._x, y = self._y):
        self._x, self._y = x, y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y


class MoveObject(Object):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, x, y):
        self._x = x
        self._y = y


class Robot(MoveObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._sclap = False

    @property
    def sclap(self):
        return self._sclap

    #使う予定はないけど、一応用意しておく
    @sclap.setter
    def sclap(self, boolean):
        self._sclap = boolean

    def move(self, x, y, absolute = False):
        if self._sclap == True:
            if absolute == False:
                x += self._x
                y += self._y

            if type(after_board[y][x]) == Robot:
                #collision
                self.kill()
                after_board[y][x].kill()
            elif type(after_board[y][x]) == Player:
                #gameover
                pass

            super().move(x, y)

        else:
            pass

    def kill(self):
        self._sclap = True


class Game():
    def __init__(level = 1, height = 10, width = 10):
        self._level = _level
        self._height = height
        self._width = width
