import pygame

class Scene:

    def __init__(self):
        pygame.init()
        self.flags = pygame.FULLSCREEN
        # self.screen = pygame.display.set_mode((1920, 1080), self.flags)
        self.screen = pygame.display.set_mode((900,900))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)

    def display(self):
        self.screen.fill("black")        

        pygame.draw.circle(self.screen, "red", self.player_pos, 40)



        mouse = pygame.mouse.get_pos()
        print(mouse)
        self.player_pos.x = mouse[0]
        self.player_pos.y = mouse[1]

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_q]:
        #     pygame.quit()
        # if keys[pygame.K_w]:
        #     self.player_pos.y -= 300 * self.dt
        # if keys[pygame.K_s]:
        #     self.player_pos.y += 300 * self.dt
        # if keys[pygame.K_a]:
        #     self.player_pos.x -= 300 * self.dt
        # if keys[pygame.K_d]:
        #     self.player_pos.x += 300 * self.dt

        # flip() the display to put your work on screen
        pygame.display.flip()

        self.dt = self.clock.tick(60) / 1000
    
    def loop(self):
        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.display()

            
