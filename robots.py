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


    # 移動したかどうかをTFで返す
    def move(self, x, y, game_master, absolute = False):
        if absolute == False:
            x += self._x
            y += self._y

        if x in range(game_master._width) \
        and y in range(game_master._height) \
        and type(game_master._before_board[y][x]) != Robot:
            #移動ができる
            game_master._after_board[y][x] = self
            super().move(x, y)
            game_master.player_pos = (y, x)
            return True

        else:
            print('move error. now pos is ' + str((x, y)))
            return False



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

    #GameOverか否かを返す
    def move(self, game_master):
        if self._sclap == False:
            #移動する座標の算出
            pos = []
            for p, e in zip(game_master.player_pos, (self._y, self._x)):
                if p - e > 0:
                    pos.append(1)
                elif p - e == 0:
                    pos.append(0)
                else:
                    pos.append(-1)

            y = self._y + pos[0]
            x = self._x + pos[1]

            if type(game_master.after_board[y][x]) == Robot:
                #collision
                self.kill(game_master)
                game_master.after_board[y][x].kill(game_master)

            elif type(game_master.after_board[y][x]) == Player:
                #gameover
                return True

            game_master.after_board[y][x] = self
            super().move(x, y)

        else:
            #先に移動してきたロボットの処理
            if type(game_master.after_board[self._y][self._x]) == Robot:
                game_master.after_board[self._y][self._x].kill(game_master)

            #スクラップだから動かない
            game_master.after_board[self._y][self._x] = self

    def kill(self, game_master):
        if self._sclap == False:
            self._sclap = True
            game_master.robot_left -= 1
            game_master.score += game_master.level * 1


class Game():
    def __init__(self, level = 1, height = 10, width = 10):
        self._level = level
        self._height = height
        self._width = width
        self._robot_left = level * 5
        self._board = [[None for i in range(height)] for j in range(width)]
        self._before_board = list(self._board)
        self._after_board = list(self._board)
        self._score = 0

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        #残りロボ数も更新
        self._robot_left = level * 5
        if self._robot_left > 40:
            self._robot_left = 40

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, num):
        self._score = num

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
    def player_pos(self):
        return self._player_pos

    @player_pos.setter
    def player_pos(self, tp):
        self._player_pos = tp


    def setting(self):
        self._board = [[None for i in range(self._height)] for j in range(self._width)]
        temp_list = []
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

        self._board[center_y][center_x] = Player(y = center_y, x = center_x)
        self._player_pos = (center_y, center_x)

    def show(self):
        #ゲームボード表示
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

        #ゲームステータス表示
        print('lv:'+str(self._level)+', score:'+str(self._score))

    def teleport(self):
        pos_list = []
        for y in range(self._height):
            for x in range(self._width):
                if type(self._board[y][x]) != Robot:
                    pos_list.append((y, x))

        pos = random.choice(pos_list)
        # return tuple((a-b) for a,b in zip(pos, self._player_pos))
        return tuple_calc(pos, self._player_pos, ope='sub')

    #なにかしらのイベントが有る場合、Trueで返す
    def action(self, command):
        self._before_board = list(self._board) #中身のコピー
        self._after_board = [[None for i in range(self._height)] \
        for j in range(self._width)]

        #各オブジェクトの移動
        #プレイヤー
        #(y, x)の順で入れる
        if command == 0:
            tp = self.teleport()
        else:
            tp = (None, None)
        cmd_to_move = [tp,(1,-1),(1,0),(1,1),(0,-1),(0,0),(0,1),(-1,-1),(-1,0),(-1,1)]
        (move_y, move_x) = cmd_to_move[command]
        if self.board_element(self._player_pos).move(move_x, move_y, game_master):
            #プレイヤーが正常に移動した場合、敵の移動
            for enemy_pos_y in range(self._height):
                for enemy_pos_x in range(self._width):
                    if type(self.board_element((enemy_pos_y, enemy_pos_x))) == Robot:
                        gameover = self.board_element((enemy_pos_y, enemy_pos_x)).move(game_master)
                        if gameover == True:
                            #print('game over!')
                            return True

        else:
            #行動せずに終了 = before状態のまま
            self._after_board = list(self._before_board)




        if self._robot_left <= 0:
            #print('level up!')
            return True

        #最後にafter状態を現在の状態にして終了
        self._board = list(self._after_board)
        #正常終了はFalse
        return False


def read_command(game_master):

    #cursesでできたら変える
    print('next move >', end=' ')
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
        event = game_master.action(command)
        if event == True:
            if game_master.robot_left <= 0:
                #level up
                print('CLEAR! LEVEL' + str(game_master.level) + ' => ' + str(game_master.level + 1))
                game_master.level += 1
                game_master.setting()

            else:
                #game over
                print('GAME OVER')
                return None



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
