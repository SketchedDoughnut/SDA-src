## classes
class GenerateBoard:
    # init
    def __init__(self, width: int, height: int) -> None:
        board = []
        n_list = []
        self.width = width
        self.height = height
        for x in range(width): # x for visualization
            for y in range(height): # y for visualization
                n_list.append(False)
            board.append(n_list)
            n_list = []
        self.board = board

    # handler for generating a new board
    def gen_new_board(self):
        board = self.get_current_board()
        n_list = []
        new_board = []
        for x in range(len(board)):
            for y in range(self.width):
                origin = (x, y)
                current_state = self.get_current_state(origin)
                bases = self.get_bases(origin)[0]
                perimeter = self.get_permimeter(origin, bases)
                population = self.get_states(board, perimeter)
                n_state = self.rules_eval(current_state, population)
                n_list.append(n_state)
            new_board.append(n_list)
            n_list = []
        self.board = new_board
        return new_board
        

    # gets active board
    def get_current_board(self) -> list:
        return self.board
    

    # gets current state
    def get_current_state(self, origin: tuple) -> bool:
        board = self.get_current_board()
        return board[origin[0]][origin[1]]


    # gets the bases (left, right, up, down of coordinate inputed)
    def get_bases(self, origin: tuple) -> tuple:

        # get current x, y
        current_x = origin[0]
        current_y = origin[1]

        # set origin to fixed values
        origin = (current_x, current_y)

        min_x = current_x - 1
        max_x = current_x + 1

        min_y = current_y - 1
        max_y = current_y + 1

        # return data
        return ((min_x, max_x), (min_y, max_y)), origin


    # gets all 8 perimeter points around origin (filters out origin overlaps)
    def get_permimeter(self, origin: tuple, bases: tuple) -> list:
        ## the only reason why there is so much out here and not compacted is to make it easier to understand, I do not believe it causes it to act any slower

        # set up parameters
        min_x = bases[0][0]
        max_x = bases[0][1]
        min_y = bases[1][0]
        max_y = bases[1][1]
        Ox = origin[0]
        Oy = origin[1]
        
        # get bases
        b1 = (min_x, Oy)
        b2 = (Ox, min_y)
        b3 = (max_x, Oy)
        b4 = (Ox, max_y)

        # get corners
        c1 = (min_x, min_y)
        c2 = (max_x, min_y)
        c3 = (max_x, max_y)
        c4 = (min_x, max_y)

        # prints not used
        # print('c1:',c1)
        # print('c2:',c2)
        # print('c3:',c3)
        # print('c4:',c4)
        # print('b1:',b1)
        # print('b2:',b2)
        # print('b3:',b3)
        # print('b4:',b4)

        # append everything
        n_list = []
        n_list.append(c1)
        n_list.append(c2)
        n_list.append(c3)
        n_list.append(c4)
        n_list.append(b1)
        n_list.append(b2)
        n_list.append(b3)
        n_list.append(b4)

        # origin filtering
        while origin in n_list:
            n_list.remove(origin)
        return n_list


    # get states of all in perimeter, returns those states and population
    def get_states(self, board: list, perimeter: tuple) -> list:
        n_list = []
        for coord in perimeter:
            x = coord[0]
            y = coord[1]
            if x >= 0 and y >= 0:
                if x < self.width and y < self.height:
                    n_list.append(board[x][y])
                else:
                    n_list.append(False)
            else:
                n_list.append(False)
        population = n_list.count(True)
        return population


    # compares against rules, returns what the state of the current square should be
    def rules_eval(self, current_state: bool, population: int) -> bool:
        alive = population
        fate = None
        # print('ALIVE COUNT:', alive)
        if current_state and alive < 2:
            fate = False
        elif current_state and alive == 2 or alive == 3:
            fate = True
        elif current_state and alive > 3:
            fate = False
        elif not current_state and alive == 3:
        # for high life (modified): https://youtu.be/rgAsqP6xdWk?t=569
        #elif not current_state and alive == 3 or alive == 5 or alive == 6:
            fate = True
        return fate
    

    # smol feature functions
    def set_state(self, origin: tuple) -> None:
        #board = self.get_current_board()
        board = self.board
        board[origin[0]][origin[1]] = not board[origin[0]][origin[1]]

    def set_board(self, board: list) -> None:
        self.board = board

    def get_state(self, origin: tuple) -> bool:
        return self.board[origin[0]][origin[1]]