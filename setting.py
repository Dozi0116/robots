tenp_list = []
center_x = self._width // 2
center_y = self._height // 2
for y in range(self._height):
    for x in range(self._width):
        if y == center_y and x == center_x: 
            pass
        else:
            temp_list.append((y, x))

random.shuffle(temp_list)
for y, x in temp_list[:self._robot_left]:
    self._board[y][x] = Robot(y = y, x = x)

self._board[center_y][center_x] = Player(y = center_y, x = center_x)
