import random


# タプルの計算をするプログラム
# 初めに入った数からopeに従い計算していき、結果のタプルを返す。
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


# Enter入力無しで入力処理を行うクラス。
# Win版とUNIX版の2種類が用意されていて、import状況に応じて自動的に分岐される。
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
    screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    #この時、得られるのはb(バイト列)である。
    #そのため、普通の文字として扱うため、.decode()を書いている。
    def __call__(self): return self.impl()


# UNIX版
# stdinから1文字読み込んで、読み込んだ文字を返す。
# この時、副作用として、b'\00'が入ってしまう。
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# Win版
# msvcrt内蔵の関数を呼出して、その値を返すだけ。
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch().decode()


# ゲームボードの上に存在するオブジェクトは必ずこのクラスを継承して作る
# オブジェクトはx,yの座標を持っている。
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


# ゲームボード上を動き回るクラスはこのクラスを継承する。
class MoveObject(Object):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, x, y):
        self._x = x
        self._y = y


# MoveObjectを継承したPlayerクラス
# 移動するときに、オブジェクトが存在していたら動けない。
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

    # 返り値として、GameOverか否かを返す。
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

    #まだスクラップになっていないなら、ロボ残数を減らし、スクラップ状態にする。
    #delとかを使って書いたほうが良かったかも
    def kill(self, game_master):
        if self._sclap == False:
            self._sclap = True
            game_master.robot_left -= 1
            game_master.score += 1


# ゲームの中心となる情報をすべて持っているクラス。
# 基本的に、この中からゲームを操作する。
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
        self._MAX_ROBOT = 40

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        #残りロボ数も更新
        self._robot_left = level * 5
        if self._robot_left > self._MAX_ROBOT:
            self._robot_left = self._MAX_ROBOT

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

    #引数で(y, x)の順で座標を渡すと、その座標に何がいるかを返す関数
    def board_element(self, pos):
        (y, x) = pos
        return self._board[y][x]

    #ゲームの初期状態を生成するクラス。
    #レベルアップごとに呼び出される。
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
        bug_flag = False
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
                    bug_flag = True

            print('|')

        print('-' * (self._width + 2))

        if bug_flag == True:
            #あり得ない表示が出た時のメッセージ
            print('予期せぬエラーが発生しています。')
            print('直ちに開発者に連絡してください。')

        #ゲームステータス表示
        print('lv:'+str(self._level)+', score:'+str(self._score))

    #ロボットがいない場所からランダムに1地点を選び、座標を(y, x)の順で返す関数
    def teleport(self):
        pos_list = []
        for y in range(self._height):
            for x in range(self._width):
                if isinstance(self._board[y][x], Object) == True:
                    pos_list.append((y, x))

        pos = random.choice(pos_list)
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
                            #game over!
                            return True
        else:
            #行動せずに終了 = before状態のまま
            self._after_board = list(self._before_board)

        if self._robot_left <= 0:
            #level up!
            return True

        #最後にafter状態を現在の状態にして終了
        self._board = list(self._after_board)
        #正常終了はFalse
        return False


#どの方向に動くかを読み取る関数
def read_command(game_master):

    print('press "h" key to open help')
    while True:
        try:
            getch = _Getch()
            x = getch()
            command = int(x)

        except ValueError:
            #hキーならヘルプを表示
            if x == 'h':
                print('\nhow to operate')
                print('7 8 9')
                print('4 @ 6')
                print('1 2 3')
                print('\n0 ... random teleport')
                print('5 ... stand-by')

            #ctr-c、EOFが入力されたら、強制終了
            elif x == '\x03':
                # ctr-c
                raise KeyboardInterrupt
            elif x == '\x04':
                # EOF
                raise EOFError


            #数字を読み込んだ直後の末端記号が入ったときは読み飛ばす
            #それ以外の文字は入力範囲外のものだから、エラーメッセージを表示
            elif x != '\x00':
                print('error. input is integer')

        else:
            #コマンドは0～9、つまりrange(10)
            if command in range(9+1):
                break
            else:
                print('error. range is 1-9')

    return command


#ゲーム開始から終了までを司る関数
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
                game_master.score += game_master.level * 10
                game_master.setting()

            else:
                #game over
                print('GAME OVER')
                return None


#ゲームに必要な前準備を書いておく
#今回みたいに1行だったら関数にする必要ないが、拡張したときにわかりやすくなるように
def init_game():
    game_master = Game()
    return game_master


#ゲーム終了後の処理を行う関数
#主に、続けてプレイするかを聞いている。
def postprocess_game():
    print('continue? y/n')
    while True:
        getch = _Getch()
        command = getch()
        if command in {'y', 'n'}:
            break

    return command


if __name__ == '__main__':

    game_master = init_game()
    while True:
        main_game(game_master)
        cont = postprocess_game()

        if cont == 'n':
            break
