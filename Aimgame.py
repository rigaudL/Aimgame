import math
import random
import time
import pygame

pygame.init()
WIDTH , HEIGHT = 1000 , 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT)
pygame.display.set_caption("ACE'S Aim Trainer") 

TARGET_INCREMENT = 400 

TARGET_EVENT = pygame.USEREVENT 

TARGET_PADDING = 30 
BG_COLOR = (0, 25, 40) 
lives = 100
TOP_BAR = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2 
    COLOR = "Red"
    SECOND_COLOR = "White"
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
            
    def update(self): 
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
            
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
            
            
            
    def collide(self, x , y):
        dis = math.sqrt((self.x -x) ** 2 + (self.y - y) **2)    
        return dis <= self.size 
    
    
    
    def draw(self, win): #draws the target on the screen 
        pygame.draw.circle( win, self.COLOR ,(self.x, self.y) , self.size) 
        pygame.draw.circle( win, self.SECOND_COLOR ,(self.x, self.y) , self.size * 0.8)
        pygame.draw.circle( win, self.COLOR ,(self.x, self.y) , self.size * 0.6) 
        pygame.draw.circle( win, self.SECOND_COLOR ,(self.x, self.y) , self.size * 0.4) 
        


def draw(win, targets):
    win.fill(BG_COLOR)
    
    for target in targets:
        target.draw(win) 
        
        

def format_time(secs):
    mili = math.floor(int(secs*1000% 1000)/100)
    seconds = int(round (secs % 60, 1))
    minutes = int(secs // 60)
    
    return (f"{minutes:02d}:{seconds:02d}.{mili}")


def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "yellow", (0,0, WIDTH, TOP_BAR))
    time_label = LABEL_FONT.render(f"TIME:{format_time(elapsed_time)}", 1, "black") 

    speed = round(targets_pressed / elapsed_time, 1 )
    speed_label = LABEL_FONT.render(f" speed:{speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f" Hits: {targets_pressed} ", 1, "black")
    live_label = LABEL_FONT.render(f"Lives: {lives - misses} ", 1, "black")
    my_label = LABEL_FONT.render(f"ACE'S GAME", 1, "black")


    win.blit(time_label, (5,5)) #blit is how u write is how u display another surface 
    win.blit(speed_label, (210,5))
    win.blit(hits_label, (450,5))
    win.blit(live_label, (550,5))
    win.blit(my_label, (750, 5))
def end_screen(win, elapsed_time, targets_pressed , clicks):
    win.fill(BG_COLOR) 
    time_label = LABEL_FONT.render(f"TIME:{format_time(elapsed_time)}", 1, "white") 

    speed = round(targets_pressed / elapsed_time, 1 )
    speed_label = LABEL_FONT.render(f" speed:{speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f" Hits: {targets_pressed} ", 1, "white")
    accuray =  round(targets_pressed/ clicks * 100,1
    accuray_label = LABEL_FONT.render(f" Hits: {targets_pressed}% ", 1, "white")
    win.blit(time_label, (get_middle(time_label),5))
    win.blit(speed_label, (get_middle(speed_label) , 5))
    win.blit(hits_label, (get_middle(hits_label),5))
    win.blit(accuray_label, (get_middle(accuray_label) ,5))
    win.blit(my_label, (get_middle(my_label) , 5))
    pygame.display.update()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                run = False
                break
def get_middle(surface):
    
    return WIDTH / 2 -surface.get_width()/2  
    
    

    my_label = LABEL_FONT.render(f"ACE'S GAME", 1, "black")

    
def main():
    run = True
    targets = [] 
    clock = pygame.time.Clock() 
    target_pressed = 0
    clicks = 0
    misses = 0 
    start_time = time.time() 
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)
    
    while  run:
        clock.tick(60) 
        click = False
        mouse_position = pygame.mouse.get_pos() 
        elasped_time = time.time() - start_time 
        for event in pygame.event.get(): 
             if event.type == pygame.QUIT:
                 run = False
                 break
             if event.type ==  TARGET_EVENT:
                 x = random.randint(TARGET_PADDING, WIDTH -TARGET_PADDING)
                 y = random.randint(TARGET_PADDING + TOP_BAR, WIDTH -TARGET_PADDING) #add the + top bar to make sure all targets spawn under bar
                 target = Target(x , y) 
                 targets.append(target)
             if event.type == pygame.MOUSEBUTTONDOWN:
                 click = True
                 clicks += 1 # we clicked so changed 
        for target in targets:
            target.update()# changes size grow/shrink
            if target.size <= 0:
                targets.remove(target)
                misses += 1 
                
            if click and target.collide(*mouse_position):
                targets.remove(target)
                target_pressed += 1
            
            
            
        if misses >= lives:
            end_screen(WIN, elasped_time, targets_pressed , clicks)
            print(f"You've missed {misses} amount of times game over")
      
            
        draw(WIN, targets)        
        draw_top_bar(WIN, elasped_time, target_pressed, misses)
        pygame.display.update() 

                 
    pygame.quit()
    
if __name__ == "__main__":
    main() 
    
    
    
'''
problems: identation with my TARGET CLASS Update / draw methods so it wouldnt print it kept saying target .update in line 83 had no attribute update

issue with Target class update method i put == instead of = wchich didnt change the value of self.size

problem - longer i run the code the slower it goes 
reason - im not disposing of targets when it get to 0 size if i dont  remove when it get to 0 size my list just keeps gettting bigger in line 84-85
solution - add lines 86 - 87

then i ran my code and my targets didnt disapper because my if block that started in line 108 wasn't indented so it only checked once
'''
