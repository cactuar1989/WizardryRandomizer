## Imports
import random
import time


WALL = '#'
CELL = ' '
ROOM = 'R'
DOOR = '|'
PATH = '.'

ROOM_NUM_MIN = 20
ROOM_NUM_MAX = 25
ROOM_SIZE_MIN = 1
ROOM_SIZE_MAX = 3
DOOR_CHANCE = 85
PATH_TURN_CHANCE = 15


def make_map(h, w, paths):
    # Find number of surrounding cells
    def surroundingCells(rand_wall):
        s_cells = 0
        if (maze[rand_wall[0]-1][rand_wall[1]] == CELL):
            s_cells += 1
        if (maze[rand_wall[0]+1][rand_wall[1]] == CELL):
            s_cells += 1
        if (maze[rand_wall[0]][rand_wall[1]-1] == CELL):
            s_cells +=1
        if (maze[rand_wall[0]][rand_wall[1]+1] == CELL):
            s_cells += 1
        return s_cells

    ## Main code
    # Init variables
    # wall = 'w'
    # cell = 'c'
    # room = 'r'
    unvisited = 'u'
    height = h + 2
    width = w + 2
    maze = []


    # Denote all cells as unvisited
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    # Randomize starting point and set it a cell
    starting_height = int(random.random()*height)
    starting_width = int(random.random()*width)
    if (starting_height == 0):
        starting_height += 1
    if (starting_height == height-1):
        starting_height -= 1
    if (starting_width == 0):
        starting_width += 1
    if (starting_width == width-1):
        starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    maze[starting_height][starting_width] = CELL
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    maze[starting_height-1][starting_width] = WALL
    maze[starting_height][starting_width - 1] = WALL
    maze[starting_height][starting_width + 1] = WALL
    maze[starting_height + 1][starting_width] = WALL

    while (walls):
        # Pick a random wall
        rand_wall = walls[int(random.random()*len(walls))-1]

        # Check if it is a left wall
        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1]-1] == 'u' and maze[rand_wall[0]][rand_wall[1]+1] == CELL):
                # Find the number of surrounding cells
                s_cells = surroundingCells(rand_wall)

                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = CELL

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]-1][rand_wall[1]] = WALL
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])


                    # Bottom cell
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]+1][rand_wall[1]] = WALL
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0): 
                        if (maze[rand_wall[0]][rand_wall[1]-1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]-1] = WALL
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)
                continue

        # Check if it is an upper wall
        if (rand_wall[0] != 0):
            if (maze[rand_wall[0]-1][rand_wall[1]] == 'u' and maze[rand_wall[0]+1][rand_wall[1]] == CELL):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = CELL

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]-1][rand_wall[1]] = WALL
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]-1] = WALL
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])

                    # Rightmost cell
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]+1] = WALL
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)
                continue

        # Check the bottom wall
        if (rand_wall[0] != height-1):
            if (maze[rand_wall[0]+1][rand_wall[1]] == 'u' and maze[rand_wall[0]-1][rand_wall[1]] == CELL):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = CELL

                    # Mark the new walls
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]+1][rand_wall[1]] = WALL
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]-1] = WALL
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]+1] = WALL
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)
                continue

        # Check the right wall
        if (rand_wall[1] != width-1):
            if (maze[rand_wall[0]][rand_wall[1]+1] == 'u' and maze[rand_wall[0]][rand_wall[1]-1] == CELL):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = CELL

                    # Mark the new walls
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]+1] = WALL
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]+1][rand_wall[1]] = WALL
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[0] != 0): 
                        if (maze[rand_wall[0]-1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]-1][rand_wall[1]] = WALL
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)
                continue

        # Delete the wall from the list anyway
        for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                walls.remove(wall)        


    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == 'u'):
                maze[i][j] = WALL

    # # Set entrance and exit
    # for i in range(0, width):
    #     if (maze[1][i] == CELL):
    #         maze[0][i] = CELL
    #         break

    # for i in range(width-1, 0, -1):
    #     if (maze[height-2][i] == CELL):
    #         maze[height-1][i] = CELL
    #         break


    # create path from start to end
    for path in paths:
        path_done = False
        path_col, path_row = path['start']
        path_row = height - 2 - path_row
        path_col += 1
        while path_done == False:
        # for x in range(10):
            end_col, end_row = path['end']
            end_row = height - 2 - end_row
            end_col += 1
            final_row, final_col = end_row, end_col
            if path_row - end_row > 0:
                # we need to go N
                row_dir = 1
            else:
                row_dir = -1
            if path_col - end_col > 0:
                # we need to go W
                col_dir = 1
            else:
                col_dir = -1
            # check if end point is close enough to draw path straight to it
            if (abs(path_row - end_row) > 5) or (abs(path_col - end_col) > 5):
                # print('picking intermediate point')
                # chance to go wrong direction
                if random.randint(1, 100) < PATH_TURN_CHANCE:
                    row_dir = row_dir * -1
                if random.randint(1, 100) < PATH_TURN_CHANCE:
                    col_dir = col_dir * - 1
                end_row = path_row - (random.randint(1, 5) * row_dir)
                if end_row < 1:
                    end_row = 1
                elif end_row > h:
                    end_row = h
                end_col = path_col - (random.randint(1, 5) * col_dir)
                if end_col < 1:
                    end_col = 1
                elif end_col > w:
                    end_col = w
            for i in range(abs(path_row - end_row) + 1):
                # print(f'path_row={path_row} | end_row={end_row}')
                maze[path_row][path_col] = CELL
                for j in range(abs(path_col - end_col) + 1):
                    # check if final row we will iterate
                    if path_row == end_row:
                        maze[path_row][path_col - (j * col_dir)] = CELL
                    # check if we are done
                    if (path_row == final_row) and ((path_col - (j * col_dir)) == final_col):
                        # maze[path_row][path_col - (j * col_dir)] = '!'
                        path_done = True
                path_row -= (1 * row_dir)
            path_col = end_col # done iterating columns
            path_row = end_row


    # pick a random starting point for a room
    room_num = random.randint(ROOM_NUM_MIN, ROOM_NUM_MAX) # number of rooms to create
    for x in range(room_num):
        room_h = random.randint(ROOM_SIZE_MIN, ROOM_SIZE_MAX) # room height
        room_w = random.randint(ROOM_SIZE_MIN, ROOM_SIZE_MAX) # room height
        room_x = random.randint(1, w) # starting room x
        room_y = random.randint(1, h) # starting room y
        for i in range(room_h):
            for j in range(room_w):
                if room_y + i < height-1 and room_x + j < width-1 and room_y + i > 0 and room_x + j > 0:
                    x = random.randint(0, 100)
                    if x < DOOR_CHANCE:
                        cell_fill = DOOR
                    else:
                        cell_fill = ROOM
                    maze[room_y + i][room_x + j] = cell_fill


    # convert maze to usable code for wizardry
    hex_maze = []
    for i in range(height - 1):
        hex_row = []
        for j in range(width - 1):
            if i > 0 and i < height - 1 and j > 0 and j < width - 1:
                current_cell = maze[i][j]
                left_bit = 0
                right_bit = 0
                # Tile Codes
                # left bit for S and W, right bit for N and E
                # +1 for N/S wall, +2 for N/S door, +4 for E/W wall, +8 for E/W door
                if current_cell == CELL:
                    # check down and build walls
                    if maze[i+1][j] in [WALL, ROOM]:
                        # if current_cell is floor and next to a wall or current cell is wall and next to a floor
                        left_bit += 1
                    # check left
                    if maze[i][j-1] in [WALL, ROOM]:
                        left_bit += 4
                    # check up
                    if maze[i-1][j] in [WALL, ROOM]:
                        right_bit += 1
                    # check right
                    if maze[i][j+1] in [WALL, ROOM]:
                        right_bit += 4
                    # check down and build doors
                    if maze[i+1][j] in [DOOR, PATH]:
                        left_bit += 2
                    # check left
                    if maze[i][j-1] in [DOOR, PATH]:
                        left_bit += 8
                    # check up
                    if maze[i-1][j] in [DOOR, PATH]:
                        right_bit += 2
                    # check right
                    if maze[i][j+1] in [DOOR, PATH]:
                        right_bit += 8

                if current_cell == PATH:
                    # check down and build walls
                    if maze[i+1][j] in [WALL, ROOM]:
                        # if current_cell is floor and next to a wall or current cell is wall and next to a floor
                        left_bit += 1
                    # check left
                    if maze[i][j-1] in [WALL, ROOM]:
                        left_bit += 4
                    # check up
                    if maze[i-1][j] in [WALL, ROOM]:
                        right_bit += 1
                    # check right
                    if maze[i][j+1] in [WALL, ROOM]:
                        right_bit += 4
                    # check down and build doors
                    if maze[i+1][j] in [DOOR, CELL]:
                        left_bit += 2
                    # check left
                    if maze[i][j-1] in [DOOR, CELL]:
                        left_bit += 8
                    # check up
                    if maze[i-1][j] in [DOOR, CELL]:
                        right_bit += 2
                    # check right
                    if maze[i][j+1] in [DOOR, CELL]:
                        right_bit += 8


                if current_cell == WALL:
                    # check down
                    if maze[i+1][j] in [CELL, ROOM, PATH]:
                        # if current_cell is floor and next to a wall or current cell is wall and next to a floor
                        left_bit += 1
                    # check left
                    if maze[i][j-1] in [CELL, ROOM, PATH]:
                        left_bit += 4
                    # check up
                    if maze[i-1][j] in [CELL, ROOM, PATH]:
                        right_bit += 1
                    # check right
                    if maze[i][j+1] in [CELL, ROOM, PATH]:
                        right_bit += 4
                    # check if next to a room to add door
                    # check down
                    if maze[i+1][j] in [DOOR]:
                        left_bit += 2
                    # check left
                    if maze[i][j-1] in [DOOR]:
                        left_bit += 8
                    # check up
                    if maze[i-1][j] in [DOOR]:
                        right_bit += 2
                    # check right
                    if maze[i][j+1] in [DOOR]:
                        right_bit += 8

                if current_cell == ROOM:
                    # check down
                    if maze[i+1][j] in [WALL, CELL, PATH]:
                        left_bit += 1
                    # check left
                    if maze[i][j-1] in [WALL, CELL, PATH]:
                        left_bit += 4
                    # check up
                    if maze[i-1][j] in [WALL, CELL, PATH]:
                        right_bit += 1
                    # check right
                    if maze[i][j+1] in [WALL, CELL, PATH]:
                        right_bit += 4
                    # # check down
                    # if maze[i+1][j] in ['r']:
                    #     left_bit += 2
                    # # check left
                    # if maze[i][j-1] in ['r']:
                    #     left_bit += 8
                    # # check up
                    # if maze[i-1][j] in ['r']:
                    #     right_bit += 2
                    # # check right
                    # if maze[i][j+1] in ['r']:
                    #     right_bit += 8

                if current_cell == DOOR:
                    # # check down (walls)
                    # if maze[i+1][j] in ['w']:
                    #     left_bit += 1
                    # # check left
                    # if maze[i][j-1] in ['w']:
                    #     left_bit += 4
                    # # check up
                    # if maze[i-1][j] in ['w']:
                    #     right_bit += 1
                    # # check right
                    # if maze[i][j+1] in ['w']:
                    #     right_bit += 4
                    # check down (hallways)
                    if maze[i+1][j] in [WALL, CELL, PATH]:
                        left_bit += 2
                    # check left
                    if maze[i][j-1] in [WALL, CELL, PATH]:
                        left_bit += 8
                    # check up
                    if maze[i-1][j] in [WALL, CELL, PATH]:
                        right_bit += 2
                    # check right
                    if maze[i][j+1] in [WALL, CELL, PATH]:
                        right_bit += 8
                # convert to hex
                val = hex(left_bit)[2:] + hex(right_bit)[2:] # leave off the 0x
                hex_row.append(val)
        if len(hex_row) != 0:
            hex_maze.append(hex_row)
    hex_maze.reverse()

    hex_maze = [item for sublist in hex_maze for item in sublist] # flatten array
    hex_data = "".join(map(str, hex_maze))
    return maze, hex_data