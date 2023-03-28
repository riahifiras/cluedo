import pygame
import random

HEIGHT = 800 #grid height
WIDTH = 800 #grid width
SIDE = 200 #side menu width
SQUARES = 25
SQUARE_SIDE = HEIGHT//SQUARES 
MARGIN = 4
IMAGE_WIDTH = 24

#class for grid
class grid:
    def __init__(self, size):
        self.size = size

    def set_up(self):
        for i in range(self.size+1):
            pygame.draw.line(screen, start_pos = ((HEIGHT // self.size)*i, 0), end_pos = ((HEIGHT // self.size)*i, WIDTH), color = "black")
            pygame.draw.line(screen, start_pos = (0, (WIDTH // self.size)*i), end_pos = (HEIGHT, (WIDTH // self.size)*i), color = "black")

#areas players can't reach (walls and borders)
#map borders
off_limits = [(HEIGHT+MARGIN, MARGIN+i*SQUARE_SIDE) for i in range(-1, 25)]+[(MARGIN+i*SQUARE_SIDE, HEIGHT+MARGIN) for i in range(-1, 25)]+[(MARGIN+i*SQUARE_SIDE, MARGIN-SQUARE_SIDE) for i in range(-1, 25)]+[(MARGIN-SQUARE_SIDE, MARGIN+i*SQUARE_SIDE) for i in range(-1, 25)]

#class for rooms
class room:
    def __init__(self, name, wall):
        self.name = name
        self.wall = wall
        #add room walls to off_limits
        off_limits.extend([(i[0]*SQUARE_SIDE+MARGIN, i[1]*SQUARE_SIDE+MARGIN) for i in self.wall])

    def show_room(self):
        for i in self.wall:
            pygame.draw.rect(screen, "white", pygame.Rect(i[0]*SQUARE_SIDE, i[1]*SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE))

#class for players
class player:
    def __init__(self, current_pos, img):
        self.current_pos = current_pos
        self.img = img

    def show_player(self):
        screen.blit(self.img, self.current_pos)
    
    def move_player(self, event):
        global illegal_move
        illegal_move = False
        original_pos = self.current_pos
        if event == pygame.K_LEFT:
            self.current_pos = (self.current_pos[0]-SQUARE_SIDE, self.current_pos[1])
        if event == pygame.K_RIGHT:
            self.current_pos = (self.current_pos[0]+SQUARE_SIDE, self.current_pos[1])
        if event == pygame.K_UP:
            self.current_pos = (self.current_pos[0], self.current_pos[1]-SQUARE_SIDE)
        if event == pygame.K_DOWN:
            self.current_pos = (self.current_pos[0], self.current_pos[1]+SQUARE_SIDE)
        if self.current_pos in off_limits:
            illegal_move = True
            self.current_pos = original_pos
        self.show_player()


#class for buttons
class button:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text
        self.state = "not_pressed"

    def show_button(self):    
        color_light = (170,170,170)
        color_dark = (100,100,100)
        smallfont = pygame.font.SysFont('Corbel',35)
        text = smallfont.render(self.text , True , (255,255,255))
        mouse = pygame.mouse.get_pos()
        if self.pos[0]/2 <= mouse[0] <= self.pos[0]/2+140 and self.pos[1]/2 <= mouse[1] <= self.pos[1]/2+40:
            pygame.draw.rect(screen,color_light,[self.pos[0]/2,self.pos[1]/2,140,40])  
        else:
            pygame.draw.rect(screen,color_dark,[self.pos[0]/2,self.pos[1]/2,140,40])
        screen.blit(text , (self.pos[0]/2+50,self.pos[1]/2))

    def action(self):
        self.state = "pressed"

#setting up pygame 
pygame.init()
screen = pygame.display.set_mode((HEIGHT + SIDE, WIDTH))
run = True
smallfont = pygame.font.SysFont('Corbel',20)

#setting up the grid
board = grid(SQUARES)

#players
p1_img = pygame.image.load("assets\\basketball-player.png")
p2_img = pygame.image.load("assets\\basketball.png")
p3_img = pygame.image.load("assets\player.png")
p4_img = pygame.image.load("assets\\tennis-player.png")
p5_img = pygame.image.load("assets\\tennis.png")
p6_img = pygame.image.load("assets\writer (2).png")
p1 = player((MARGIN, MARGIN), p1_img)
p2 = player((HEIGHT-MARGIN-IMAGE_WIDTH, MARGIN), p2_img)
p5 = player((MARGIN, HEIGHT-MARGIN-IMAGE_WIDTH), p5_img)
p4 = player((HEIGHT-MARGIN-IMAGE_WIDTH, HEIGHT-MARGIN-IMAGE_WIDTH), p4_img)
p3 = player((HEIGHT-MARGIN-IMAGE_WIDTH, (HEIGHT-IMAGE_WIDTH)//2), p3_img)
p6 = player((MARGIN, (HEIGHT-IMAGE_WIDTH)//2), p6_img)

players = [p1, p2, p3, p4, p5, p6]

#rooms
study = room('study', [(6, i) for i in range(5) if i != 2]+[(i, 4) for i in range(7)])
lounge = room('lounge', [(i, 4) for i in range(18,25) if i != 2]+[(18, i) for i in range(5) if i != 2])
conservatory = room('conservatory', [(6, i) for i in range(20, 25) if i != 22]+[(i, 20) for i in range(7)])
kitchen = room('kitchen', [(18, i) for i in range(20, 25) if i != 22]+[(i, 20) for i in range(18, 25)])
hall = room('hall', [(8, i) for i in range(7)]+[(i, 6) for i in range(8, 17) if i != 12]+[(16, i) for i in range(7)])
dining_room = room('dining room', [(18, i) for i in range(8, 17) if i != 12]+[(i, 8) for i in range(18, 25)]+[(i, 16) for i in range(18, 25)])
cellar = room('cellar', [(10, i) for i in range(10, 15)]+[(i, 14) for i in range(10, 15)]+[(14, i) for i in range(10, 15)]+[(i, 10) for i in range(10, 15) if i!=12])
billard_room = room('billard room', [(6, i) for i in range(13, 18) if i != 15]+[(i, 13) for i in range(7)]+[(i, 17) for i in range(7)])
library = room('library', [(6, i) for i in range(7, 12) if i != 9]+[(i, 7) for i in range(7)]+[(i, 11) for i in range(7)])
ballroom = room('ballroom', [(8, i) for i in range(18, 25)]+[(i, 18) for i in range(8, 17) if i != 12]+[(16, i) for i in range(18, 25)])

rooms = [study, lounge, kitchen, conservatory, hall, dining_room, cellar, billard_room, library, ballroom]

#buttons
roll_button = button((1650, 80), 'roll')
number_rolled = 0
num_player = 5
number_rolled_text = smallfont.render("number rolled is {}".format(number_rolled) , True , (255,255,255))

if __name__=="__main__":

    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and number_rolled > 0:
                players[num_player].move_player(event.key)
                if illegal_move == True:
                    illegal_move = False
                else:
                    number_rolled -= 1
            if roll_button.pos[0]/2 <= mouse[0] <= roll_button.pos[0]/2+140 and roll_button.pos[1]/2 <= mouse[1] <= roll_button.pos[1]/2+40 and event.type == pygame.MOUSEBUTTONDOWN:
                roll_button.action()
        screen.fill((30, 110, 160))
        board.set_up()
        for i in rooms:
            i.show_room()
        p1.show_player()
        p2.show_player()
        p3.show_player()
        p4.show_player()
        p5.show_player()
        p6.show_player()
        roll_button.show_button()
        screen.blit(number_rolled_text, (820, 120))
        if roll_button.state == "pressed":
            number_rolled = random.randint(1,12)
            if num_player == 5:
                num_player = 0
            else:
                num_player += 1
            number_rolled_text = smallfont.render("number rolled is {}".format(number_rolled) , True , (255,255,255))
            roll_button.state = "not_pressed"

        pygame.display.update()