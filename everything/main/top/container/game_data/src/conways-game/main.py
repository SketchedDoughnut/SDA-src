########################################################################
class Crash_Handler:
    def __init__(self, wDir, error):
        print('------------------')
        print('Crash Handler setting up...')
        con = self.convert_path(wDir, '/')
        con = self.split_path(con)
        con = self.assemble_path(con)
        con = self.promote_path(con)
        print('Path formatted...')
        dumps_path = self.assemble_dir(con)
        print('Directory assembled...')
        con = self.get_data(dumps_path)
        self.dump_data(con, error)
        print('Data acquired, dumped...')
        print('------------------')
        print('Crash documented to:', f'{con}')
        print('------------------')
        input('Enter anything to exit: ')
        exit()

    def convert_path(self, path, mode):
        n_string = ''
        for letter in path:
            if mode == '/':
                if letter == '\\':
                    n_string += '/'
                else:
                    n_string += letter
            elif mode == '\\':
                if letter == '/':
                    n_string += '\\'
                else:
                    n_string += letter
        return n_string
    
    def split_path(self, path):
        n_string = ''
        n_list = []
        for letter in path:
            if letter == '/':
                n_list.append(n_string)
                n_string = ''
            else:
                n_string += letter
        while n_list[0] == " ":
            n_list.pop(0)
        return n_list
    
    def assemble_path(self, path_list):
        n_string = ''
        for word in path_list:
            n_string += word
            n_string += '/'
        return n_string
    
    def remove_n_path_index(self, path):
        path_list = self.split_path(path)
        path_list.pop(len(path_list) - 1)
        path = self.assemble_path(path_list)
        return path_list, path
    
    def promote_path(self, path):
        while True:
            path_list, path = self.remove_n_path_index(path)
            if path_list[len(path_list) - 1] == 'everything':
                break
        return path

    def assemble_dir(self, path):
        path += 'crash/dumps'
        return path
    
    def format_time(self):
        import time
        s = (time.ctime(time.time()))
        s = s.replace(':', '-')
        s = s.split()
        for __ in range(2):
            s.pop(0)
        n_string = ''
        for num in s:
            n_string += num
            if s.index(num) != len(s) -1:
                n_string += '_'
        return n_string

    def get_data(self, dumps_dir):
        import os
        import json
        time_val = self.format_time()
        nc_log = os.path.join(dumps_dir, f'crash_log_{time_val}.log')
        nc_log = self.convert_path(nc_log, '\\')
        return nc_log

    def dump_data(self, path, error):
        #import json
        f = open(path, 'w')
        #json.dump(error, f)
        f.write(error)
        f.close()
########################################################################

try:
    import pygame
    import rendering
    import time

    # my files
    import eval

    pygame.init()
    WINDOW = pygame.display.set_mode((600,400), pygame.RESIZABLE)
    pygame.display.set_caption('Conways Game Of Life')
    renderer = rendering.BoardRenderer()

    renderer.cellSize = 50
    renderer.borderSize = 3
    renderer.FPS = 30
    renderer.onColor = (97, 26, 122) # not final colors
    renderer.offColor = (36, 25, 42)
    renderer.backgroundColor = (8,0,12)

    # my additions
    width = 100
    height = 100
    board_gen = eval.GenerateBoard(width, height)
    generationTickRate = 5
    lastTime = time.perf_counter()
    tickTimer = 0


    renderer.camera.x = board_gen.width / 2 * renderer.cellSize
    renderer.camera.y = board_gen.height / 2 * renderer.cellSize

    leftMouseButtonDown = False
    rightMouseButtonDown = False
    paintMode = True
    panning = False
    lastMousePosition = (0,0)

    # pausing 
    paused = True
    start_menu = True
    space_pressed = False
    running = True

    import start_screen
    SS = start_screen.StartScreen(WINDOW)
    while running:

        SCREENWIDTH = pygame.display.Info().current_w

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('window quit')
                running = False
            
            elif event.type == pygame.WINDOWRESIZED:
                SS = start_screen.StartScreen(WINDOW)
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # originally elif
                if not panning:
                    clickedCellLocation = renderer.camera.screenToWorldPoint(event.pos)
                    clickedCellLocation = (round(clickedCellLocation[1] / renderer.cellSize),round(clickedCellLocation[0] / renderer.cellSize))
                    if clickedCellLocation[0] < board_gen.width and clickedCellLocation[0] >= 0 and clickedCellLocation[1] < board_gen.width and clickedCellLocation[1] >= 0:
                        board_gen.set_state(clickedCellLocation)
                leftMouseButtonDown = False
                panning = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                leftMouseButtonDown = True
                lastMousePosition = (event.pos[0],event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                rightMouseButtonDown = True
                clickedCellLocation = renderer.camera.screenToWorldPoint(event.pos)
                clickedCellLocation = (round(clickedCellLocation[1] / renderer.cellSize),round(clickedCellLocation[0] / renderer.cellSize))
                paintMode = not board_gen.get_state(clickedCellLocation)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                rightMouseButtonDown = False

            elif event.type == pygame.MOUSEMOTION:
                if leftMouseButtonDown:
                    panning = True
                    widthScale = pygame.display.get_window_size()[0] / SCREENWIDTH
                    worldStart = renderer.camera.screenToWorldPoint(lastMousePosition)
                    worldChange = renderer.camera.screenToWorldPoint((event.pos[0],event.pos[1]))
                    worldChange = ((worldChange[0] - worldStart[0]) / widthScale, (worldChange[1] - worldStart[1]) / widthScale)
                    renderer.camera.x -= worldChange[0] * widthScale
                    renderer.camera.y -= worldChange[1] * widthScale
                    lastMousePosition = event.pos
                elif rightMouseButtonDown:
                    clickedCellLocation = renderer.camera.screenToWorldPoint(event.pos)
                    clickedCellLocation = (round(clickedCellLocation[1] / renderer.cellSize),round(clickedCellLocation[0] / renderer.cellSize))
                    if clickedCellLocation[0] < board_gen.width and clickedCellLocation[0] > 0 and clickedCellLocation[1] < board_gen.width and clickedCellLocation[1] > 0:
                        board_gen.board[clickedCellLocation[0]][clickedCellLocation[1]] = paintMode

            elif event.type == pygame.MOUSEWHEEL:
                renderer.camera.z = renderer.camera.z * (0.9 ** event.y)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if start_menu == True:
                        start_menu = False
                    else:
                        paused = not paused
                        print('space:', paused, '->', not paused)
                elif event.key == pygame.K_r:
                    board_gen = eval.GenerateBoard(width, height)
                    paused = True
                elif event.key == pygame.K_ESCAPE:
                    print('menu invoked')
                    paused = True
                    start_menu = True
                
        deltaTime = time.perf_counter() - lastTime
        lastTime = time.perf_counter()
        tickTimer += deltaTime
        current_board = board_gen.get_current_board()
        if tickTimer > 1 / generationTickRate:
            tickTimer = 0
            if paused == False:
                new_board = board_gen.gen_new_board()
        renderer.tick(WINDOW, current_board)
        if start_menu == True:
            start_menu = SS.draw()
        if tickTimer > 1 / generationTickRate:
            if paused == False:
                current_board = new_board
        pygame.display.update()
    pygame.quit()

except Exception as e:
  import os
  import traceback
  Crash_Handler(
      wDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
      error = traceback.format_exc()
  )