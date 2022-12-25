#problem 1:
    #the major problem faced was the proper orientation and podistioning of the grid ans\d the falling shapes insid the grid.
    #we have to calculate the coordinates very careefully otherwise it used to overlap over each other.....


import pygame #help you make games and other multimedia applications
import random # in-built module of Python which is used to generate random numbers
import math   #  use for mathematical tasks

pygame.init()    #initialize all imported pygame modules is a convenient way to get everything started.
pygame.font.init()

#10x20 SQ GRID.

# GLOBALS VARS
s_width = 800 #sCREEN width
s_height = 700  #SCREEN height
play_width = 300  # meaning 300 // 10 = 30 width per block #exactly half of height to have perfect sq.
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

#top left pos of actual play area
top_left_x = (s_width - play_width) // 2  #gaps are there on left and right so we need to divide by 2
top_left_y = s_height - play_height  #we didn't divided by 2 as there is no gap at the bottom.


# SHAPE FORMATS
#list of lists
#we have included all the possible rotations of a shape
#shapes: S,Z,I,O,J,L,T
#'0' represents where the block actually exits.
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T] #list of lists of shapes
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)] #list of colors
# index 0 - 6 represent shape

#it is the main ds of our game and represents diff pieces.
#contsains info about the pices.

class Piece(object):  # *
    def __init__(self, x, y, shape): #initialization fn
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


#for grid we create a 2D list full of colors.
def create_grid(locked_pos={}):  # *locked pos is a dictoinary, it have ecah pos as key and the corresponding color as value
    #e.g: {(1,1):(225,0,0)} ->locked pos..........

    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)] #2D list

    #this is a blank grid

    #one list of 10 items for 20 times

    #0,0,0 reperesnts black clor.
    #there could be bloks already locked in the grid.
    #so we will chnage the color of the corresponding blocks in grid that already have some shapes in it.

    for i in range(len(grid)): #len(grid)=20
        for j in range(len(grid[i])): #==10
            if (j, i) in locked_pos: #if it exists in locked pos that means it contains a piece.
                c = locked_pos[(j,i)] #value of color at i,j
                grid[i][j] = c #change the clor of the block to the corresponding color of the piece.
    return grid

#return the list of pos of the shape given
def convert_shape_format(shape): #shape is like T,S...a list of lists........
#shape is also piece object.......
    positions = []#empty list
    #shape.shape will give the shape of the object called shape....
    format = shape.shape[shape.rotation % len(shape.shape)] #we need one list out of lists of list.......
     #at rot =0 we get first list, then anther and another and the cycle continues.......

    for i, line in enumerate(format): #Enumerate() method adds a counter.....
        row = list(line) #gives line in list format......
        for j, column in enumerate(row):
            if column == '0': #this is our position req, so add in pos list......
                positions.append((shape.x + j, shape.y + i)) #adding i and j to current x,y value of our shape inn the grid

    for i, pos in enumerate(positions):
        positions[i] = (pos[0]-2 , pos[1]-4 ) #this is done to remove the offset due to periods and pos the block more
#accurately on the screen...................
    return positions #returig the pos oof coordinates of all the block that belong to this shape

#checks weather the shapes are in their valid space or not.....
def valid_space(shape, grid): #shape is a piece object also..........
    #we only add those pos to our acc pos which have color black i.e which are empty.....
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] #list of all possible pos....
    accepted_pos = [j for sub in accepted_pos for j in sub] #flattens the above list [[(0,1)],[(2,3)]]-->[(0,1),(2,3)]
#it becomes easier to loop through..........
    formatted = convert_shape_format(shape) #liist of pos containing our shape...........
    for pos in formatted: #we compare both the lists to check weather the shape lies in valid pos or not.......
        if pos not in accepted_pos:
            if pos[1] > -1: # we allow some negative y values not in acc_pos, so that the shapes looks like falling and dont look like they are popping suddenly
                return False
    return True


#problem 2:
    #the shapes looked like that they were poping suddnely so we aloowed some -ve y in valid spaces so that it look like its falling

#checks that the y value of last block hit y=0 line or not
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1: #if pos is less than 1 ie 0 we are lost .....
            return True
    return False #if every pos is more than 0 we are not lost......

def get_shape():
    return Piece(5, 0, random.choice(shapes)) #randomly return a shape from shapes list....

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True) #creating font object.......
    label = font.render(text, 1, color) #Create a Text surface object in which Text is drawn on it....
    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
# half of label width is sub to put the half of text in right and half in left......

