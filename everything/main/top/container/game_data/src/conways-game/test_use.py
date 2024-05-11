# import eval

# ################## SETUP ##################
# ## showing how to use it (I prefer no tampering with the stuff I built, I didn't tamper with yours but did just fix an issue where you imported the wrong thing)
# ## this testcase will use the point: (5, 5)
# origin = (5, 5)

# # when initially setting up, give it width height data (should be a square but handles rectangles too)
# generateBoard = eval.GenerateBoard(int(input('Enter a width: ')), int(input('Enter a height: ')))

# ################## OPERATION ##################
# # does all handling for generating new board, returns new board as well as alive / dead
# current_board = generateBoard.get_current_board()
# new_board = generateBoard.gen_new_board()

# # print(current_board)
# # print('-------------')
# # print(new_board)
# print('-------------')
# print('current:', len(current_board))
# print('-------------')
# print('-', current_board[0])
# print('-------------')
# print('new:', len(new_board))
# print('-------------')
# print('-', new_board[0])

# exit()

# for i in range(1):
#     current_board = generateBoard.get_current_board()
#     new_board = generateBoard.gen_new_board()
    
#     # print('-------------')
#     # print('state:', generateBoard.get_current_state(origin))
#     print('-------------')

#     c = 0
#     for collumn in current_board:
#         c += collumn.count(True)
#     print('total true count before:', c)

#     c = 0
#     for collumn in new_board:
#         c += collumn.count(True)
#     print('total true count after:', c)
# print('-------------')

import start_screen
import pygame
window = pygame.display.set_mode((1920, 1080))
start_screen.StartScreen(window)