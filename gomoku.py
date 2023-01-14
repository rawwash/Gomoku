#Yousef Alrawwash & Asser Abdelgawad - Project 2: Gomoku - November 19, 2021

'''This program initiates a game of standard gomoku between the user and an AI engine'''

def is_empty(board):

  '''Check if there are no stones on board'''
  for i in range(8):
    for j in range(8):
      if board[i][j] != " ":
        return False

  return True

def is_side_closed(one_before_y, one_before_x, one_after_y, one_after_x):

  initial_side = False
  final_side = False

  if one_before_y < 0 or one_before_y > 7 or one_before_x < 0 or one_before_x > 7:
    initial_side = True
  if one_after_y < 0 or one_after_y > 7 or one_after_x < 0 or one_after_x > 7:
    final_side = True

  return initial_side, final_side




def is_bounded(board, y_end, x_end, length, d_y, d_x):

  #evaluate before and after
  one_before_x = x_end - (length*d_x)
  one_before_y = y_end - (length*d_y)

  one_after_x = x_end + d_x
  one_after_y = y_end + d_y

  initial_side = False
  final_side = False

  initial_side = is_side_closed(one_before_y, one_before_x, one_after_y, one_after_x)[0]

  final_side = is_side_closed(one_before_y, one_before_x, one_after_y, one_after_x)[1]



  if not initial_side and not final_side:
    #no edges or corners
    if board[one_before_y][one_before_x] != " " and board[one_after_y][one_after_x] != " ":
      return "CLOSED"

    elif board[one_before_y][one_before_x] != " " or board[one_after_y][one_after_x] != " ":
      return "SEMIOPEN"

    else:
      return "OPEN"

  else:
    #blocked on both sides
    if final_side and initial_side:
      return "CLOSED"

    if initial_side:
      if board[one_after_y][one_after_x] != " ":
        return "CLOSED"

      elif board[one_after_y][one_after_x] == " ":
        return "SEMIOPEN"


    elif final_side:
      if board[one_before_y][one_before_x] != " ":
        return "CLOSED"

      elif board[one_before_y][one_before_x] == " ":
        return "SEMIOPEN"








def detect_row(board, col, y_start, x_start, length, d_y, d_x):

  open_seq_count, semi_open_seq_count, i = 0, 0, 0

  begin_y, begin_x = 0, 0

  while -1 < begin_y < 8 and -1 < begin_x < 8:

    wrong_length = False
    j = 0
    begin_y = y_start + i*d_y
    begin_x = x_start + i*d_x

    #re-check
    if not (-1 < begin_y < 8 and -1 < begin_x < 8):
      continue


    #count the streak
    if board[begin_y + j*d_y][begin_x + j*d_x] != col:
      i += 1
      continue

    while board[begin_y + j*d_y][begin_x + j*d_x] == col:
        j += 1

        #re-check
        if not (-1 < begin_y + j*d_y < 8 and -1 < begin_x + j*d_x < 8):
          break

    #if wrong length, move on to next sequence
    if j != length:
      wrong_length = True

    if wrong_length:
      i += j
    #if right length, check open and semiopen
    else:
      y_end = begin_y + length*d_y - d_y
      x_end = begin_x + length*d_x - d_x

      #check if open or semiopen
      if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
        i += length
        semi_open_seq_count += 1

      elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
        i += length
        open_seq_count += 1

      else:
        i += length


  return open_seq_count, semi_open_seq_count



#edit detect_rows_closed()
#detect_row(board, col, y_start, x_start, length, d_y, d_x)
def detect_rows(board, col, length):

  open_seq_count, semi_open_seq_count = 0, 0

  for i in range(8):
    #horizontals
    open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[0]

    semi_open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[1]

    #verticals
    open_seq_count += detect_row(board, col, 0, i, length, 1, 0)[0]

    semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 0)[1]

  #UtoL
  for i in range(8):
    open_seq_count += detect_row(board, col, i, 0, length, 1, 1)[0]

    semi_open_seq_count += detect_row(board, col, i, 0, length, 1, 1)[1]

    if i == 7:
      for j in range(7):
        open_seq_count += detect_row(board, col, 0, j + 1, length, 1, 1)[0]

        semi_open_seq_count += detect_row(board, col, 0, j + 1, length, 1, 1)[1]

  #LtoU
  for i in range(7,-1,-1):
    open_seq_count += detect_row(board, col, i, 0, length, -1, 1)[0]

    semi_open_seq_count += detect_row(board, col, i, 0, length, -1, 1)[1]

    if i == 0:
      for j in range(7):
        open_seq_count += detect_row(board, col, 7, j + 1, length, -1, 1)[0]

        semi_open_seq_count += detect_row(board, col, 7, j + 1, length, -1, 1)[1]

  return open_seq_count, semi_open_seq_count