def draw_grid(surface, grid): #it will draw the lines in the grid.........
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)): #grey color lines are drawn
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size)) #horizontal lines
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height)) #vertical lines

#clears a full colored row and shifts the above row below.......
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1): #look through our grid backward so that we dont overwrite while shifting dowm
        row = grid[i]
        if (0,0,0) not in row: #if not black then clear the compl row..
            inc += 1 #it tells how many rows we need to move dowm....
            ind = i #it tells which pos needed to be shift.........
            for j in range(len(row)):
                try:
                    del locked[(j,i)] #after deleting the row we need to shift everything
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]: #sorted the list based on y value.
            x, y = key
            if y < ind: #if y value is above the curr index.......
                newKey = (x, y + inc) #shifteing the row down
                locked[newKey] = locked.pop(key)
    return inc #returns nuber of rows cleared.....

#it draws the next shape on the right hand side...
def draw_next_shape(shape, surface): #this shape is piece objet....
    font = pygame.font.SysFont('comicsans', 30) #font object....
    label = font.render('Next Shape', 1, (255,255,255)) #text color white
#pos of the next shape.........
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)] #it is real shape list out of list of lists of shape.......

    for i, line in enumerate(format): #we will draw a constant imapge of shape for showing the next shape.........
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30)) #write the content of label

#updates the value of highest score in the score text file
def update_score(nscore):
    score = max_score() #gives last max score.....
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score)) #high score remain same so we write that again
        else:
            f.write(str(nscore)) #high score is changed

#returns the value of max score.......
def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip() #it removes /n from the text files........whiich is invisible to us
    return score

def draw_window(surface, grid, score, last_score ): #displays the score, highscore and tetris in the game window.......
    surface.fill((0, 0, 0))
    start, end = 30, 25
    #these are the rectangles in the left , right and top
    pygame.draw.rect(surface, (128, 128, 128), (start + 220, end, 300, 50))
    pygame.draw.rect(surface, (48,48,48), (start, end, 200, s_height - end-20))
    pygame.draw.rect(surface, (48,48,48), (start + s_width - 260, end, 210, s_height - end-20))
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30)) #writting the game name.........
#this written in the label will be copied to the surface
    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

#pos where we will show the score
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 10, sy + 160)) #bllit stands for blcok transfer and is used to copy the content of one surface to
   #another
   # last score
    label = font.render('High Score: ' + last_score, 1, (255,255,255))
    sx = top_left_x - 200 #in the left side
    sy = top_left_y + 200 #in the middle
    surface.blit(label, (sx + 20, sy + 160)) #writting the high score......
    for i in range(len(grid)): #wee are drawing rectangles....
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    draw_grid(surface, grid) #it will draw horizontal and verrtical lines......

def main(win,speed):
    last_score = max_score() #contains the max score
    locked_positions = {} #dic
    grid = create_grid(locked_positions) #contains the grid with no rec.
    change_piece = False
    run = True
    current_piece = get_shape() #piece object..contains the curr coming shape.....
    next_piece = get_shape() #piece object....contains the next coming shape.....
    clock = pygame.time.Clock() #clock object
    fall_time = 0
    fall_speed = speed
    level_time = 0
    score = 0 #contains curr score
    end=False
    # run=False
    # end=True
    while run:
        grid = create_grid(locked_positions) #we will update the grid based on locked pos
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        if level_time/1000 > 5: #at every 5 sec we inc the speed
            level_time = 0
            if level_time > 0.12: #so that the time dont get negative
                level_time -= 0.005 #dec the level time will inc the speed
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0: #if this is true we aare at the bottom or above another piece
                current_piece.y -= 1 #reverse to a valid space.......
                change_piece = True #doing this will fix the curr piece and bring another piece
        for event in pygame.event.get(): #pygamme.QUIT->deactivates the Pygame library
                                           #pygame.KEYDOWN ->detects a key is preesed or not
                                               #pygame.k_q->detects if q is pressed
                                               # so q dabane pe ruk jaygea game.............
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q): #this will stop the loop
                run = False #and the game will stop
                end=True
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: #on hitting left the block should move left......
                    current_piece.x -= 1  #current piece=get_sgape(), which return a piece object having x,y, shape.......
                                           #we reduced the x of the current piece by 1 to move it left....
                    if not(valid_space(current_piece, grid)): #checking if the piece in withing play screen limits....
                        current_piece.x += 1 #if the piece go out we just reverse and do nothing...
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1  #we added 1 to x of the curr piece to move it right on pressing right arrow.
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1 #move 1 block down on preeing down arrow........
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:  #we change the rotation of the piece on pressing up key
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_SPACE: #on clicking space the piece will directly jump to the bottom most pos possible
                    while True:
                        current_piece.y += 1 #we will inc while we hit a non valid space
                        if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                            current_piece.y -= 1 #as we hit a non valid space we will go 1 step back and break the loop.
                            change_piece = True
                            break

        shape_pos = convert_shape_format(current_piece) #give the pos where piece is present....
        for i in range(len(shape_pos)):#this will show the color of moving piece
            x, y = shape_pos[i]
            if y > -1: #so that the pice is inside the grid completely...........
                grid[y][x] = current_piece.color #adding color to the current pos of the piece in the grid...........

        if change_piece: #it means we hit the bottom or other piece...we wll update locked pos....
            for pos in shape_pos: #this will help in imarting color at the fixed pos......
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color #locked pos is a dic having colors of the block we are updating it
                #when we pass it to create grid it helps in chnaging the color of the grid to the piece color
            current_piece = next_piece #takes the prev value of next shape...
            next_piece = get_shape() #put new shape in next shape........
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10 #checking that a row is compl and del the comp row and inc the score.....

