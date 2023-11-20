import pygame
from pygame import QUIT

# Global Parameters
windowWidth = 800
windowHight = 800
imageDimension = 50
imageRobotPath = "images/robot.png"
imageObstaclePath = "images/armchair.png"
imageTargetPath = "images/stain.png"
imageBackgroundPath = "images/parquet.png"


class Enviroment:

    def __init__(self):
        self.dimensionX = windowHight
        self.dimensionY = windowWidth
        self.dimension_image = imageDimension

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

    def execute(self):
        run = True
        while run:
            self.screen.blit(self.image_background, (0, 0))
            self.screen.blit(self.image_robot, (100, 100))
            self.screen.blit(self.image_furniture, (300, 300))
            self.screen.blit(self.image_target, (500, 500))
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    env = Enviroment()
    env.execute()
