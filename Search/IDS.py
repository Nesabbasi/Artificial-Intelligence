from itertools import count
import time


class Node:
    def __init__(self, loc):
        self.isRecipe = False
        self.isMorid = False
        self.isHard = False
        self.moridRecipes = []
        self.location = loc

    def updateHard(self):
        self.isHard = True
    
    def updateRecipe(self):
        self.isRecipe = True
    
    def updateMorid(self, info):
        self.isMorid = True
        self.moridRecipes = [item - 1 for item in info]


class State:
    def __init__(self, n, state, morids):
        self.parent = None
        self.state = state
        self.cost = 0
        self.remainingTime = 0
        self.seenMorids = morids
        self.seenRecipes = [False] * n
        self.seenHardVertics = [0] * n
    
    def decreaseRemainingTime(self):
        self.remainingTime -= 1

    def increaseCost(self):
        self.cost += 1

    def goalTest(self):
        for i in self.seenMorids.keys():
            if not self.seenMorids[i]: return False
        return True
    
    def copyFromParent(self, parent):
        self.parent = parent
        self.cost = int(parent.cost)
        self.seenRecipes = list(parent.seenRecipes)
        self.seenMorids = dict(parent.seenMorids)
        self.seenHardVertics = list(parent.seenHardVertics)

    def updateMorids(self, s,  moridsRec):
        for info in moridsRec:
            if not self.seenRecipes[info]: return
        self.seenMorids[s] = True

    def updateRecipes(self, s):
        self.seenRecipes[s] = True

    def updateHardVertices(self, s):
        self.remainingTime = self.seenHardVertics[s]
        self.seenHardVertics[s] += 1



class IDS:
  def __init__(self, n, graph, morids, allNodes):
    self.frontier = []
    self.counter = 0
    self.size = n
    self.graph = graph
    self.morids = morids
    self.allNodes = allNodes

  def updateChild(self, node, idx):
    nodeInfo = allNodes[idx]
    if(nodeInfo.isHard):
        node.updateHardVertices(idx)
    if(nodeInfo.isRecipe):
        node.updateRecipes(idx)
    if(nodeInfo.isMorid):
        node.updateMorids(idx, nodeInfo.moridRecipes)

  def printPath(self, goal):
    path = []
    print("Count:", self.counter)
    print("cost:", goal.cost)
    while(goal != None):
        path.append(goal.state + 1)
        goal = goal.parent

    for i in range(len(path) - 1, -1, -1):
        if (i != 0):
            print(path[i], end='->')
        else:
            print(path[i])

  def recursiveDLS(self, node, maxDepth):
    if(node.goalTest()):
        goal = node
        isReachedGoal = True
        return goal, isReachedGoal
    
    if maxDepth == 0:
        return None, False
    isReachedGoal = False
    if node.remainingTime == 0:
        for neighbor in self.graph[node.state]:
            child_node = State(state=neighbor, n=self.size, morids = self.morids)
            child_node.copyFromParent(node)
            self.updateChild(child_node, neighbor)
            self.counter += 1
            child_node.increaseCost()
            res, isReachedGoal = self.recursiveDLS(child_node, maxDepth - 1)
            if isReachedGoal:
                return res, True
    else:
        node.decreaseRemainingTime()
    return None, isReachedGoal
    
  def DLS(self,start,maxDepth):
    start_node = State(n = self.size, state = start, morids = morids)
    self.updateChild(start_node, start)
    self.counter = 1
    path, isReachGoal =  self.recursiveDLS(start_node, maxDepth)
    if isReachGoal:
        self.printPath(path)
        return True
    return False
 
  def IDS(self, start):
    i = 1
    while(True):
        if (self.DLS(start, i)):
            break
        i += 1

def getInput():
    f = open('input3.txt', 'r')
    n, m = f.readline().split()
    n = int(n)
    m = int(m)

    graph = [[] for x in range(n)]
    for i in range(m):
        u, v = f.readline().split()
        u = int(u)
        v = int(v)
        graph[u - 1].append(v - 1)
        graph[v - 1].append(u - 1)

    allNodes = []
    for i in range(n):
        allNodes.append(Node(i))

    h = int(f.readline())
    idxHardV = [int(x) for x in f.readline().split()]
    for idx in idxHardV: 
        allNodes[idx - 1].isHard = True
        

    s = int(f.readline())
    moridsInfo = []
    for i in range(s):
        temp = [int(x) for x in f.readline().split()]
        idx = temp.pop(0) - 1
        moridsInfo.append(idx)
        temp.pop(0)
        for item in temp: allNodes[item - 1].isRecipe = True
        allNodes[idx].updateMorid(temp)
        
    morids = {info: False for info in moridsInfo}

    starter = int(f.readline()) - 1

    return n, graph, morids, starter, allNodes

begin = time.time()
n, graph, morids, start, allNodes = getInput()
search = IDS(n, graph, morids, allNodes)
search.IDS(start)
print("time :", time.time() - begin)