#we called clear rows here nott in loop because there is poss that while coming down at some point we get full row colored
#but we dont want that to be removed we only want the row to be removed whhen the piece gets locked atv the bootom and full
#row gets colored.................

        draw_window(win, grid, score, last_score) #dispaly the score
        draw_next_shape(next_piece, win) #draws the next piece on the screen.. as next shape contains the next coming shape
        pygame.display.update() #update the window to show the next shape.

        if check_lost(locked_positions): #checking lost after each step
            run = False
            end=True
            update_score(score) #it will update the highest scoree in our text file after we are lost

    clock=pygame.time.Clock()
    time=0
    global shape_stream, offset
    while end:
        win.fill((17,12,17))
        for i, stream in enumerate(shape_stream):
            draw_stream(stream, (i - 1) * 3 * block_size, offset[i], int(offset[i] / 40))
        pygame.draw.rect(win, (0, 150, 100), (top_left_x - 125, 50, 550, 550))
        time += clock.get_rawtime()
        clock.tick()
        if time<100:
            color=(255,255,255)
        elif time>=100 and time<200:
            color=(0,255,0)
        elif time>=200 and time<300:
            color=(0, 0, 255)
        elif time>=300:
            color = (0, 0, 255)
            time=0
        t = 'YOU LOST!'
        draw_text_name(win, 45, 150, t, 50, color)
        t = 'Press Q To QUIT'
        draw_text_name(win, 5, 200, t, 50, color)
        t = 'Press A To Play Again'
        draw_text_name(win, -30, 250, t, 50, color)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q): #if we select q or close the game then it will return -1
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a: #if we press a it will return 1 and the main menu loop will run again and we can play again
                return 1

def draw_text_name(surface, x, y,text, size, color):
    size-=22
    font = pygame.font.SysFont("bookmanoldstyle", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x+x , top_left_y+y))

def create_stream():
    stream = []
    for _ in range(6):
        temp = Piece(0, 0, random.choice(shapes))
        temp.rotation += random.randint(0, 4)
        stream.append(temp)
    return stream

def draw_shape(shape, surface, sx, sy):
    form = shape.shape[shape.rotation % len(shape.shape)]
    block_size_temp=20
    height = s_height + 50
    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                color=shape.color
                pygame.draw.rect(surface, color,(sx + j * block_size_temp, (sy % height) + (i+1) * block_size_temp - 100,
                                                 block_size_temp, block_size_temp), 0)

def draw_stream(shape_stream, x, offset, speed):
    for j, shape in enumerate(shape_stream):
        draw_shape(shape, win, x, offset + shape.y + j * block_size * 9)
        shape.y += speed
def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
def rotateLinePoints(start, end, degrees):
    startx, starty = start
    endx, endy = end
    middleX = (startx + endx) // 2
    middleY = (starty + endy) // 2
    inRadians = math.radians(degrees)
    newStart = rotate((middleX, middleY), start, inRadians)
    newEnd = rotate((middleX, middleY), end, inRadians)
    return newStart, newEnd
def drawScreen(screen):
    global counter
    counter += 2
    screen.fill((0,0,0))
    for line in lines:
        newStart, newEnd = rotateLinePoints(line[:2], line[2:], counter)
        pygame.draw.line(screen,(255,255,255), newStart, newEnd, 10)

