import pygame, random, input
from time import sleep

pygame.init()
fps = pygame.time.Clock()

WIDTH: int = 800
HEIGHT: int = 600
directions = input.layout()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
player_length = 1
playerblock = 30
def playerlen(playerblock, player_list):
    for x in player_list:
        pygame.draw.rect(screen,(0,255,0),[x[0], x[1],playerblock,playerblock])
player_list = []
run: bool = True
gotapple = True
apple = pygame.Rect((100,100,40,40))

snake_body = [  [100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
            ]
snake_position = [100, 50]    
x = WIDTH / 2
y = HEIGHT / 2

x_change = 0
y_change = 0
xy= [WIDTH / 2,HEIGHT / 2]

while run:
    
    screen.fill((0,0,0))
    
    if gotapple:
        appx, appy = random.randint(0,WIDTH-40),random.randint(0,HEIGHT-40)
        apple.update(appx,appy,20,20)
        gotapple = False
      
    pygame.draw.rect(screen, (255,0,0), apple)

    if x >= 0 or (x + 30) < WIDTH or y >= 0 or (y + 30) < HEIGHT:
        x_change,y_change = xy = input.keypressed(x_change, y_change, playerblock, playerblock, directions)

    x += x_change
    y += y_change

    snake_Head = []
    snake_Head.append(x)
    snake_Head.append(y)
    player_list.append(snake_Head)
    if len(player_list) > player_length:
            del player_list[0]
    
    if snake_Head in player_list[:-1]:
        break
    
    if x < 0 or y < 0 or x > WIDTH or y > HEIGHT:
        break
    
    playerlen(playerblock,player_list)
    
    
    if apple.clip(x, y,playerblock,playerblock):
        gotapple = True
        player_length += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        
    pygame.display.update()
    fps.tick(5)
pygame.font.init()
font = pygame.font.SysFont('Helvetica',100)
txt = "You Lost!"
msg = font.render(txt, True, (255,0,0))
width, height = font.size(txt)
xoffset = (WIDTH-width) // 2
yoffset = (HEIGHT-height) // 2
coords = xoffset, yoffset
screen.blit(msg,coords)
pygame.display.update()
sleep(3)
    
pygame.QUIT