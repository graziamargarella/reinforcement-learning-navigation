import pygame
import random
import numpy as np
from collections import namedtuple

# Global Parameters
framerate = 60
windowWidth = 850
windowHight = 850
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
        self.robot = Point(self.dimensionX // (2 * self.dimension_image), self.dimensionY // (2 * self.dimension_image))
        self.obstacles = []
        self.target = Point(0, 0)
        self.score = 0
        self.reward = 0
        self.total_reward = 0
        self.game_over = False

        # Init the Window
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
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

        # Set the score label
        self.label_score = self.font.render("Score : " + str(self.score), True, "White")
        self.screen.blit(self.label_score, [0, 0])

        # Set Background,Clock and update interface
        self.screen.blit(self.image_background, (0, 0))
        self._place_something(food=True)
        self.clock = pygame.time.Clock()
        pygame.display.update()

    # Random Generator of Coordinates
    def _random_generator_coordinates(self):
        x = random.randint(0, (self.dimensionX // self.dimension_image) - 1)
        y = random.randint(0, (self.dimensionY // self.dimension_image) - 1)
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
    def _place_something(self, food):
        x, y = self._random_generator_coordinates()
        tmp = Point(x, y)
        while tmp in self.obstacles or tmp == self.robot or tmp == self.target or self._out_of_borders(tmp):
            x, y = self._random_generator_coordinates()
            tmp = Point(x, y)
        if food:
            self.target = tmp
        else:
            self.obstacles.append(tmp)

    # Redraw the interface with new positions
    def _redraw_interface(self):
        # BackGround
        self.screen.blit(self.image_background, (0, 0))
        # Obstacles
        for obs in self.obstacles:
            self.screen.blit(self.image_furniture, (obs.x * self.dimension_image, obs.y * self.dimension_image))
        # Target
        self.screen.blit(self.image_target,
                         (self.target.x * self.dimension_image, self.target.y * self.dimension_image))
        # Robot
        self.screen.blit(self.image_robot, (self.robot.x * self.dimension_image, self.robot.y * self.dimension_image))
        # Score Label
        self.label_score = self.font.render("Score : " + str(self.score)
                                            # + " Total Reward : " + str(self.total_reward),
                                            , True, "White")
        self.screen.blit(self.label_score, [0, 0])
        # Update the Window
        pygame.display.update()

    # Checks if the robot goes out of the borders
    def _out_of_borders(self, new_pos):
        if new_pos.x < 0 or new_pos.y < 0:
            return True
        if new_pos.x >= self.dimensionX // self.dimension_image or new_pos.y >= self.dimensionY // self.dimension_image:
            return True
        return False

    # Checks if the robot hit an obstacle
    def _hit_obstacle(self, new_pos):
        if new_pos in self.obstacles:
            return True
        return False

    # Checks if the robot take a target
    def _hit_target(self, new_pos):
        if new_pos == self.target:
            return True
        return False

    # Called to move the target in a direction
    # Movement is an array composed by [Up, Left, Right, Down]
    def _move_target(self, movement):
        position = self.robot
        finish_game = True
        new_pos = None
        if np.array_equal(movement, [1, 0, 0, 0]):
            new_pos = Point(position.x, position.y - 1)
        elif np.array_equal(movement, [0, 1, 0, 0]):
            new_pos = Point(position.x - 1, position.y)
        elif np.array_equal(movement, [0, 0, 1, 0]):
            new_pos = Point(position.x + 1, position.y)
        elif np.array_equal(movement, [0, 0, 0, 1]):
            new_pos = Point(position.x, position.y + 1)
        if new_pos is None or self._out_of_borders(new_pos):
            self.reward = -10
        elif self._hit_obstacle(new_pos):
            self.reward = -10
        elif self._hit_target(new_pos):
            self.reward = 10000
            self.score = self.score + 1
            finish_game = False
        else:
            self.reward = -0.5
            finish_game = False
        if finish_game:
            self.game_over = finish_game
        else:
            self.robot = new_pos

    # Called Every time to reset position of the robot, score, obstacles and number of targets acquired
    def _reset(self):
        self.robot = Point(self.dimensionX // (2 * self.dimension_image), self.dimensionY // (2 * self.dimension_image))
        self.obstacles = []
        self._place_something(food=True)
        self.score = 0
        self.total_reward = 0
        self.game_over = False
        self.screen.blit(self.image_background, (0, 0))

    # Place a number n of obstacle in the environment
    def place_n_obstacles(self, n):
        for i in range(0, n):
            self._place_something(food=False)

    # Return True if has a obstacle or a border
    def obstacle_or_border(self, new_pos):
        if new_pos in self.obstacles:
            return True
        elif self._out_of_borders(new_pos):
            return True
        return False

    # Return the observations for the agent
    # Composed by [TargetUp, TargetLeft, TargetRight, TargetDown, ObstacleUp, ObstacleLeft, ObstacleRight, ObstacleDown]
    def get_observations(self):
        vertical = 0
        if self.robot.y > self.target.y:
            vertical = 1
        elif self.robot.y < self.target.y:
            vertical = 2
        horizontal = 0
        if self.robot.x > self.target.x:
            horizontal = 1
        elif self.robot.x < self.target.x:
            horizontal = 2
        up = Point(self.robot.x, self.robot.y - 1)
        down = Point(self.robot.x, self.robot.y + 1)
        left = Point(self.robot.x - 1, self.robot.y)
        right = Point(self.robot.x + 1, self.robot.y)
        obs = (vertical, horizontal, self._hit_obstacle(up), self._hit_obstacle(left), self._hit_obstacle(right),
               self._hit_obstacle(down))
        return obs

    # Update the robot position given a movement and eventually reset the game. 
    # Returns the reward obtained, the status of the agent, if the environment has been reset and the total reward and score values
    def execute_a_step(self, movement):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self._move_target(movement)
        self.total_reward = self.total_reward + self.reward
        finish = False
        tot = self.total_reward
        score = self.score
        if self.game_over:
            finish = True
            self._reset()
        if self._hit_target(self.robot):
            self.place_n_obstacles(1)
            self._place_something(food=True)
        self._redraw_interface()
        self.clock.tick(framerate)
        return self.reward, self.get_observations(), finish, tot, score

    # Test Method to see how it works
    def execute(self):
        while True:
            movement = [1, 0, 0, 0]
            self.execute_a_step(movement)
            movement = [0, 1, 0, 0]
            self.execute_a_step(movement)
            movement = [0, 0, 1, 0]
            self.execute_a_step(movement)
            movement = [0, 0, 0, 1]
            self.execute_a_step(movement)

"""
if __name__ == "__main__":
    env = Enviroment()
    env.execute()
"""