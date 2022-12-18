import pygame
from random import randint

class RainingCoins:
    def __init__(self):
        pygame.init()

        # Set display dimensions, framerate, time limit and points limit
        self.width = 640
        self.height = 480
        self.FPS = 60
        self.time_limit = 40
        self.points_limit = 30

        # Loads display and sets window title
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Raining Coins")
        
        # Loads our assets
        self.robot = pygame.image.load("robot.png")
        self.coin = pygame.image.load("coin.png")
        self.monster = pygame.image.load("monster.png")

        # Sets our clock and font for use later
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()

        # Instructions displayed only when starting new instance
        self.first_game()

    def initial_state(self):
        # Robot's initial position, movement speed and points value
        self.p_x = 0
        self.p_y = self.height - self.robot.get_height()
        self.robot_speed = 4
        self.points = 0
        
        self.to_right = False
        self.to_left = False

    def first_game(self):
        # Displays instructions then checks if we want to start a new game or quit
        instructions1 = self.game_font.render(f"Collect {self.points_limit} coins in {self.time_limit} seconds while dodging the monsters!", True, (255, 255, 255))
        instructions2 = self.game_font.render("Use the arrow keys to move.", True, (255, 255, 255))
        instructions3 = self.game_font.render("Press Enter to continue or Esc to exit.", True, (255, 255, 255))
        self.window.blit(instructions1, ((self.width - instructions1.get_width()) / 2, 180))
        self.window.blit(instructions2, ((self.width - instructions2.get_width()) / 2, instructions1.get_height() + 190))
        self.window.blit(instructions3, ((self.width - instructions3.get_width()) / 2, 2 * instructions1.get_height() + 200))

        pygame.display.flip()

        self.restart_check()
    
    def restart_check(self):
        # Checks whether we want to start a new game or quit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.main_loop()
                    if event.key == pygame.K_ESCAPE:
                        exit()
                if event.type == pygame.QUIT:
                    exit()
        
    def main_loop(self):
        # Sets robot's initial position
        self.initial_state()

        # Sets timer
        self.timer = 0

        # Generates random arrays for our monsters and coins to spawn, fewer monsters than coins
        self.coins = self.rand_list(5)
        self.monsters = self.rand_list(3)
        
        # Do the following constantly
        while True:
            self.check_events()
            self.move()
            self.draw_window()
            self.spawn_items(self.coin, self.coins, 4)
            self.spawn_items(self.monster, self.monsters, 6)
            if self.points >= self.points_limit:
                self.win()
            if self.timer >= self.time_limit:
                self.fail()

    def check_events(self):    
        # Checks for movement and updates states as necessary, also allows exiting at any point
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_ESCAPE:
                        exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False

            if event.type == pygame.QUIT:
                exit()

    def move(self):
        # Moves robot as requested at given speed within bounds of window
        if self.to_right:
            if self.p_x < self.width - self.robot.get_width():
                self.p_x += self.robot_speed
        if self.to_left:
            if self.p_x > 0:
                self.p_x -= self.robot_speed

    def rand_list(self, count: int):
        # Creates an array of 'raining' items of given size
        array = []
        for i in range(count):
            array.append([-1000, self.height])
        return array
    
    def spawn_items(self, item: pygame.Surface, items: list, speed: float):
        # Spawns items from the array at random locations and moves them at given speed
        for i in range(len(items)):
            if items[i][1] + item.get_height() < self.width:
                items[i][1] += speed
            else:
                if items[i][0] < - item.get_width() or items[i][0] > self.width:
                    items[i][0] = randint(0,self.width - item.get_width())
                    items[i][1] = - randint(100, 1000)
                elif items[i][0] + item.get_width() < self.width:
                    items[i][0] -= speed
                else:
                    items[i][0] += speed
    
    def draw_items(self, item: pygame.Surface, items: list):
        # Draws items and checks for collisions, updates values as needed
        for i in range(len(items)):
            self.window.blit(item, (items[i][0], items[i][1]))
            if (self.p_x <= items[i][0] + item.get_width() / 2 <= (self.robot.get_width() + self.p_x) 
                and self.p_y <= (items[i][1] + item.get_height() / 2) <= self.p_y + self.robot.get_height()):
                if item == self.coin:
                    self.coins[i] = [-1000, self.height]
                    self.points += 1
                else:
                    self.fail()
            if items[i][1] > self.height and items[i][0] > 0:
                items[i] = [-1000, self.height]

    def draw_window(self):
        # Draws our robot, calls item functions, updates timer then updates the screen
        self.window.fill((13, 194, 255))

        self.draw_items(self.coin, self.coins)
        self.window.blit(self.robot, (self.p_x, self.p_y))
        self.draw_items(self.monster, self.monsters)
            
        self.points_text = self.game_font.render(f"Points: {self.points}", True, (255, 0, 0))
        self.window.blit(self.points_text, (self.width - self.points_text.get_width() - 20, 0))
        self.timer_text = self.game_font.render(f"Time: {self.timer:.3f}", True, (255, 0, 0))
        self.window.blit(self.timer_text, (20, 0))
        pygame.display.flip()

        self.timer += 1/self.FPS
    
        self.clock.tick(self.FPS)

    def fail(self):
        # Displays failure message then allows restart
        if self.timer >= self.time_limit:
            message1 = self.game_font.render("Unfortunately you were slightly too slow!", True, (0, 0, 0))
        else:
            message1 = self.game_font.render("Unfortunately you were hit by a monster!", True, (0, 0, 0))
        message2 = self.game_font.render("Press Enter to try again or Esc to exit.", True, (0, 0, 0))

        pygame.draw.rect(self.window, (255, 0, 0), ((self.width - message1.get_width()) / 2 - 10, 170, message1.get_width() + 20, 3 * message1.get_height() + 10))
        self.window.blit(message1, ((self.width - message1.get_width()) / 2, 180))
        self.window.blit(message2, ((self.width - message2.get_width()) / 2, message1.get_height() + 190))

        pygame.display.flip()

        self.restart_check()

    def win(self):
        # Displays victory message then allows restart
        message1 = self.game_font.render("Congratulations! You won!", True, (0, 0, 0))
        message2 = self.game_font.render(f"Your time was {self.timer:.3f} s.", True, (0, 0, 0))
        message3 = self.game_font.render("Press Enter to see if you can beat it or Esc to exit.", True, (0, 0, 0))

        pygame.draw.rect(self.window, (0, 255, 0), ((self.width - message3.get_width()) / 2 - 10, 170, message3.get_width() + 20, 4 * message3.get_height() + 10))
        self.window.blit(message1, ((self.width - message1.get_width()) / 2, 180))
        self.window.blit(message2, ((self.width - message2.get_width()) / 2, message1.get_height() + 187))
        self.window.blit(message3, ((self.width - message3.get_width()) / 2, message2.get_height() + 220))

        pygame.display.flip()
        
        self.restart_check()


if __name__ == "__main__":
    RainingCoins()