import pygame
import os
from open_cv import open_cv_camera


def load_images(path_to_directory):
    image_dict = {}
    for filename in os.listdir(path_to_directory):
        if filename.endswith(".png"):
            path = os.path.join(path_to_directory, filename)
            key = filename[:-4]
            image_dict[key] = pygame.image.load(path).convert()
    return image_dict


class Scene:

    def __init__(self):
        pygame.init()
        self.flags = pygame.FULLSCREEN
        # self.screen = pygame.display.set_mode((1920, 1080), self.flags)
        self.screen = pygame.display.set_mode((1920, 1090))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.font = pygame.font.Font(None, 34)

        self.player_pos = pygame.Vector2(
            self.screen.get_width() / 2, self.screen.get_height() / 2
        )

    def display(self, xPos, yPos):
        self.screen.fill("black")

        text_surface = self.font.render(
            f"x coordinate = {xPos}\n y coordinate = {yPos}", True, (0, 0, 0)
        )
        xPos = int(xPos)
        yPos = int(yPos)

        # print(f"x coordinate = {xPos}\n y coordinate = {yPos}")
        pygame.draw.circle(self.screen, (255, 0, 0), (xPos, yPos), 20)
        self.screen.blit(text_surface, (0, 0))

        # flip() the display to put your work on screen
        pygame.display.flip()

        self.dt = self.clock.tick(60) / 1000

    def loop(self):

        cv_obj = open_cv_camera()

        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            landmarks = cv_obj.get_body_landmarks(show_video_frame=True)

            x_left_shoulder, y_left_shoulder = landmarks["left_shoulder"]

            self.display(x_left_shoulder, y_left_shoulder)
