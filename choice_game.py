import pygame, sys
from pygame.locals import *
import dragons_story

story = dragons_story.story
current = story[1]
but1_txt = current[1]
but2_txt = current[2]
position = 1

# Structure for the story: dict {}, key is positional value (int), values is tuple of: Text on screen (mandatory), 
# Text on button (at least one), 
# Button value, ie: points to which key next
# Since each Button has a text and a value, the scripts gets the number of buttons by dividing the length of tuple by two minus the text on screen
# which allows for as many buttons as you want
# The script will write a file 'save.txt' with the key value so that it can be restarted where you left off


class filesave:
    def retrievesave(self):
        try:
            with open('save.txt', 'r+') as save:
                position = int(save.read())
                list(story[position])
        except FileNotFoundError:
            with open('save.txt', 'w+') as save:
                print('File not found, creating new save...')
                position = 1
                save.write(str(position))
        except KeyError:
            with open('save.txt', 'r+') as save:
                print('invalid save value, resetting')
                position = 1
                save.truncate(0)
                save.write(str(position))
        finally:
            return position
    def saveposition(self,position):
        try:
            with open('save.txt', 'r+') as save:
                save.seek(0)
                save.write(str(position))
        except IOError:
            with open('save.txt', 'w+') as save:
                save.truncate(0)
                save.write(str(position))
            

pygame.init()
size: list = [800,600]
screen = pygame.display.set_mode(size)
font_size = screen.get_width() // 20
font = pygame.font.SysFont(None, font_size) # type: ignore
windows = screen.get_rect(center=(800,400))
butwin = screen.get_rect(center=(800,200))
sprites = pygame.sprite.Group() # type: ignore

def txt_size(text):
    if '\n' in text:
        words = [text.split('\n') for text in text.splitlines()]
        h=font.render(text,1,(0,0,0)).get_height()
        x,y= windows.width/2,((windows.height-h*3-100)/2)
        for line in words:
                for word in line:
                    txt = font.render(word, True, (0,255,0))
                    txtRect = txt.get_rect()
                    txtRect.centerx = screen.get_rect().centerx
                    txtRect.centery = screen.get_rect().centery
                    word_width, word_height = txt.get_size()
                    x = (windows.width-word_width)/2
                    screen.blit(txt, (x, y))
                    y += word_height
    else:
        x,y= windows.width/2,(windows.height/(2+(len(text)-1)))
        txt = font.render(text, True, (0,255,0))
        txtRect = txt.get_rect()
        txtRect.centerx = screen.get_rect().centerx
        txtRect.centery = screen.get_rect().centery
        word_width, word_height = txt.get_size()
        x = (windows.width-word_width)/2
        y = (windows.height-word_height-100)/2
        screen.blit(txt, (x,y))

class Button(pygame.sprite.Sprite):
    def __init__(self, color, color_hover, rect, callback, text='', outline=None):
        super().__init__()
        self.text = text
        self.color = color
        tmp_rect = pygame.Rect(0, 0, *rect.size)

        self.org = self._create_image(color, outline, text, tmp_rect)
        self.hov = self._create_image(color_hover, outline, text, tmp_rect)

        self.image = self.org
        self.rect = rect
        self.callback = callback
    def _create_image(self, color, outline, text, rect):
        img = pygame.Surface(rect.size)
        if outline:
            img.fill(outline)
            img.fill(color, rect.inflate(-4, -4))
        else:
            img.fill(color)

        if text != '':
            but_font = pygame.font.SysFont(None, 30)
            words = [text.split('\n') for text in text.splitlines()]
            x,y= rect.width/2,(rect.height/(2+len(words)-1))
            for line in words:
                for word in line:
                    text_surf = but_font.render(word, 1, pygame.Color('black'))
                    word_width, word_height = text_surf.get_size()
                    x = (rect.width-word_width)/2
                    img.blit(text_surf, (x, y))
                    y += word_height
        return img
         
    def update(self, events):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        self.image = self.hov if hit else self.org
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                self.callback(self)


def choice(position):

    current = list(story[position])

    extrabuttons = []
    button_txt = []
    buttons = round(len(current[1:])/2)
    but = 1
    for b in range(buttons):

        current = list(story[position])
            
        
        if (str(current[-but])).isdigit():
            extrabuttons.append(current[-but])
        but += 1

        button_txt.append(current[-buttons-b-1])
    
    screen.fill((0,0,0))
    txt_size(current[0])
    drawsprites(extrabuttons[::-1],button_txt[::-1])
    filesave().saveposition(position)

def spriteadd(posx,text,pos):
    sprites.add(Button(pygame.Color('green'), 
                           pygame.Color('red'), 
                           pygame.Rect(posx, 450, 190, 100), 
                           lambda b: choice(pos),
                           text,
                           pygame.Color('black')))
    
    
def drawsprites(extrabuttons,button_txt):
    sprites.empty()
    select = 0
    splitbut = ((butwin.width)/len(extrabuttons))
    for i in range(len(extrabuttons)):
        select += 1
        posx = (((splitbut-190))/2)+splitbut*(select-1)
        text = button_txt[i]
        pos = extrabuttons[i]
        spriteadd(posx,text,pos)

screen.fill((0,0,0))
position = filesave().retrievesave()
choice(position)
pygame.display.update()

while True:  
    events = pygame.event.get()
    for event in events:
        key = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        
        if event.type == KEYUP:        
            if key[K_ESCAPE]:
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    sprites.update(events)
    sprites.draw(screen)
    pygame.display.update()