import pygame
import random
from pygame import QUIT
from collections import namedtuple

# Global Parameters
windowWidth = 800
windowHight = 800
imageDimension = 50
imageRobotPath = "images/robot.png"
imageObstaclePath = "images/armchair.png"
imageTargetPath = "images/stain.png"
imageBackgroundPath = "images/parquet.png"

Point = namedtuple('Point', 'x, y')
Point.__eq__ = lambda a, b: a.x == b.x and a.y == b.y


class Enviroment:

    def __init__(self):
        self.dimensionX = windowHight
        self.dimensionY = windowWidth
        self.dimension_image = imageDimension
        self.robot = Point(self.dimensionX / 100, self.dimensionY / 100)
        self.obstacles = []
        self.target = Point(0, 0)

        # Init the Window
        pygame.init()
        self.screen = pygame.display.set_mode((self.dimensionX, self.dimensionY))
        pygame.display.set_caption("Robot Navigation")

        # Load Images
        self.image_background = pygame.image.load(imageBackgroundPath)
        self.image_robot = pygame.image.load(imageRobotPath)
        self.image_furniture = pygame.image.load(imageObstaclePath)
        self.image_target = pygame.image.load(imageTargetPath)

        # Resize Images
        self.image_background = pygame.transform.scale(self.image_background, (self.dimensionX, self.dimensionY))
        self.image_robot = pygame.transform.scale(self.image_robot, (self.dimension_image, self.dimension_image))
        self.image_furniture = pygame.transform.scale(self.image_furniture,
                                                      (self.dimension_image, self.dimension_image))
        self.image_target = pygame.transform.scale(self.image_target, (self.dimension_image, self.dimension_image))

        # Set Clock and update interface
        self.clock = pygame.time.Clock()
        pygame.display.flip()

    # Random Generator of Coordinates
    def _random_generator_coordinates(self):
        x = random.randint(0, (self.dimensionX // self.dimension_image))
        y = random.randint(0, (self.dimensionY // self.dimension_image))
        return x, y

    # Return true if the target is surrounded by 4 walls (Does not check every possible unreachability)
    def _check_surrounded(self, food, point):
        if not food:
            return False
        x = point.x
        y = point.y
        p1 = Point(x, y + 1)
        p2 = Point(x, y - 1)
        p3 = Point(x - 1, y)
        p4 = Point(x + 1, y)
        if p1 in self.obstacles and p2 in self.obstacles and p3 in self.obstacles and p4 in self.obstacles:
            return True
        return False

    # Method which create an obstacle or a target (depends on boolean value in parameters) in the enviroment
    # CAN BE IMPROVED WITH A CHECK IF I CANT PLACE ANYWHERE TODO
    def _place_something(self, food):
        x, y = self._random_generator_coordinates()
        tmp = Point(x, y)
        while tmp in self.obstacles or tmp == self.robot or tmp == self.target:
            x, y = self._random_generator_coordinates()
            tmp = Point(x, y)
        if food:
            self.target = tmp
        else:
            self.obstacles.append(tmp)

    def _redraw_interface(self):
        for obs in self.obstacles:
            self.screen.blit(self.image_furniture, (obs.x * self.dimension_image, obs.y * self.dimension_image))
        self.screen.blit(self.image_target,
                         (self.target.x * self.dimension_image, self.target.y * self.dimension_image))
        self.screen.blit(self.image_robot, (self.robot.x * self.dimension_image, self.robot.y * self.dimension_image))
        pygame.display.update()

    # Called Every time to reset position of the robot, score, obstacles and number of targets acquired
    def reset(self):
        self.robot = Point(self.dimensionX // 2, self.dimensionY // 2)
        self.obstacles = []
        self.target = Point(0, 0)

    # Execution Method to show the window and start the simulation
    def execute(self):
        run = True
        c = 0
        while run:
            self.screen.blit(self.image_background, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
            if c < 10:
                self._place_something(False)
                c = c + 1
            self._redraw_interface()

        pygame.quit()


if __name__ == "__main__":
    env = Enviroment()
    env.execute()
