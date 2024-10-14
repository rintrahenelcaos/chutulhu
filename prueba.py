import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(surface.get_width() / 2, surface.get_height() / 2)

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

class Game():
    def __init__(self, surface) -> None:
        self.surface = surface
    def start_the_game(self):
        running = True
        while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the surface with a color to wipe away anything from last frame
            self.surface.fill("purple")

            pygame.draw.circle(self.surface, "red", player_pos, 40)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player_pos.y -= 300 * dt
            if keys[pygame.K_s]:
                player_pos.y += 300 * dt
            if keys[pygame.K_a]:
                player_pos.x -= 300 * dt
            if keys[pygame.K_d]:
                player_pos.x += 300 * dt

            # flip() the display to put your work on surface
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000

        pygame.quit()
        
    
def start_the_game():
    pass
def start_game2():
    game = Game(surface)
    game.start_the_game()

menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)