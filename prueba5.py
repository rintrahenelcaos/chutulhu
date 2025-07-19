# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
import pygame
import sys
import itertools
from constants import GENERIC_FONT


def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh

def wordwarp(font, text, width):
    lines = []
    x = 0
    w = len(text)

    while x < w:
        while font.size(text[x:w])[0] > width:
            w -= 1

        if w != len(text):
            while text[w] != " ":
                w -= 1

        lines.append(text[x:w].strip())
        x = w
        w = len(text)

    return lines 

def text_wrapper(text, font, width, screen, colour): 
    textlines = []
    for line in wordwarp(font, text, width):
        textlines.append(font.render(line, True, colour))
        
    y = itertools.count(30, font.get_linesize())
    for line in textlines:
        screen.blit(line, (15, next(y)))

def main():
    pygame.init()
    # print(sorted(pygame.font.get_fonts()))
    screen = pygame.display.set_mode((500, 480))
    pygame.display.init()
    
    textual = "test card descriptio to check line width identation and the rest"
    
    #renderTextCenteredAt(textual, GENERIC_FONT, "red", 200, 0, screen, 100)
    text_wrapper(textual, GENERIC_FONT, 150, screen, "red")
    
    
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
                
                
if __name__ == "__main__":
    main()