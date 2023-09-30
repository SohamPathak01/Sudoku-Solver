import pygame
import time

pygame.init()


class Grid:
    board = [ [7,8,0,4,0,0,1,2,0],
              [6,0,0,0,7,5,0,0,9],
              [0,0,0,6,0,1,0,7,8],
              [0,0,7,0,4,0,2,6,0],
              [0,0,1,0,5,0,9,3,0],
              [9,0,4,0,6,0,0,0,5],
              [0,7,0,3,0,0,0,1,2],
              [1,2,0,0,0,7,4,0,0],
              [0,4,9,2,0,6,0,0,7] ]
    

    def __init__(self,rows,cols,height,width,win):

        self.rows = rows
        self.cols = cols
        self.height = height
        self.width = width
        self.win = win
        self.cubes = [[Cube(self.board[i][j], i,j, width,height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.update_model()
        self.selected = None
        self.finish = False


    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]


    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)
            
            
            
            
    def place(self, val):
        row, col= self.selected
        if self.cubes[row][col].value==0:
            self.cubes[row][col].set(val)        
            self.update_model()


            if self.valid(val, row, col) and self.solve():
                return True
            
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def valid(self, val, row, col):

        for i in range(0,9):
            if self.model[row][i] == val and i != col:
                return False

            if self.model[i][col] == val and i != row:
                return False

            r=3*(row//3)+(i//3)
            c=3*(col//3)+(i%3)

            if self.model[r][c] == val and (r,c) != (row,col):
                return False

        return True
    

    def find_empty(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.model[i][j] == 0:
                    return (i, j)
        
        return None


    def solve(self):
        find = self.find_empty()
        
        if not find:
            return True
        
        else:
            row,col = find

        for i in range(1,10):
            if self.valid(i, row, col):
                self.model[row][col]=i

                if self.solve():
                    return True

            self.model[row][col] = 0

        return False

    
    def is_finished(self):
        for i in range(9):
            for j in range(9):

                if self.cubes[i][j].value == 0:
                    return False
                
        self.finish = True

        return True

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap =self.width/9
            c = pos[0] // gap
            r = pos[1] // gap
            return (int(r),int(c))

        else:
            return None

    
    def select(self, row, col):
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):

        gap = self.width / 9
        for i in range(self.rows+1):
            if i%3 == 0 and i!=0:
                thick = 4
            else:
                thick = 1
            
            pygame.draw.line(self.win, (0,0,0), (0,i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0,0,0), (i*gap, 0), (i*gap, self.height), thick)


        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)
            
        
    
    def format_time(self, secs):
        sec = secs % 60
        minute = secs // 60

        play_time = str(minute) + ":" + str(sec)
        return play_time


    def redraw_window(self, play_time):
        self.win.fill("#FFE4C4")

        
        fnt = pygame.font.SysFont("comicsans", 40)
        text = fnt.render("Time: " + self.format_time(play_time), True,(0,0,0))
        self.win.blit(text, (510 -180, 550))
        if self.finish:
            fnt = pygame.font.SysFont("comicsans",40, bold=True)
            text =fnt.render("Winner... ", True , (0,0,255))
            self.win.blit(text, (20, 550))

        
        self.draw()


    def strikes(self, cross):
        fnt = pygame.font.SysFont("comicsans", 40, bold = True)

        if cross:
            text=fnt.render("X", True, (255,0,0))
        
        else:
            text = fnt.render("Correct", True, (0, 255, 0))

        self.win.blit(text, (20, 550))
        pygame.display.update()
        pygame.time.delay(700)


    def solve_gui(self):
        self.update_model()
        find = self.find_empty()

        if not find:
            self.finish = True
            return True

        else:
            row, col = find


        for i in range(1, 10):
            if self.valid(i, row, col):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)


                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win,False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

    

class Cube:
    rows = 9
    cols = 9


    def __init__(self,value,row,col,width,height):

        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False


    def set_temp(self, val):
        self.temp = val


    def set(self, val):
        self.value = val


    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)


        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap


        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), True, (128, 128, 128))
            win.blit(text, (x+5, y+5))

        elif not (self.value == 0):
            text = fnt.render(str(self.value), True, (0,0,0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap/2 -text.get_height() / 2)))


        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y,gap,gap),3)


    
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width/9
        x=self.col*gap
        y=self.row*gap

        pygame.draw.rect(win, (255,255,255), (x, y, gap,gap),0)

        text = fnt.render(str(self.value), True, (0,0,0))
        win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 -text.get_height()/2)))
        if g:
            pygame.draw.rect(win, (0,255,0), (x,y,gap,gap), 3)

        else:
            pygame.draw.rect(win, (255,0,0), (x,y,gap, gap), 3)

        

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9,9,550,550,win)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None


                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                
                if event.key == pygame.K_RETURN:
                    i,j = board.selected
                    if board.place(board.cubes[i][j].temp):
                        print("Success")
                        board.strikes(False)
                    else:
                        board.strikes(True)
                        print("Wrong")
                        strikes +=1
                    key = None

                if board.is_finished():
                    print("Game Over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        board.redraw_window(play_time)
        pygame.display.update()


main()
pygame.quit()

     
    



