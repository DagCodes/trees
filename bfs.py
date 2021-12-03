import time
start_time = time.time()

# creats the maze.
class Maze:
    def __init__(self):
        self.maze = []
        self.start = []
        self.end = []
        self.readFile()
        self. findStartEnd()

    #Reads it from the input text
    def readFile(self):
        f = open("maze_10x10.txt", "r")
        for line in f:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            self.maze.append(line_list)

        f.close()

    # finds the start & end and marks it with "S" - Start "E" - End
    def findStartEnd(self):
        for i in range(len(self.maze[0])):
            if self.maze[0][i] == '0':
                self.end.append("0")
                self.end.append(str(i))
                self.maze[0][i] = "E"
        for i in range(len(self.maze[-1])):
            if self.maze[-1][i] == '0':
                self.start.append(len(self.maze)-1)
                self.start.append(i)
                self.maze[len(self.maze)-1][i] = "5"

# A queue class implementation
class Queue:
    def __init__(self):
        self.queue = [""]
    def enqueue(self, val):
        self.queue.append(val)
    def dequeue(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        raise Exception("Empty")

# The BFS Algroithm
class BFS:
    def __init__(self, maze):
        self.maze = maze.maze
        self.queue = Queue()
        self.row, self.col, = maze.start[0], maze.start[1]
        self.finalMaze = maze.maze

    # Makes sure we are allowed to go in the given direction   
    def legal(self, moves):
        row, col = self.row, self.col
        for move in moves:
            temp = self.applyMoves(move, col, row)
            col = temp[0]
            row = temp[1]

            if not(0 <= col < len(self.maze[0]) and 0 <= row < len(self.maze)):
                return False
            elif (self.maze[row][col] == "1"):
                return False

        return True


    # Returns True if the maze is solveed, else false
    def solveHelper(self, moves):
        row, col = self.row, self.col
        for move in moves:
            temp = self.applyMoves(move, col, row)
            col = temp[0]
            row = temp[1]

        if self.maze[row][col] == "E":
            return True

        return False
    
    # Plots the moves in 2D array
    def drawMaze(self, solution, path=""):
        row, col = self.row, self.col
        coordinates = set()
        for move in path:
            temp = self.applyMoves(move, col, row)
            col = temp[0]
            row = temp[1]
            coordinates.add((row, col))

        for j, row in enumerate(self.finalMaze):
            for i, col in enumerate(row):
                if (j, i) in coordinates:
                    if solution:
                        self.finalMaze[j][i] = "5"
                    else:
                         self.finalMaze[j][i] = "2"

    # Navigates the direction
    def applyMoves(self, move, col, row):
        if move == "U":
            row -= 1
        elif move == "L":
            col -= 1
        elif move == "R":
            col += 1
        elif move == "D":
            row += 1
        return [col, row]

    # Makes sure we are not stuck in back and forth loop
    def visitedEdge(self, add, edge):
        if len(add) > 0:
            temp = add[-1]
            if edge == "U":
                if temp == "D": return True
            elif edge == "D":
                if temp == "U": return True
            elif edge == "R":
                if temp == "L": return True 
            elif edge == "L":
                if temp == "R": return True
        return False

   # Repeats the algorithm properly until the maze is solved
    def solve(self):
        add = ""
        visited = set()
        directions = ["U", "L","R", "D"]
        solution = ""
        while not self.solveHelper(add): 
            add = self.queue.dequeue()
            for j in directions:
                put = add + j
                if put not in visited and self.legal(put) and not self.visitedEdge(add, j):
                    visited.add(put)
                    self.queue.enqueue(put)
                solution = put
        for i in visited:
            self.drawMaze(False, i)
        self.drawMaze(True, solution)

# starts the program
maze = Maze()
bfs = BFS(maze)
bfs.solve()
for i in bfs.finalMaze:
    print(i)

#saves the maze with a solution into a text file
with open('BFSOutput.txt', 'w') as f:
    for i in bfs.finalMaze:
        for j in i:
            f.write(j)
            f.write(" ")
        f.write('\n')
f.close()
        