import time
import msvcrt
import threading
import os
import random

field_size_x = 60
field_size_y = 23

game_over = False

player1_points = 0
player2_points = 0

class Point:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)


class Ball(Point):
    def __init__(self):
        self.x = int((field_size_x-2)/2)
        self.y = int((field_size_y-2)/2)
        self.is_step1 = True
        self.angle = random.randint(2,12)*22.5
        self.move_strategy = [[],[]]
        self.set_move_strategy(True)
        self.speed = 0.125

    def set_move_strategy(self, hit_horizontal_wall):
        if hit_horizontal_wall == True:
            if self.angle > 180:
                self.angle = 540-self.angle
            else:
                self.angle = 180-self.angle
        else:
            self.angle = 360-self.angle
            self.speed *= 0.9

        intervall_angle = self.angle // 22.5
        self.counter = 0
        if intervall_angle <= 1:# 0 & 22,5 Grad
            self.move_strategy = [[0,-1],[1,-1]]
        elif intervall_angle == 2:# 45 Grad
            self.move_strategy = [[1,-1],[1,-1]]
        elif intervall_angle == 3:# 67,5 Grad
            self.move_strategy = [[1,0],[1,-1]]
        elif intervall_angle == 4:# 90 Grad
            self.move_strategy = [[1,0],[1,0]]
        elif intervall_angle == 5:# 112,5 Grad
            self.move_strategy = [[1,0],[1,1]]
        elif intervall_angle == 6:# 135 Grad
            self.move_strategy = [[1,1],[1,1]]
        elif intervall_angle == 7:# 157,5 Grad
            self.move_strategy = [[0,1],[1,1]]
        elif intervall_angle == 8 or intervall_angle == 9:# 180 & 202,5 Grad
            self.move_strategy = [[0,1],[-1,1]]
        elif intervall_angle == 10:# 225 Grad
            self.move_strategy = [[-1,1],[-1,1]]
        elif intervall_angle == 11:# 247,5 Grad
            self.move_strategy = [[-1,0],[-1,1]]
        elif intervall_angle == 12:# 270 Grad
            self.move_strategy = [[-1,0],[-1,0]]
        elif intervall_angle == 13:# 292,5 Grad
            self.move_strategy = [[-1,0],[-1,-1]]
        elif intervall_angle == 14:# 315 Grad
            self.move_strategy = [[-1,-1],[-1,-1]]
        else:               # 337,5 Grad
            self.move_strategy = [[0,-1],[-1,-1]]
                


    def move(self,field):
        global game_over, player1_points, player2_points
        if self.x == 1:
            game_over = True
            player2_points += 1
            return
        if self.x == field_size_x-2:
            game_over = True
            player1_points += 1
            return
        if self.x == 2:
            if field[self.y][1] == '#':
                if self.y == 1:
                    self.angle= 135
                elif self.y == field_size_y-2:
                    self.angle= 45
                else:
                    offset = player1_bat.hit_offset(self.y)
                    self.angle += offset * 22.5
                self.set_move_strategy(False)
                self.x += self.move_strategy[0][0]
                self.y += self.move_strategy[0][1]
                self.is_step1 = False
                return
        if self.x == field_size_x-3:
            if field[self.y][field_size_x-2] == '#':
                if self.y == 1:
                    self.angle= 225
                elif self.y == field_size_y-2:
                    self.angle= 315
                else:
                    offset = player2_bat.hit_offset(self.y)
                    self.angle += offset * 22.5
                self.set_move_strategy(False)
                self.x += self.move_strategy[0][0]
                self.y += self.move_strategy[0][1]
                self.is_step1 = False
                return

        would_cross_border = False

        if self.y == 1:
            if self.is_step1 and self.move_strategy[0][1] == -1:
                 would_cross_border = True
            elif not self.is_step1 and self.move_strategy[1][1] == -1:
                 would_cross_border = True
        elif self.y == field_size_y-2:
            if self.is_step1 and self.move_strategy[0][1] == 1:
                 would_cross_border = True
            elif not self.is_step1 and self.move_strategy[1][1] == 1:
                 would_cross_border = True


        if would_cross_border:
            self.set_move_strategy(True)
            self.x += self.move_strategy[0][0]
            self.y += self.move_strategy[0][1]
            self.is_step1 = False
        else:
            if self.is_step1:
               self.x += self.move_strategy[0][0]
               self.y += self.move_strategy[0][1]
               self.is_step1 = False
            else:
               self.x += self.move_strategy[1][0]
               self.y += self.move_strategy[1][1]
               self.is_step1 = True

        

class Bat(Point):
    def __init__(self, isPlayer1):
        if isPlayer1:
            self.x = 1           
        else:
            self.x = field_size_x-2
        self.y = field_size_y//2
        self.points = [Point(self.x,self.y-2),Point(self.x,self.y-1),Point(self.x,self.y),
                          Point(self.x,self.y+1),Point(self.x,self.y+2)]
        
    def move_up(self):
        if self.y > 3:
            self.y -= 1
            self.points = [Point(self.x,self.y-2),Point(self.x,self.y-1),Point(self.x,self.y),
                          Point(self.x,self.y+1),Point(self.x,self.y+2)]

    def move_down(self):
        if self.y < field_size_y-4:
            self.y += 1
            self.points = [Point(self.x,self.y-2),Point(self.x,self.y-1),Point(self.x,self.y),
                          Point(self.x,self.y+1),Point(self.x,self.y+2)]

    def hit_offset(self, y):
        for point in self.points:
            if point.y == y:
                return (self.y - point.y)
        return 0




field = [
    ['+','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',' ','0',':','0',' ','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','+'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['+','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','+'],
    ]
def draw_field():   
    whole_field = ''
    for i in range(field_size_y):
        for j in range(field_size_x):
            whole_field += field[i][j]
        whole_field += '\n'
    os.system('cls')
    print(whole_field)


def ball_threading():
    ball = Ball()
    global game_over
    while True:
        while not game_over:
            ball.move(field)
            field[ball.y][ball.x] = 'o'
            draw_field()
            time.sleep(ball.speed)
            field[ball.y][ball.x] = ' '

        field[0][28] = str(player1_points)
        field[0][30] = str(player2_points)
        draw_field()
        time.sleep(2)
        ball = Ball()
        game_over = False


player1_bat = Bat(True)
player2_bat = Bat(False)
ball_thread = threading.Thread(target=ball_threading, args=())
ball_thread.start()

while True:
    #Set Bats
    for i in range(5):
        field[player1_bat.points[i].y][player1_bat.points[i].x] ='#'
        field[player2_bat.points[i].y][player2_bat.points[i].x] ='#'


    #Get input
    input_player = msvcrt.getch()
    #Reset bats on field
    for i in range(5):
        field[player1_bat.points[i].y][player1_bat.points[i].x] =' '
        field[player2_bat.points[i].y][player2_bat.points[i].x] =' '

    #analyse input
    if input_player[0] == 119:
        player1_bat.move_up()
    if input_player[0] == 115:
        player1_bat.move_down()
    if input_player[0] == 111:
        player2_bat.move_up()
    if input_player[0] == 108:
        player2_bat.move_down()

