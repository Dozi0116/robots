import random

def tuple_calc(*tuples, ope):
    ans_list = [0] * len(tuples[0])
    first_flg = True
    for tp in tuples:
        for i in range(len(tp)):
            if ope == 'add' or first_flg == True: #初めの数から後ろを引いていくための準備
                ans_list[i] += tp[i]
            elif ope == 'sub':
                ans_list[i] -= tp[i]
        first_flg = False

    return tuple(ans_list)


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

    def move(self, x, y, game_master, absolute = False):
        if absolute == False:
            x += self._x
            y += self._y

        super().move(x, y)
        print(y, x)
        game_master.player_pos = (y, x)


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

    def move(self, x, y, game_master, absolute = False):
        if self._sclap == True:
            if absolute == False:
                x += self._x
                y += self._y

            if type(game_master.after_board[y][x]) == Robot:
                #collision
                self.kill(game_master)
                game_master.after_board[y][x].kill(game_master)
            elif type(game_master.after_board[y][x]) == Player:
                #gameover
                pass

            super().move(x, y)

        else:
            pass

    def kill(self, game_master):
        if self._sclap == False:
            self._sclap = True
            game_master.robot_left -= 1


class Game():
    def __init__(self, level = 1, height = 10, width = 10):
        self._level = level
        self._height = height
        self._width = width
        self._robot_left = level * 5
        self._board = [[None for i in range(height)] for j in range(width)]
        self._before_board = list(self._board)
        self._after_board = list(self._board)
        self._player_pos = (None, None)

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

    def board_element(self, pos):
        (y, x) = pos
        return self._board[y][x]

    @property
    def before_board(self):
        return self._before_board

    @property
    def after_board(self):
        return self._after_board

    @property
    def enemy_pos_list(self):
        return self._enemy_pos_list

    @property
    def player_pos(self):
        return self._player_pos

    @player_pos.setter
    def player_pos(self, tp):
        self._player_pos = tp


    def setting(self):
        temp_list = []
        self._enemy_pos_list = []
        center_x = self._width // 2
        center_y = self._height // 2
        center = (center_y, center_x)
        for y in range(self._height):
            for x in range(self._width):
                if (y, x) != center:
                    temp_list.append((y, x))
        #it = itertools.product(range(self._height), range(self._width))
        #temp_list = [e for e in it if e != center]

        random.shuffle(temp_list)
        for y, x in temp_list[:self._robot_left]:
            self._board[y][x] = Robot(y = y, x = x)
            self._enemy_pos_list.append((y, x))

        self._board[center_y][center_x] = Player(y = center_y, x = center_x)
        self._player_pos = (center_y, center_x)

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

    def teleport(self):
        pos_list = []
        for y in range(self._height):
            for x in range(self._width):
                if type(self._board[y][x]) != Robot:
                    pos_list.append((y, x))

        pos = random.choice(pos_list)
        print(pos, self._player_pos)
        # return tuple((a-b) for a,b in zip(pos, self._player_pos))
        return tuple_calc(pos, self._player_pos, ope='sub')

    def action(self, command):
        self._before_board = list(self._board) #中身のコピー
        self._after_board = [[None for i in range(self._height)] \
        for j in range(self._width)]
        #(y, x)の順で入れる
        if command == 0:
            tp = self.teleport()
        else:
            tp = (None, None)
        cmd_to_move = [tp,(1,-1),(1,0),(1,1),(0,-1),(0,0),(0,1),(-1,-1),(-1,0),(-1,1)]
        move = cmd_to_move[command]
        #各オブジェクトの移動
        #まずはプレイヤー
        print(self._player_pos)
        (move_pos_y, move_pos_x) = tuple_calc(self._player_pos, move, ope='add')
        if move_pos_x in range(self._width) \
        and move_pos_y in range(self._height) \
        and type(self._before_board[move_pos_y][move_pos_x]) != Robot:
            #移動ができる
            print(self._player_pos)
            self._after_board[move_pos_y][move_pos_x] \
            = self.board_element(self._player_pos)
            self._after_board[move_pos_y][move_pos_x].move(move_pos_y, move_pos_x, game_master, absolute = True)

        else:
            print('move error. now pos is ' + str((move_pos_x, move_pos_y)))

        # temp move
        for (enemy_pos_y, enemy_pos_x) in self._enemy_pos_list:
            self._after_board[enemy_pos_y][enemy_pos_x] = self.board_element((enemy_pos_y, enemy_pos_x))
        self._board = list(self._after_board)



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
        game_master.action(command)


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
