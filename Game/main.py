from re import T
from select import select
from symbol import dotted_as_name
import time
import turtle
import math
import random
from copy import deepcopy
from time import sleep
from sys import argv

INF = 100000

class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False
    count = 0

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        sleep(1)
    
                
    def _swap_turn(self, turn):
        if turn == 'red':
            return 'blue'
        else:
            return 'red'

    def _evaluate(self):
        count = 0
        if self.gameover(self.red, self.blue) == 'red':
            return math.inf
        elif self.gameover(self.red, self.blue) == 'blue':
            return -math.inf
        elif self.turn == 'red':
            for move in (self.available_moves):
                self.available_moves.remove(move)
                self.red.append(move)
                if self.gameover(self.red, self.blue) == 'blue':
                    count -= 8
                elif self.gameover(self.red, self.blue) == 0:
                    count += 10
                self.available_moves.append(move)
                self.red.remove(move)
            return count
        elif self.turn == 'blue':
            for move in (self.available_moves):
                self.available_moves.remove(move)
                self.blue.append(move)
                if self.gameover(self.red, self.blue) == 'red':
                    count += 10
                elif self.gameover(self.red, self.blue) == 0:
                    count -= 8
                self.available_moves.append(move)
                self.blue.remove(move)
            return count

    def minimax(self, depth, player_turn):
        if depth == 0 or len(self.available_moves) == 0:
            return None, self._evaluate()
        alpha = -math.inf
        beta = math.inf
        if player_turn == 'red':
            value = -math.inf
            bestMove = None
            for move in (self.available_moves):
                self.turn = self._swap_turn(self.turn)
                self.available_moves.remove(move)
                self.red.append(move)
                _, tempValue =  self.minimax(depth - 1, self.turn)
                self.red.remove(move)
                self.available_moves.append(move)
                self.turn = self._swap_turn(self.turn)
                if tempValue >= value:
                    value = tempValue
                    bestMove = move
                alpha = max(alpha, value)
                if self.prune and beta <= alpha:
                    break
            return bestMove, value
        elif player_turn == 'blue':
            value = math.inf
            for move in (self.available_moves):
                self.turn = self._swap_turn(self.turn)
                self.available_moves.remove(move)
                self.blue.append(move)
                _, tempValue =  self.minimax(depth - 1, self.turn)
                self.blue.remove(move)     
                self.available_moves.append(move)     
                self.turn = self._swap_turn(self.turn)     
                if tempValue <= value:
                    value = tempValue
                    bestMove = move
                beta = min(beta, value)
                if self.prune and beta >= alpha:
                    break
            return bestMove, value
            
        
    def enemy(self):
        return random.choice(self.available_moves)

    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                selection = self.minimax(depth=self.minimax_depth, player_turn=self.turn)[0]
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        if len(r) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        if len(b) < 3: return 0
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__=="__main__":

    begin = time.time()
    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))
    # game = Sim(5, True, 0)
    results = {"red": 0, "blue": 0}
    for i in range(100):
        # print(i)
        results[game.play()] += 1

    print(results)
    print("Probability of Winning:", results['red'] / 100)
    print("Time of each Play:", (time.time() - begin)/100)
    print("Total time :", time.time() - begin)  
    