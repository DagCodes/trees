from queue import PriorityQueue

class Maze:
    def __init__(self):
        self.maze = []
        self.start = ()
        self.readFile()
        self.end = ()
        self.grid = []
        self.map = {}
        self.findStartEnd()
        self.findCoordinates()
        self.findMap()

    #Reads it from the input text
    def readFile(self):
        f = open("maze_10x10.txt", "r")
        for line in f:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            self.maze.append(line_list)

        f.close()

    # finds the start & end
    def findStartEnd(self):
        for i in range(len(self.maze[0])):
            if self.maze[0][i] == '0':
                self.end = (1,i+1)
        for i in range(len(self.maze[-1])):
            if self.maze[-1][i] == '0':
                self.start = (len(self.maze), i+1)
    def findCoordinates(self):
        for i in range(1, len(self.maze[0]) + 1):
            for j in range(1, len(self.maze) + 1):
                self.grid.append((j, i))
    def findMapHelper(self, x):
        value = {}
        if x[0] == 0:
            value["U"] = 0
        else:
            if self.maze[x[0]-1][x[1]] != "1":
               value["U"] = 1
            else:
                 value["U"] = 0

        if x[0] == len(self.maze) - 1:
            value["D"] = 0
        else:
            if self.maze[x[0]+1][x[1]] != "1":
               value["D"] = 1
            else:
                 value["D"] = 0
        
        if x[1] == 0:
            value["L"] = 0
        else:
            if self.maze[x[0]][x[1] - 1] != "1":
               value["L"] = 1
            else:
                 value["L"] = 0

        if x[1] == len(self.maze[0]) - 1:
            value["R"] = 0
        else:
            if self.maze[x[0]][x[1] + 1] != "1":
               value["R"] = 1
            else:
                 value["R"] = 0
        return value
        
    def findMap(self):
        for i, j in self.grid:
            self.map[(i,j)] = self.findMapHelper((i-1, j-1))
        
# A star class
class A:        
    def __init__(self):
        self.maze = Maze()
        self.g_score = {row: float("inf") for row in self.maze.grid}
        self.g_score[self.maze.start] = 0
        self.f_score = {row: float("inf") for row in self.maze.grid}
        self.f_score[self.maze.start] = self.manhattan(self.maze.start, self.maze.end)
        self.visited,self.solution=self.a(self.maze)
        self.drawMaze()

    def manhattan(self, cell,cell1):
        x,y=cell
        x1,y1=cell1
        return abs(x-x1) + abs(y-y1)

    def a(self, maze):
        pQueue = PriorityQueue()
        pQueue.put((self.manhattan(maze.start, maze.end), self.manhattan(maze.start, maze.end), maze.start))
        aPath = {}
        visited=[maze.start]
        while not pQueue.empty():
            currCell = pQueue.get()[2]
            visited.append(currCell)
            if currCell == maze.end:
                break        
            for i in 'RLUD':
                if maze.map[currCell][i]==True:
                    if i=='R':
                        childCell=(currCell[0],currCell[1]+1)
                    elif i=='L':
                        childCell=(currCell[0],currCell[1]-1)
                    elif i=='U':
                        childCell=(currCell[0]-1,currCell[1])
                    elif i=='D':
                        childCell=(currCell[0]+1,currCell[1])

                    g_score_helper = self.g_score[currCell] + 1
                    temp = g_score_helper + self.manhattan(childCell, maze.end)

                    if temp < self.f_score[childCell]:   
                        aPath[childCell] = currCell
                        self.g_score[childCell] = g_score_helper
                        self.f_score[childCell] = g_score_helper + self.manhattan(childCell, maze.end)
                        pQueue.put((self.f_score[childCell], self.manhattan(childCell, maze.end), childCell))

    
        solution= set()
        x = maze.end
        while x!=maze.start:
            solution.add(x)
            x=aPath[x]
        return visited,solution
        
    # replaces the maze 2D with the solution
    def drawMaze(self):
        for i, j in self.visited:
            self.maze.maze[i-1][j-1] = "2"
        for i, j in self.solution:
            self.maze.maze[i-1][j-1] = "5"
        self.maze.maze[self.maze.start[0]-1][self.maze.start[1]-1] = "5"
        for i in self.maze.maze:
            print(i)


x = A()
#saves the maze with a solution into a text file
with open('AOutput.txt', 'w') as f:
    for i in x.maze.maze:
        for j in i:
            f.write(j)
            f.write(" ")
        f.write('\n')
f.close()