from puzzlegen import generate_puzzle
import heapq

# algo = 1 #manhattan
# algo = 2 #RowCOl-dist
# algo = 3 #Misplaced
algoList = [1,2,3]

def manhattan_dist(pt1, pt2):
    distance = 0
    for i in range(len(pt1)):
        distance += abs(pt1[i] - pt2[i])
    return distance

class MyClass:
    def __init__(self, puzzle,g):
        self.puzzle = puzzle
        row, col = self.find_empty()
        self.row = row
        self.col = col
        self.g = g
        self.prev = None
        self.finish = False


    def find_empty(self):
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                if self.puzzle[i][j] == 0:
                    return i, j

    def f(self):
        return self.g + self.get_h()
    
    def get_h(self):
        if algo == 1:
            return self.get_manhattan()
        if algo == 2:
            return self.get_rowcoldif()
        if algo == 3:
            return self.get_misplaced()

    def print(self):
        for i in self.puzzle:
            print(i)
    
    def get_children(self):
            actions = [(1,0),(0,1),(-1,0),(0,-1)]
            children = []
            for a in actions:
                row = self.row + a[0]
                col = self.col + a[1]
                if row < 0 or row > 2 or col < 0 or col > 2:
                    continue

                
                m = [puzzlerow[:] for puzzlerow in self.puzzle]
                temp = m[row][col]
                m[row][col] = 0
                m[self.row][self.col] = temp
                # if self.check_puzzle_in_path(m):
                #     continue

                if self.check_puzzle_in_closed(m,closedlist):
                    continue

                ns = MyClass(m,self.g+1)
                ns.prev = self
                children.append(ns)
            
            return children


    def get_misplaced(self):
        puzzle = self.puzzle
        count = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != goal[i][j] and puzzle[i][j] != 0:
                    count += 1
        
        if count == 0:
            self.finish = True
        return count

    def check_puzzle_in_path(self, matrix):
        state = self
        while state.prev != None:
            if state.puzzle == matrix:
                return True
            state = state.prev

        return False

    def check_puzzle_in_closed(self, m, closedlist):
        # for x in closedlist:
        #     if x == m:
        #         return True

        return matrixtostring(m) in closedlist

    def get_manhattan(self):
        state = self.puzzle
        distances = [[0,0,0] for i in range(3)]
        for i in range(len(state)):
            for j in range(len(state[i])):
                no = state[i][j]
                row, col = dicts[str(no)]
                distances[i][j] = manhattan_dist([i,j],[row,col])

        msum = 0
        for i in range(len(distances)):
            for j in range(len(distances[i])):
                msum += distances[i][j]
        
        if msum == 0:
            self.finish = True
        return msum

    def get_rowcoldif(self):
        state = self.puzzle
        distances = [[0,0,0] for i in range(3)]
        for i in range(len(state)):
            for j in range(len(state[i])):
                score = 0
                no = state[i][j]
                row, col = dicts[str(no)]
                if i != row:
                    score += 1
                if j != col:
                    score += 1
                distances[i][j] = score

        msum = 0
        for i in range(len(distances)):
            for j in range(len(distances[i])):
                msum += distances[i][j]
        
        if msum == 0:
            self.finish = True
        return msum

    def print_path(self):
        state = self
        sl = []
        while state != None:
            sl.append(state)
            state = state.prev
        while len(sl) > 1:
            state = sl.pop()
            state.print()
            print('    |')
            print('    |')
            print('    V')
        state = sl.pop()
        state.print()
        
        print("Tree depth: ", self.g)
    
def matrixtostring(matrix):
    s ='' 
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            s += (str(matrix[i][j]))
    
    return s



def get_next(openlist):
    best = openlist[0]
    bestv = best.f()
    for x in openlist:
        if x.f() < bestv:
            best = x
            bestv = x.f()
    return best
        
def create_dict(gs):
    mydict = {}
    for i in range(len(gs)):
        for j in range(len(gs[i])):
            mydict[str(gs[i][j])] = (i,j)

    return mydict

puzzles = []
for k in range(100):
    np = generate_puzzle()
    puzzles.append(np)

dummy = 0


for p in puzzles:
    results = []
    print(p)
    for algo in algoList:
        # S = MyClass([[1,2,5],[6,3,0],[4,7,8]],0)
        #S = MyClass([[1,2,3],[4,5,0],[6,7,8]],0) #13 steps to goal
        # S = MyClass([[3,6,2],[7,1,8],[0,4,5]],0)
        S = MyClass(p,0)
        goal = [[1,2,3],[4,5,6],[7,8,0]]
        dicts = create_dict(goal)

        openl = [(S.f(),dummy,S)]
        dummy += 1
        closedlist = {} 

        for i in range(100000):
            # print(i)
            if S.finish == True:
                # print("Goal!!")
                break
            # openl.remove(S)
            closedlist[matrixtostring(S.puzzle)] = 1
            children = S.get_children()
            # openl.extend(children)
            for x in children:
                heapq.heappush(openl,(x.f(),dummy,x))
                dummy += 1


            S = heapq.heappop(openl)[2]
            # nextNode = get_next(openl)

        # S.print_path()
        print(i)
        print(S.g)
        results.append(i)
        # if i > 1:
        #     break

    # output = str(p)
    # for x in results:
    #     output += "," + str(x)
    # print(output)