#closed wins
def detect_row_closed(board, col, y_start, x_start, length, d_y, d_x):

  closed_seq_count = 0
  i = 0

  begin_y, begin_x = 0, 0

  while -1 < begin_y < 8 and -1 < begin_x < 8:

    wrong_length = False
    j = 0
    begin_y = y_start + i*d_y
    begin_x = x_start + i*d_x

    #re-check
    if not (-1 < begin_y < 8 and -1 < begin_x < 8):
      continue


    #count the streak
    if board[begin_y + j*d_y][begin_x + j*d_x] != col:
      i += 1
      continue

    while board[begin_y + j*d_y][begin_x + j*d_x] == col:
        j += 1

        #re-check
        if not (-1 < begin_y + j*d_y < 8 and -1 < begin_x + j*d_x < 8):
          break

    #if wrong length, move on to next sequence
    if j != length:
      wrong_length = True

    if wrong_length:
      i += j
    #if right length, check open and semiopen
    else:
      y_end = begin_y + length*d_y - d_y
      x_end = begin_x + length*d_x - d_x

      #check if open or semiopen
      if is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
        i += length
        closed_seq_count += 1

      else:
        i += length

  return closed_seq_count





#detect_rows_closed(board, col, y_start, x_start, length, d_y, d_x)
def detect_rows_closed(board, col, length):

  closed_seq_count = 0

  for i in range(8):
    #horizontals
    closed_seq_count += detect_row_closed(board, col, i, 0, length, 0, 1)

    #verticals
    closed_seq_count += detect_row_closed(board, col, 0, i, length, 1, 0)


  #UtoL
  for i in range(8):
    closed_seq_count += detect_row_closed(board, col, i, 0, length, 1, 1)

    if i == 7:
      for j in range(7):
        closed_seq_count += detect_row_closed(board, col, 0, j + 1, length, 1, 1)


  #LtoU
  for i in range(7,-1,-1):
    closed_seq_count += detect_row_closed(board, col, i, 0, length, -1, 1)

    if i == 0:
      for j in range(7):
        closed_seq_count += detect_row_closed(board, col, 7, j + 1, length, -1, 1)


  return closed_seq_count





def search_max(board):

  move_y, move_x = 0, 0
  maxScore = -100001
  save_y, save_x = 0, 0

  for i in range(8):
    for j in range(8):
      move_y, move_x = i, j
      if (board[move_y][move_x] == " "):
        board[move_y][move_x] = "b"
        if score(board) >= maxScore:
          maxScore = score(board)
          save_y, save_x = move_y, move_x
        board[move_y][move_x] = " "


  move_y, move_x = save_y, save_x

  return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

 #is_win needs a detect_row closed
def is_win(board):

  #winning
  if detect_rows(board, "b", 5)[0] != 0 or detect_rows(board, "b", 5)[1] != 0 or detect_rows_closed(board, "b", 5) != 0:
    return "Black won"
  if detect_rows(board, "w", 5)[0] != 0 or detect_rows(board, "w", 5)[1] != 0 or detect_rows_closed(board, "w", 5) != 0:
    return "White won"

  #continue playing or draw
  for i in range(8):
    for j in range(8):
      if board[i][j] == " ":
        return "Continue playing"

  return "Draw"



def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


#tests
def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded(board, y_end, x_end, length, d_y, d_x):


    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 3; y = 2; d_x = 1; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")

    print_board(board)
    if detect_row(board, "b", 0,1,4,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
  board = make_empty_board(8)

  x = 3; y = 5; d_x = 1; d_y = -1; length = 3; col = 'b'
  #put_seq_on_board(board, y, x, d_y, d_x, length, "b")

  put_seq_on_board(board, x, y, d_y, d_x, length, "b")


  print_board(board)
  if detect_rows(board, col,length) == (0,1):
    print("TEST CASE for detect_rows PASSED")
  else:
    print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':


  #print(play_gomoku(8))
  board = [['w', 'b', 'w', ' ', 'w', ' ', ' ', ' '], [' ', 'b', ' ', 'w', ' ', ' ', ' ', ' '], [' ', 'b', 'b', 'w', 'w', ' ', 'w', 'w'], ['w', 'b', 'w', 'b', 'b', 'b', ' ', ' '], [' ', 'w', 'b', 'b', 'b', 'b', 'w', ' '], ['b', 'w', 'b', 'w', 'b', 'b', 'w', 'w'], ['b', 'b', 'b', ' ', 'b', 'b', 'w', 'w'], ['b', ' ', ' ', 'b', 'b', 'w', ' ', ' ']]



  print_board(board)
