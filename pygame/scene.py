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
        current_directory = os.path.dirname(__file__)
        images_directory = os.path.join(current_directory, "images")
        self.image_dict = load_images(images_directory)
        # self.screen = pygame.display.set_mode((1920, 1080), self.flags)
        self.screen = pygame.display.set_mode((1920, 1090))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.font = pygame.font.Font(None, 34)

        self.player_pos = pygame.Vector2(
            self.screen.get_width() / 2, self.screen.get_height() / 2
        )

    def display(self, landmarks):
        self.screen.fill("black")
        
        left_shoulder = landmarks.get("left_shoulder")
        right_shoulder = landmarks.get("right_shoulder")
        left_hip = landmarks.get("left_hip")
        right_hip = landmarks.get("right_hip")
        
        image_to_draw = self.image_dict.get("google")
        
        if left_shoulder and right_shoulder and left_hip and right_hip:
            
            center_x = (left_shoulder[0] + right_shoulder[0] + left_hip[0] + right_hip[0])
            center_y = (left_shoulder[1] + right_shoulder[1] + left_hip[1] + right_hip[1])
            
            pygame.draw.circle(self.screen, (0, 255, 0), (center_x, center_y), 10)
            
            
        if image_to_draw is not None:
            
            image_rect = image_to_draw.get_rect()
            image_x = center_x - image_rect.width // 2
            image_y = center_y - image_rect.height // 2
            
            self.screen.blit(image_to_draw, (image_x, image_y))

        if landmarks:
            for landmark in landmarks:
                xPos, yPos = landmarks[landmark]

                xPos = int(xPos)
                yPos = int(yPos)
                
                # print(f"x coordinate = {xPos}\n y coordinate = {yPos}")
                pygame.draw.circle(self.screen, (255, 0, 0), (xPos, yPos), 20)

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

            self.display(landmarks)
