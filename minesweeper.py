import random as rnd
import msvcrt as key
import time
import datetime
import os
colors = {"black":"\033[38;5;0m",
          "red":"\033[38;5;1m",
          "green":"\033[38;5;2m",
          "orange":"\033[38;5;202m",
          "blue":"\033[38;5;4m",
          "purple":"\033[38;5;5m",
          "cyan":"\033[38;5;6m",
          "silver":"\033[38;5;7m",
          "grey":"\033[38;5;8m",
          "brightred":"\033[38;5;9m",
          "brightgreen":"\033[38;5;10m",
          "brightyellow":"\033[38;5;11m",
          "brightblue":"\033[38;5;12m",
          "pink":"\033[38;5;13m",
          "brightcyan":"\033[38;5;14m",
          "white":"\033[38;5;15m"}
colors2 = {0:colors["white"],
           1:colors["brightblue"],
           2:colors["green"],
           3:colors["brightred"],
           4:colors["blue"],
           5:colors["red"],
           6:colors["cyan"],
           7:colors["purple"],
           8:colors["silver"],
           'X':colors["black"]}
os.system('color 70')
print('\033[?25l\033[48;5;7m',end='')
while True:
    print('WASD to move cursor, Spacebar to uncover, Q to mark as bomb')
    print('Select difficulty')
    print('1 for 7x7 with 6 mines')
    print('2 for 9x9 with 10 mines')
    print('3 for 16x16 with 40 mines')
    print('4 for 30x16 with 100 mines')
    print('5 for 40x25 with 200 mines')
    difficulty = int(input())
    match difficulty:
        case 1:
            width = 7
            height = 7
            minecount = 6
        case 2:
            width = 9
            height = 9
            minecount = 10
        case 3:
            width = 16
            height = 16
            minecount = 40
        case 4:
            width = 30
            height = 16
            minecount = 100
        case 5:
            width = 40
            height = 20
            minecount = 200
    setup = True
    gameover = 0
    uncovered = 0
    time1 = time.time()
    field = []
    visfield = []
    for a in range(height):
        c = []
        for b in range(width):
            c += [0]
        field += [c]
    for a in range(height):
        c = []
        for b in range(width):
            c += str('#')
        visfield += [c]
    selx = round(width/2)-1
    sely = round(height/2)-1
    os.system('cls')
    while gameover == 0:
        if uncovered >= width*height-minecount:
            gameover = 2
        button = []
        while key.kbhit():
            try:
                button += [key.getch().decode("ASCII").lower()]
            except:
                pass
        for a in button:
            match a:
                case 'a':
                    selx -= 1
                case 'd':
                    selx += 1
                case 'w':
                    sely += 1
                case 's':
                    sely -= 1
                case ' ' if  visfield[sely][selx] == '#':
                    visfield[sely][selx] = ' '
                    uncovered += 1
                    #Setup mines
                    if setup == True:
                        for b in range(sely-1,sely+2,1):
                            for c in range(selx-1,selx+2,1):
                                if b < height and b > -1 and c < width and c > -1 and visfield[b][c] == '#':
                                    visfield[b][c] = ' '
                                    uncovered += 1
                        mines = 0
                        while mines < minecount:
                            b = rnd.randint(0,height-1)
                            c = rnd.randint(0,width-1)
                            if visfield[b][c] != ' ' and field[b][c] != 'X':
                                field[b][c] = 'X'
                                for d in range(b-1,b+2,1):
                                    for e in range(c-1,c+2,1):
                                        if d < height and d > -1 and e < width and e > -1 and type(field[d][e]) == int:
                                            field[d][e] += 1
                            mines = 0
                            for b in range(height):
                                for c in range(width):
                                    if field[b][c] == 'X':
                                        mines += 1
                        setup = False
                    elif field[sely][selx] == 'X':
                        gameover = 1
                    while True:
                        loop = False
                        for b in range(height):
                            for c in range(width):
                                if field[b][c] == 0 and visfield[b][c] == ' ':
                                    for d in range(b-1,b+2,1):
                                        for e in range(c-1,c+2,1):
                                            if d < height and d > -1 and e < width and e > -1 and visfield[d][e] == '#':
                                                visfield[d][e] = ' '
                                                uncovered += 1
                                                loop = True
                        if loop == False:
                            break
                case 'q' if setup == False:
                    if visfield[sely][selx] == '#':
                        visfield[sely][selx] = '+'
                    elif visfield[sely][selx] == '+':
                        visfield[sely][selx] = '#'
        selx = selx%width
        sely = sely%height
        time2 = datetime.timedelta(seconds=(round(time.time()-time1)))
        #Grid draw
        print('\033[5;0H',end='')
        print(f'\033[30CDimensions are {width}x{height}, {minecount} mines, Time:{time2}')
        print('\033[30C+',end='')
        for a in range(width*2-1):
            print('-',end='')
        print('+')
        for a in range(height-1,-1,-1):
            print('\033[30C|',end='')
            for b in range(width):
                if a == sely and b == selx:
                    print('\033[48;5;10m',end='')
                if visfield[a][b] == ' ':
                    print(colors2[field[a][b]],end='')
                    print(field[a][b],end='')
                else:
                    if visfield[a][b] == '+':
                        print(colors["black"],end='')
                    print(visfield[a][b],end='')
                print('\033[48;5;7m\033[38;5;8m',end=' ')
            print('\033[D|')
        print('\033[30C+',end='')
        for a in range(width*2-1):
            print('-',end='')
        print('+')
    #Draw postmortem
    print('\033[5;0H',end='')
    print(f'\033[30CDimensions are {width}x{height}, {minecount} mines, Time:{time2}')
    print('\033[30C+',end='')
    for a in range(width*2-1):
        print('-',end='')
    print('+')
    for a in range(height-1,-1,-1):
        print('\033[30C|',end='')
        for b in range(width):
            print(colors2[field[a][b]],end='')
            print(field[a][b],end='')
            print('\033[38;5;8m',end=' ')
        print('\033[D|')
    print('\033[30C+',end='')
    for a in range(width*2-1):
        print('-',end='')
    print('+')
    if gameover == 1:
        input('\033[30C You lost! Enter anything to reset')
    if gameover == 2:
        input('\033[30C You win! Enter anything to reset')
    os.system('cls')
