import pygame
import os
from open_cv import open_cv_camera
import math


def load_images(path_to_directory):
    image_dict = {}
    for filename in os.listdir(path_to_directory):
        if filename.endswith(".png"):
            path = os.path.join(path_to_directory, filename)
            key = filename[:-4]
            image_dict[key] = pygame.image.load(path)
    return image_dict


class Scene:

    def __init__(self):
        pygame.init()
        self.flags = pygame.FULLSCREEN
        current_directory = os.path.dirname(__file__)
        images_directory = os.path.join(current_directory, "images")

        self.image_dict = load_images(images_directory)
        print(self.image_dict)
        self.screen = pygame.display.set_mode((1920, 1090))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.font = pygame.font.Font(None, 34)

        self.player_pos = pygame.Vector2(
            self.screen.get_width() / 2, self.screen.get_height() / 2
        )

    def area_of_quadrilateral(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # Calculate the area of triangle 1
        area_triangle1 = 0.5 * abs(
            (x1 * y2 + x2 * y3 + x3 * y1) - (y1 * x2 + y2 * x3 + y3 * x1)
        )

        # Calculate the area of triangle 2
        area_triangle2 = 0.5 * abs(
            (x1 * y4 + x4 * y3 + x3 * y1) - (y1 * x4 + y4 * x3 + y3 * x1)
        )

        # Total area of the quadrilateral
        total_area = area_triangle1 + area_triangle2

        return total_area

    def angle_of_legs(self, x1, y1, x2, y2):
        angle = 0
        if x1 != x2:
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        return angle

    def display(self, landmarks):
        self.screen.fill("black")

        left_shoulder = landmarks.get("left_shoulder")
        right_shoulder = landmarks.get("right_shoulder")
        left_hip = landmarks.get("left_hip")
        right_hip = landmarks.get("right_hip")
        left_ankle = landmarks.get("left_ankle")
        right_ankle = landmarks.get("right_ankle")

        chest_image = self.image_dict.get("instagram")
        leg_image = self.image_dict.get("google")

        center_x, center_y = 0, 0
        area_of_chest = 200
        if (left_shoulder and right_shoulder and left_hip and right_hip) and (
            left_shoulder[0] < 1920
            and left_shoulder[1] < 1080
            and right_shoulder[0] < 1920
            and right_shoulder[1] < 1080
            and left_hip[0] < 1920
            and left_hip[1] < 1080
            and right_hip[0] < 1920
            and right_hip[1] < 1080
        ):

            print(f"left_shoulder = {left_shoulder}")
            print(f"right_shoulder = {right_shoulder}")
            center_x = (
                ((left_shoulder[0] + right_shoulder[0]) // 2)
                + ((left_hip[0] + right_hip[0]) // 2)
            ) // 2
            center_y = (
                ((left_shoulder[1] + right_shoulder[1]) // 2)
                + ((left_hip[1] + right_hip[1]) // 2)
            ) // 2

            area_of_chest = self.area_of_quadrilateral(
                left_shoulder[0],
                left_shoulder[1],
                right_shoulder[0],
                right_shoulder[1],
                left_hip[0],
                left_hip[1],
                right_hip[0],
                right_hip[1],
            )

        if (left_ankle and right_ankle) and (
            (
                left_ankle[0] < 1920
                and left_ankle[1] < 1080
                and right_ankle[0] < 1920
                and right_ankle[1] < 1080
            )
            and (leg_image)
        ):

            angle_left_leg = (
                self.angle_of_legs(
                    left_hip[0], left_hip[1], left_ankle[0], left_ankle[1]
                )
                * -1
            )
            angle_right_leg = (
                self.angle_of_legs(
                    right_hip[0], right_hip[1], right_ankle[0], right_ankle[1]
                )
                * -1
            )

            left_leg_length = math.sqrt(
                (left_hip[0] - left_ankle[0]) ** 2 + (left_hip[1] - left_ankle[1]) ** 2
            )

            right_leg_length = math.sqrt(
                (right_hip[0] - right_ankle[0]) ** 2
                + (right_hip[1] - right_ankle[1]) ** 2
            )

            og_width, og_height = (
                leg_image.get_rect().width,
                leg_image.get_rect().height,
            )

            left_scale_factor = left_leg_length / og_width
            right_scale_factor = right_leg_length / og_width

            scaled_left_leg = pygame.transform.scale(
                leg_image,
                (
                    int(og_width * left_scale_factor),
                    int(og_height * left_scale_factor),
                ),
            )

            scaled_right_leg = pygame.transform.scale(
                leg_image,
                (
                    int(og_width * right_scale_factor),
                    int(og_height * right_scale_factor),
                ),
            )

            scaled_left_leg = pygame.transform.rotate(scaled_left_leg, angle_left_leg)
            scaled_right_leg = pygame.transform.rotate(
                scaled_right_leg, angle_right_leg
            )

            self.screen.blit(scaled_left_leg, (left_hip[0], left_hip[1]))
            self.screen.blit(scaled_right_leg, (right_hip[0], right_hip[1]))

        pygame.draw.circle(self.screen, (0, 255, 0), (center_x, center_y), 10)

        if chest_image:
            image_rect = chest_image.get_rect()
            image_area = image_rect.width * image_rect.height
            scaling_factor = (area_of_chest / image_area) ** 0.5
            scaled_image = pygame.transform.scale(
                chest_image,
                (
                    int(image_rect.width * scaling_factor),
                    int(image_rect.height * scaling_factor),
                ),
            )
            image_x = center_x - scaled_image.get_rect().width // 2
            image_y = center_y - scaled_image.get_rect().height // 2
            self.screen.blit(scaled_image, (image_x, image_y))

        if landmarks:
            for landmark in landmarks:
                xPos, yPos = landmarks[landmark]

                xPos = int(xPos)
                yPos = int(yPos)

                # print(f"x coordinate = {xPos}\n y coordinate = {yPos}")
                pygame.draw.circle(self.screen, (255, 0, 255), (xPos, yPos), 20)

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
