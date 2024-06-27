import conway_crash_handler
try:
    import pygame
    import rendering
    import time
    import threading
    import tkinter # window stuff

    # my files
    import eval
    import loads
    import start_screen





    def pho_run(window: pygame.Surface, text: str, text_rect: pygame.Rect) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if can_exit:
                        print('window quit')
                        global running
                        running = False
                    else:
                        print('cannot exit: a task is running')
            window.blit(text, text_rect)
            pygame.display.update()




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
    can_exit = True

    SS = start_screen.StartScreen(WINDOW)
    while running:

        SCREENWIDTH = pygame.display.Info().current_w

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if can_exit:
                    print('window quit')
                    running = False
                else:
                    print('cannot exit: a task is running')
            
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
                # ik its diff let me have this
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL] and keys[pygame.K_c] or keys[pygame.K_LCTRL] and keys[pygame.K_w]:
                    if can_exit:
                        print('ctrl + c / ctrl + w')
                        running = False
                    else:
                        print('cannot exit: a task is running')
                elif keys[pygame.K_e]:
                    print('outputting file...')
                    try:
                        can_exit = False
                        c = conway_crash_handler.Crash_handler(None, None, 'setup')
                        now_time = c.get_time()
                        import os
                        log_wDir = os.path.abspath(__file__)
                        path = c.path_tools.convert_path(log_wDir, '/')
                        path = path.removesuffix('/main.py')

                        #print('before mk:', path)
                        create_path = path + '/maps_out'
                        try:
                            os.mkdir(create_path)
                        except:
                            pass
                        #print('after mk:', path)
                        path = c.path_tools.convert_path(path, '/')
                        #print('conv back:', path)
                        f = open(f'{path}/maps_out/map_{now_time}.json', 'w')
                        import json
                        json.dump(board_gen.get_current_board(), f)
                        f.close()
                        # print(f'logged map to: {path}/maps_out/map_{now_time}.json') # replaced with tkinter window

                        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
                        # goal_width = 1250
                        # goal_height = 500
                        # scaled_width = goal_width / 1920 * screen_width
                        # scaled_height = goal_height / 1080 * screen_height
                        # scaled_width = round(scaled_width)
                        # scaled_height = round(scaled_height)
                        window = tkinter.Tk(className="window~!")
                        # window.geometry(f"{scaled_width}x{scaled_height}")
                        string_var = tkinter.StringVar()
                        string_var.set(f'logged map to: {path}/maps_out/map_{now_time}.json')
                        text = tkinter.Label(window, pady=25, textvariable=string_var)
                        text.pack()
                        button = tkinter.Button(window, width=25, text="close this window", command=window.destroy, pady=5)
                        button.pack()
                        window.mainloop()

                        can_exit = True
                    except Exception as e:
                        print('output map error:', e)
                        raise 'outputMapError'
                    
                elif keys[pygame.K_i]:
                    # if start_menu == True:
                    m1 = loads.Map_loader()
                    # map_path = loads.load_map()
                    try:
                        m1.load_map()
                        map_path = m1.map_path
                        # print('----------------------')
                        # print('Restarting window...')
                        # pygame.init()
                        # WINDOW = pygame.display.set_mode((600,400), pygame.RESIZABLE)
                        # pygame.display.set_caption('Conways Game Of Life')
                        # # create loading text
                        # f_size = round(36) # size is normally 36 in other projects
                        # font = pygame.font.Font('freesansbold.ttf', f_size)
                        # msg = 'Loading map...'
                        # msg = font.render(msg, True, (255, 255, 255), None)  # text, some bool(?), text color, bg color
                        # rect = msg.get_rect()
                        # rect.center = (pygame.display.get_window_size()[0] / 2, pygame.display.get_window_size()[1] / 2)
                        # # pho_thread = threading.Thread(target=lambda:pho_run(WINDOW, msg, rect))
                        # # pho_thread.start()
                        # WINDOW.blit(msg, rect)
                        # pygame.display.update()
                        # print('Loading map, start screen...')
                        if m1.map_name:
                            board_gen = eval.GenerateBoard(width, height, load_map = map_path)
                            SS = start_screen.StartScreen(WINDOW)
                            print('Loading done')
                            #pho_thread.join()
                            print('----------------------')
                        else:
                            print('loading failed: invalid path')
                            print('----------------------')
                    except:
                        print('loading failed: invalid path')
                        print('----------------------')


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
                    #start_menu = True
                    start_menu = not start_menu
                
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
            start_menu, board_gen = SS.draw(board_gen)
        if tickTimer > 1 / generationTickRate:
            if paused == False:
                current_board = new_board
        pygame.display.update()
    pygame.quit()

except Exception as e:
  import os
  import traceback
  conway_crash_handler.Crash_handler(
      error = traceback.format_exc()
  )