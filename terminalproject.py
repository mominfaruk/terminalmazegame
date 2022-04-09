import curses
from curses import wrapper
import imp
import queue 
import time
import random

print("1: " ,"Want to Generate a random maze?")
print("2: " ,"Want to generate a maze using a maze?")
choice=int(input("Enter your choice: "))
if choice==1:
    totalrow=random.randint(3,15)
    totalcol=random.randint(3,15)
else:
    totalrow=int(input("Enter the number of rows: "))
    totalcol=int(input("Enter the number of columns: "))
if totalcol<1 or totalrow<1:
    print("Can't be smmaller than 1")
    exit

maze=[[random.choice(['#',' ',' ',' ']) for i in range(totalcol)] for j in range(totalrow)]
in_start=[random.randint(1,totalrow-1),random.randint(1,totalcol-1)]
end=[random.randint(1,totalrow-1),random.randint(1,totalcol-1)]
maze[in_start[0]][in_start[1]]="O"
maze[end[0]][end[1]]="X"

def print_maze(maze,stdscr,path=[]):
    blue=curses.color_pair(1)
    red=curses.color_pair(2)

    for index,row in enumerate(maze):
        for jndex,value in enumerate(row):
            if (index,jndex) in path:
                if maze[index][jndex]=='O':
                    stdscr.addstr(index,jndex*2,"O",red)
                else:
                    stdscr.addstr(index,jndex*2,"X",red)
            else:
                stdscr.addstr(index,jndex*2,value,blue)
def find_start(maze,start):
    for index,row in enumerate(maze):
        for jndex,col in enumerate(row):
            if col=='O':
                return index,jndex
    return None

visited=set()
def find_path(maze,stdscr):
    start="O"
    end="X"
    start_pos=find_start(maze,start)
    if start_pos==None:
        return "NO START"
    
    q=queue.Queue()
    q.put((start_pos,[start_pos]))
    while not q.empty():
        current_pos,path=q.get()
        row,col=current_pos

        stdscr.clear()
        print_maze(maze,stdscr,path)
        time.sleep(0.3)
        stdscr.refresh()

    
        if maze[row][col]==end:
            return path
        neighbors=find_neighbors(maze,current_pos[0],current_pos[1])
        
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            r,c=neighbor
            if maze[r][c]=='#':
                continue

          
            visited.add(neighbor)
            q.put((neighbor,path+[neighbor]))


def find_neighbors(maze,row,col):
    neighbor=[]

    if row>0:
        neighbor.append((row-1,col))
    if row<len(maze)-1:
        neighbor.append((row+1,col))
    if col>0:
        neighbor.append((row,col-1))
    if col<len(maze[0])-1:
        neighbor.append((row,col+1))
    return neighbor



def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    
    find_path(maze,stdscr)
    stdscr.getch()
    
wrapper(main)