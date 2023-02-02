from collections import deque
import datetime
import time
import heapq

ALPHA = 1

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
        self.costToGoal = 0
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __lt__(self, s):
        return self.cost < s.cost

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

    def updateMorids(self, s, moridsRec):
        for info in moridsRec:
            if not self.seenRecipes[info]: return
        self.seenMorids[s] = True

    def updateRecipes(self, s):
        self.seenRecipes[s] = True

    def updateHardVertices(self, s):
        self.remainingTime = self.seenHardVertics[s]
        self.seenHardVertics[s] += 1

    def heuristic(self, s, moridsRec, recipe):
        temp = []
        for i in range(len(recipe)):
            if recipe[i]:
                if not self.seenRecipes[i]:
                    self.costToGoal += 1
                    temp.append(i)
        for info in self.seenMorids:
            if not self.seenMorids[info] and int(info) not in temp:
                self.costToGoal += 1

class AStar:
  def __init__(self, n, graph, recipes, morids, allNodes):
    self.frontier = []
    self.counter = 0
    self.size = n
    self.graph = graph
    self.recipes = recipes
    self.morids = morids
    self.allNodes = allNodes


  def contains(self, state, explored):
    for item in explored:
        if(item.state == state.state and
            item.seenMorids == state.seenMorids and 
            item.seenRecipes == state.seenRecipes and
            item.remainingTime == state.remainingTime and
            item.seenHardVertics == state.seenHardVertics):
            if(item.f > state.f):
                return False
            return True
    return False


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
    print("Cost:", goal.cost)
    while(goal != None):
        path.append(goal.state + 1)
        goal = goal.parent

    for i in range(len(path) - 1, -1, -1):
        if (i != 0):
            print(path[i], end='->')
        else:
            print(path[i])

  def algorithm(self, start):
    explored = []
    frontier = []
    isReachedGoal = False
    start_node = State(n = self.size, state = start, morids = morids)
    self.counter = 1
    frontier.append((start_node.f, start_node))
    explored.append(start_node)
    goal = start_node
    self.updateChild(start_node, start)
    if(start_node.goalTest()):
        isReachedGoal = True

    while (frontier and not isReachedGoal):
        heapq.heapify(frontier)
        node = heapq.heappop(frontier)
        nodeF = node[0]
        node = node[1]
        if node.remainingTime == 0:
            for neighbor in self.graph[node.state]: 
                child_node = State(state=neighbor, n=self.size, morids = self.morids)
                child_node.copyFromParent(node)
                self.updateChild(child_node, neighbor)
                self.counter += 1
                child_node.increaseCost()
                if(child_node.goalTest()):
                    goal = child_node
                    isReachedGoal = True
                    break
                nodeInfo = allNodes[neighbor]
                child_node.g = node.g + child_node.cost
                child_node.heuristic(neighbor, nodeInfo.moridRecipes, recipes)
                child_node.h = child_node.costToGoal
                child_node.f = child_node.g + child_node.h * ALPHA

                if not self.contains(child_node, explored):
                    explored.append(child_node)
                    heapq.heappush(frontier, (child_node.f, child_node))

        else:
            node.decreaseRemainingTime()
            node.increaseCost()
            frontier.append((child_node.f, child_node))
    self.printPath(goal)



def getInput():
    f = open('input5.txt', 'r')
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
    recipes = [False] * n
    for i in range(s):
        temp = [int(x) for x in f.readline().split()]
        idx = temp.pop(0) - 1
        moridsInfo.append(idx)
        temp.pop(0)
        for item in temp: 
            allNodes[item - 1].isRecipe = True
            recipes[item - 1] = True
        allNodes[idx].updateMorid(temp)
        
    morids = {info: False for info in moridsInfo}

    starter = int(f.readline()) - 1

    return n, graph, morids, starter, recipes, allNodes

begin = time.time()
n, graph, morids, start, recipes, allNodes = getInput()
search = AStar(n, graph, recipes, morids, allNodes)
search.algorithm(start)
print("time :", time.time() - begin)