import math
import random
import time
import pygame

pygame.init()
WIDTH , HEIGHT = 1000 , 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #makes a pygame window n display on screen and can draw stuff on it
pygame.display.set_caption("ACE'S Aim Trainer") # name of window ^^

TARGET_INCREMENT = 400 # IF # is smaller it makes it harder and if # is higher than it makes it easier cuz targets come later and these are miliseconds wantt to delay until i make another target 

TARGET_EVENT = pygame.USEREVENT # custom event

TARGET_PADDING = 30 # how many pixels i want it off the edge of the screem
BG_COLOR = (0, 25, 40) # EACH value is a color i define it in a tuple n i can use in a function in python
lives = 100 #tries
TOP_BAR = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

class Target:
    MAX_SIZE = 30 # size that starts shrinking , it grows to this size then starts shrinking
    GROWTH_RATE = 0.2 # how many pixels i want to grow the target per frame as i adjust it makes it makes it more diffivult
    COLOR = "Red"
    SECOND_COLOR = "White"
    
    def __init__(self,x,y): #this is a constructer self refers to the construccter and x , y is the pos where i want to place the target on the screen randomly n store inside the target object
        self.x = x
        self.y = y
        self.size = 0 # radius of target and inscrease by growth rate till it reaches max size when it hit max size it start shrinking and when it hit 0 it disapear
        self.grow = True # i need to make false when it start shrinking instead of growing 
            
    def update(self): # to update target size inside i cehck if target growing or shrinking and adujst target when that happen
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
            
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
            
            
            
            # this blow tracks if qw clicked
    def collide(self, x , y): # write func n gonna put on each target or target class x,y is mouse position
        #performin collision see if distance of str8 line if grater than radius # DO CHATGBT TO UNDERSTAND THISS    
        dis = math.sqrt((self.x -x) ** 2 + (self.y - y) **2) # distance to a point formula     
        return dis <= self.size # any coordinates i put i must keep the order (self.y - y) 
    
    
    
    def draw(self, win): #draws the target on the screen 
        pygame.draw.circle( win, self.COLOR ,(self.x, self.y) , self.size) #drawing things in pygame is diff for diff shapes but in the parameters what we pass are (the window i want to draw something on,  the color of the circle, the center position of the circle , the radius of the circle)
        pygame.draw.circle( win, self.SECOND_COLOR ,(self.x, self.y) , self.size * 0.8) # need 4 circles if imma do target circle multiple colors 1sr circle must be largest and the rest must be smaller than each other
        pygame.draw.circle( win, self.COLOR ,(self.x, self.y) , self.size * 0.6) # have to use multiply to change shape so when 1 ring changes all the others do dynamically
        pygame.draw.circle( win, self.SECOND_COLOR ,(self.x, self.y) , self.size * 0.4) # EACH Circle gets overlaped on top of each other in pygame the order where i draw stuff is important everything after goes on top of the previous line/overlap it
        


def draw(win, targets):
    win.fill(BG_COLOR)
    
    for target in targets:
        target.draw(win) # loops thru alll targets n put them on the screen 
        
        

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
    win.fill(BG_COLOR) # clear eveything pn the screen czu i want the txt in the middle of the screen 
