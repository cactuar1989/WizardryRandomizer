from map_maker import make_map
from colorama import init
from colorama import Fore, Back, Style

# Initialize colorama
init()


WALL = '#'
CELL = ' '
ROOM = 'R'
DOOR = '|'
PATH = '.'


## Functions
def printMaze(maze):
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if (maze[i][j] == 'u'):
                print(Fore.RED + str(maze[i][j]), end="   ")
            elif (maze[i][j] == CELL):
                print(Fore.WHITE + str(maze[i][j]), end="   ")
            elif (maze[i][j] == DOOR or maze[i][j] == ROOM):
                print(Fore.GREEN + str(maze[i][j]), end="   ")
            elif (maze[i][j] == PATH):
                print(Fore.MAGENTA + str(maze[i][j]), end="   ")
            else:
                print(Fore.BLUE + str(maze[i][j]), end="   ")          
        print('\n')

maze, hex_date = make_map(20, 20, paths=[
    # {'start':(0,0), 'end':(0,10)},
    # {'start':(0,0), 'end':(13,3)},
    {'start':(0,0), 'end':(0,10)}])
printMaze(maze)