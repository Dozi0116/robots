import random


class Object():
    def __init__(self, x = -1, y = -1):
        self._x, self._y = x, y

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, pos):
        if len(pos) != 2:
            raise "test"
        (x, y) = pos
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

class Player(MoveObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, x, y, absolute = False):
        if absolute == False:
            x += self._x
            y += self._y

        if before_board[y][x] is None:
            super().move(x, y)
        else:
            #移動できない
            pass


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
    def __init__(self, level = 1, height = 10, width = 10):
        self._level = level
        self._height = height
        self._width = width
        self._robot_left = level * 5
        self._board = [[None for i in range(height)] for j in range(width)]

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        #残りロボ数も更新
        self._robot_left = level * 5

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def robot_left(self):
        return self._robot_left

    @robot_left.setter
    def robot_left(self, robot_left):
        self._robot_left = robot_left

    @property
    def board(self):
        return self._board

    def setting(self):
        temp_list = [i for i in range(self._height * self._width)]
        center_num = self._height // 2 * self._width + self._width // 2
        obj_indices = []
        #プレイヤーの場所確保
        obj_indices.append(temp_list.pop(center_num))
        for _ in range(self._robot_left):
            obj_indices.append(temp_list.pop(temp_list.index(random.choice(temp_list))))

        #マップデータ埋め込み
        index = obj_indices.pop()
        self._board[index // self._width][index % self._width] = Player(x = index % self._width, y = index // self._width)
        for index in obj_indices.pop():
            self._board[i // self._width][i % self._width] = Robot(x = i % self._width, y = i // self._width)


    # def setting(self):
    #     temp_list = [None for i in range(self._height * self._width)]
    #     temp_list[0] = 'Player'
    #     for i in range(1, self._robot_left):
    #         temp_list[i] = 'Robot'
    #
    #     #プレイヤーを中心に
    #     random.shuffle(temp_list)
    #     center_num = self._height // 2 * self._width + self._width // 2
    #     print(center_num)
    #     for i in range(len(temp_list)):
    #         if temp_list[i] == 'Player':
    #             temp_list[i], temp_list[center_num] = temp_list[center_num], temp_list[i]
    #
    #     #マップデータ埋め込み
    #     for i in range(len(temp_list)):
    #         if temp_list[i] == 'Robot':
    #             self._board[i // self._width][i % self._width] = Robot(x = i % self._width, y = i // self._width)
    #         elif temp_list[i] == 'Player':
    #             self._board[i // self._width][i % self._width] = Player(x = i % self._width, y = i // self._width)

    def show(self):
        print('-' * (self._width + 2))
        for y in range(self._height):
            print('|', end = '')
            for x in range(self._width):
                if self._board[y][x] is None:
                    print(' ', end = '')
                elif type(self._board[y][x]) == Robot:
                    if self._board[y][x].sclap == True:
                        print('*', end = '')
                    else:
                        print('+', end = '')
                elif type(self._board[y][x]) == Player:
                    print('@', end = '')
                else:
                    #本来ありえない表示
                    print('#', end = '')

            print('|')

        print('-' * (self._width + 2))

    def action(self):
        #各オブジェクトの移動
        #まずはプレイヤー



def read_command(game_master):

    #cursesでできたら変える
    print('next move >')
    while True:
        try:
            command = int(input())
        except ValueError:
            pass
            print('error. input is integer')
        else:
            if command in range(9+1):
                break
            else:
                print('error. range is 1-9')

    return command

def init_game():
    pass

def preprocess_game():
    #フィールドサイズとかを変更する処理があるなら
    #ここで変更する
    return Game()

def main_game(game_master):
    game_master.setting()
    while True:
        game_master.show()
        command = read_command(game_master)
        game_master.action()


def postprocess_game():
    while True:
        print('continue? y/n')
        command = input()
        if command in {'y', 'n'}:
            break

    return command

if __name__ == '__main__':
    init_game()

    while True:
        game_master = preprocess_game()
        main_game(game_master)
        cont = postprocess_game()

        if cont == 'n':
            break