def information_win(win):
    time=0
    clock=pygame.time.Clock()
    while True:
        drawScreen(win)
        pygame.draw.rect(win, (0, 150, 100), (top_left_x - 125, 50, 550, 550))
        t = 'INSTRUCTIONS'
        font = pygame.font.SysFont("signpainterttc", 85, bold=True)
        label = font.render(t, 1, (255, 255, 255))
        win.blit(label, (top_left_x + (-110), top_left_y + 0))
        t = 'Press Q to quit'
        draw_text_name(win, -100, 150, t, 40, (255, 255, 255))
        t = 'Press Left Arrow To Move Left'
        draw_text_name(win, -100, 180, t, 40, (255, 255, 255))
        t = 'Press Right Arrow To Move right'
        draw_text_name(win, -100, 210, t, 40, (255, 255, 255))
        t = 'Press Up Arrow To rotate the shape'
        draw_text_name(win, -100, 240, t, 40, (255, 255, 255))
        t = 'Press Down Arrow repeatedly To Move faster'
        draw_text_name(win, -100, 270, t, 40, (255, 255, 255))
        t = 'Press Space Bar For Hard Drop'
        draw_text_name(win, -100, 300, t, 40, (255, 255, 255))
        time += clock.get_rawtime()
        clock.tick()
        if time < 100:
            color = (255, 255, 255)
        elif time >= 100 and time < 200:
            color = (255,0, 0)
        elif time >= 200 and time < 300:
            color = (0, 0, 255)
        elif time >= 300:
            color = (0, 0, 255)
            time = 0
        t = 'PRESS A TO GO BACK'
        draw_text_name(win, -100, 400, t, 60, color)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT  or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                return 1

def main_menu(win):#shows the main menu that comes on starting the game.......
    run = True
    global shape_stream,offset
    while run:
        win.fill((17,12,17))
        for i, stream in enumerate(shape_stream):
            draw_stream(stream, (i - 1) * 3 * block_size, offset[i], int(offset[i] / 40))
        pygame.draw.rect(win, (0, 150, 100), (top_left_x - 125, 50, 550, 550))
        t = 'DELHI TECHNOLOGICAL UNIVERSITY'
        draw_text_name(win, -50, 0, t, 47, (255, 255, 255))
        t = 'Made by :'
        draw_text_name(win, 85, 260, t, 45, (255, 255, 255))
        t = 'TANEESHA GAUR'
        draw_text_name(win, 50, 300, t, 45, (255, 255, 255))
        t = 'HARSHIT MUHAL'
        draw_text_name(win, 50, 330, t, 45, (255, 255, 255))
        logo = pygame.image.load('logo2.png')
        logo = pygame.transform.scale(logo, (150, 150))
        win.blit(logo, (top_left_x + 85, 170))
        text = 'Press E Key To Play in Easy Mode'
        draw_text_name(win, -90, 390, text, 40, (255,255,255))
        text = 'Press M Key To Play in Medium Mode'
        draw_text_name(win, -90, 415, text, 40, (255, 255, 255))
        text = 'Press D Key To Play in Difficult Mode'
        draw_text_name(win, -90, 440, text, 40, (255,255,255))
        text = 'Press I To see Instructions'
        draw_text_name(win, -90, 465, text, 40, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    f=main(win,0.28) # in easy we give lower sppeed
                    if f==-1:
                        run = False
                if event.key == pygame.K_m:
                    f=main(win, 0.14) #entering the main will start the game.......
                    if f==-1:
                        run = False
                if event.key == pygame.K_d:
                    f=main(win,0.09)
                    if f==-1:
                        run = False
                if event.key == pygame.K_i: #pressisng i will open the info window that tells aout game rules.....
                    f=information_win(win)
                    if f==-1:
                        run = False
                if event.key == pygame.K_q: #pressing q will close the game window........
                    run=False
    pygame.display.quit()
counter = 0
lines = []
square = 50
for x in range(0, s_width, square):
    for y in range(0, s_height, square):
        if random.random() > 0.5:
            lines.append([x, y, x + square, y + square])
        else:
            lines.append([x, y + square, x + square, y])

shape_stream = [create_stream() for _ in range(20)]
offset = [block_size * random.randrange(3, 10) for _ in range(len(shape_stream))]
win = pygame.display.set_mode((s_width, s_height)) #pyagmae window or surface........
pygame.display.set_caption('Tetris') # Set the current window caption
pygame.mixer.music.load("Tetris.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
main_menu(win)
pygame.mixer.music.stop()

