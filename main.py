import pygame
import random

# Stuff
WIDTH, HEIGHT = 800, 800
FPS = 144
WHITE = 255, 255, 255
ROCK = 255, 0, 0
PAPER = 0, 255, 0
SCISSORS = 0, 0, 255
count = 4
random_movement = 10
object_count = 100


# Class
class RPS:
    def __init__(self, start_pos):
        self.current_pos = start_pos
        self.rect = pygame.rect.Rect(start_pos[0], start_pos[1], 16, 16)
        self.type = {1: ROCK, 2: PAPER, 3: SCISSORS}.get(random.randint(1, 3))
        self.weight_vector = (0, 0)
        self.nearby = []
        self.nearby_coords = []

    def check_rock(self):
        if self.type == ROCK:
            for i in objects:
                if i.type == SCISSORS:
                    self.nearby_coords.append((i.rect.x, i.rect.y))
                    self.nearby.append(abs((self.rect.x - i.rect.x) ** 2 + (self.rect.y - i.rect.y) ** 2) ** 0.5)
        else:
            self.weight_vector = (0, 0)

    def check_scissors(self):
        if self.type == SCISSORS:
            for i in objects:
                if i.type == PAPER:
                    self.nearby_coords.append((i.rect.x, i.rect.y))
                    self.nearby.append(abs((self.rect.x - i.rect.x) ** 2 + (self.rect.y - i.rect.y) ** 2) ** 0.5)
        else:
            self.weight_vector = (0, 0)

    def check_paper(self):
        if self.type == PAPER:
            for i in objects:
                if i.type == ROCK:
                    self.nearby_coords.append((i.rect.x, i.rect.y))
                    self.nearby.append(abs((self.rect.x - i.rect.x) ** 2 + (self.rect.y - i.rect.y) ** 2) ** 0.5)
        else:
            self.weight_vector = (0, 0)

    def move_rectangle(self):
        if not count % 5:
            self.nearby = []
            self.nearby_coords = []
            # Find enemies and move and calculate direction
            self.check_rock()
            self.check_paper()
            self.check_scissors()

            if self.nearby:
                weight_x = self.nearby_coords[self.nearby.index(min(self.nearby))][0] - self.rect.x
                weight_y = self.nearby_coords[self.nearby.index(min(self.nearby))][1] - self.rect.y
                self.weight_vector = pygame.math.Vector2(weight_x, weight_y)
                try:
                    self.weight_vector = pygame.math.Vector2.normalize(self.weight_vector)
                except ValueError:
                    self.weight_vector = (0, 0)

        # Move the rectangles
        move_x, move_y = random.randint(random_movement*-1, random_movement) + self.weight_vector[0], random.randint(random_movement*-1, random_movement) + self.weight_vector[1]
        self.rect.move_ip(move_x, move_y)
        if self.rect.x < 0 or self.rect.x > 784 or self.rect.y < 0 or self.rect.y > 784:
            self.rect.move_ip(move_x*-1, move_y*-1)

    def check_collisions(self):
        for i in objects:
            if pygame.Rect.colliderect(i.rect, self.rect) and i.rect != self.rect:
                if self.type == {ROCK: SCISSORS, SCISSORS: PAPER, PAPER: ROCK}.get(i.type):
                    self.type = i.type

    def draw_rectangle(self):
        pygame.draw.rect(screen, self.type, self.rect)


# Setup
pygame.init()
pygame.display.set_caption("Rock, Paper, Scissors")  # The title of the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Makes game window

objects = []
for i in range(object_count):
    objects.append(RPS((random.randint(0, 784), random.randint(0, 784))))


# Main loop
def main():
    global count
    # Variables
    run = True
    clock = pygame.time.Clock()

    # Game loop
    while run:
        # Gets input
        for event in pygame.event.get():
            # Closes game when told to
            if event.type == pygame.QUIT:
                run = False

        screen.fill(WHITE)
        # Logic
        count += 1
        for rect in objects:
            rect.move_rectangle()
        for rect in objects:
            rect.check_collisions()
        for rect in objects:
            rect.draw_rectangle()

        # Update screen
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