# main loop that deals with diff events on window pressin on screen quitting window if target apperred or not and its a infinit loop untill i quit the window
    time_label = LABEL_FONT.render(f"TIME:{format_time(elapsed_time)}", 1, "white") 

    speed = round(targets_pressed / elapsed_time, 1 )
    speed_label = LABEL_FONT.render(f" speed:{speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f" Hits: {targets_pressed} ", 1, "white")
    accuray =  round(targets_pressed/ clicks * 100,1)# num of targets we pressed and num of targets weve pressed / # of clicks we got 
    accuray_label = LABEL_FONT.render(f" Hits: {targets_pressed}% ", 1, "white")
    win.blit(time_label, (get_middle(time_label),5)) #blit is how u write is how u display another surface 
    win.blit(speed_label, (get_middle(speed_label) , 5))
    win.blit(hits_label, (get_middle(hits_label),5))
    win.blit(accuray_label, (get_middle(accuray_label) ,5))
    win.blit(my_label, (get_middle(my_label) , 5)) # way we render middle of screen i must take middle of screen  x/2 - width / 2 then i draw obj in center pretty much i take the width oif the screen / 2 then - by width of obj we drawing pver 2 that gives x pos where we draw to make obj in thwe middlew
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
    # when user press the x in window its an event and we need to handle that event to close the window for user
    targets = [] #loop thru targest n update size and every x seconds i must place new targets on screen must create a custom event and triggers every x seconds  then check event and make new target at random position and then add it 
    
    clock = pygame.time.Clock() # need to introducute frame rate to control speed
    target_pressed = 0
    clicks = 0
    misses = 0 # target popped up on the screen and we missed when i get certain # of misses then the game ends
    start_time = time.time() # do 2 see when we started running code and started tracking how much time passs to show how long the round is
    
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) # trigger the target event every , target_increment seconds
    
    
    while  run:
        clock.tick(60) # mean run 60 frames per second on any computer that can run without this it wud go on processor speed n that varies
        click = False # look at events and if user clicked mouse down then change to true then check if mouse position colided with target
        mouse_position = pygame.mouse.get_pos() # gives us x,y position in  py game and its a tuple(x,y) and its considered 1 object 
        elasped_time = time.time() - start_time # if we access to start time tehn can get time elasped by taking current time n subtrating by the starttime willl give # of secs that elapsed 
        for event in pygame.event.get(): # loops thru all events thats going how ever fast its running
             if event.type == pygame.QUIT:
                 run = False
                 break
             if event.type ==  TARGET_EVENT:
                 x = random.randint(TARGET_PADDING, WIDTH -TARGET_PADDING) # TO MAKE SURE targests dont go off the string cuz it starts at center and radius goes right n left 
                 
                 #geberating a random # to make sure the to make sure the center make the target dont be off the screen 
                 y = random.randint(TARGET_PADDING + TOP_BAR, WIDTH -TARGET_PADDING) #add the + top bar to make sure all targets spawn under bar
                 target = Target(x , y) # initilize new instances of target class
                 targets.append(target) # put new target object in list to use it n loop thru it n now every x seconds i create a new target 
             if event.type == pygame.MOUSEBUTTONDOWN:
                 click = True
                 clicks += 1 # we clicked so changed 
        for target in targets:
            target.update()# changes size grow/shrink
            if target.size <= 0:
                targets.remove(target) # remove it out the list so we wont go over it , i put it here so i can update list first because if if was first we wud never see the targets cuz the list start at size 0
                misses += 1 # when target is removed we increment cuz we missed the target
                
            if click and target.collide(*mouse_position): # when i use a * as func argument it breaks down the tuple into its indivual part #also in the collide function its not taking in a tuple but mouse pos turns it into a tuple so i use * to get the indiviudal values it equals mouse position[0], mouse position[1] its known as splat operator
                targets.remove(target)
                target_pressed += 1
            
            
            
        if misses >= lives:
            end_screen(WIN, elasped_time, targets_pressed , clicks)
            print(f"You've missed {misses} amount of times game over")
            # break
            # pass # end the game or i cud just subc=tract from the lives
            
            
        draw(WIN, targets)        
        draw_top_bar(WIN, elasped_time, target_pressed, misses)
        pygame.display.update() # onlu=y update after eveything draws all targets n fills the screen in

                 
    pygame.quit() # quit the pygame window and close it
    
if __name__ == "__main__":
    main() # if i important any function in another file it dont start this game up 
    
    
    
'''
problems: identation with my TARGET CLASS Update / draw methods so it wouldnt print it kept saying target .update in line 83 had no attribute update

issue with Target class update method i put == instead of = wchich didnt change the value of self.size

problem - longer i run the code the slower it goes 
reason - im not disposing of targets when it get to 0 size if i dont  remove when it get to 0 size my list just keeps gettting bigger in line 84-85
solution - add lines 86 - 87

then i ran my code and my targets didnt disapper because my if block that started in line 108 wasn't indented so it only checked once
'''