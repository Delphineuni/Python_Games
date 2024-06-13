import ctypes, sys
import pygame
from pygame.locals import *

pygame.time.Clock().tick(15)

def layout():
    key = pygame.key.get_pressed()
    # For debugging Windows error codes in the current thread
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    # Made up of 0xAAABBBB, AAA = HKL (handle object) & BBBB = language ID
    klid = user32.GetKeyboardLayout(thread_id)
    # Language ID -> low 10 bits, Sub-language ID -> high 6 bits
    # Extract language ID from KLID
    lid = klid & (2**16 - 1)
    # Convert language ID from decimal to hexadecimal
    lid_hex = hex(lid)
    
    if lid_hex == '0x409':
        layout = 'Azerty'
        DIRECTIONS = [K_z,K_s,K_q,K_d]
        return DIRECTIONS
    elif lid_hex == '0x411':
        layout = 'Qwerty'
        DIRECTIONS = [K_w,K_a,K_s,K_d]
        return DIRECTIONS

def keypressed(x,y,xmov,ymov,DIRECTIONS) -> list:
    for event in pygame.event.get():
        key= pygame.key.get_pressed()
        if event.type == KEYDOWN:
            if key[DIRECTIONS[0]] or key[K_UP]:
                x = 0
                y = -ymov
                return [x,y]
            if key[DIRECTIONS[1]] or key[K_DOWN]:
                x = 0
                y = ymov
                return [x,y]
            if key[DIRECTIONS[2]] or key[K_LEFT]:
                x = -xmov
                y = 0
                return [x,y]
            if key[DIRECTIONS[3]] or key[K_RIGHT]:
                x = xmov
                y = 0
                return [x,y]
        if event.type == QUIT:
            quit()
            sys.exit()

        if key[K_ESCAPE]:
            quit()
            sys.exit()
    return [x,y]
                   
if __name__ == '__main__':
    pygame.init()
    display = pygame.display.set_mode((300, 300))
    DIRECTIONS = layout()
    print(K_ESCAPE)
    while True:
        keypressed(1,1,1,1,DIRECTIONS)