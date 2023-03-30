import pygame
import random

# Set up the screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


pygame.display.set_caption("Dungoon")

TILE_SIZE = 16

# Tile types
WALL = 0
FLOOR = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Dungeon:
#------------------------------------------------------------------------------------------------------------ INITIATE
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[WALL for y in range(height)] for x in range(width)]
#------------------------------------------------------------------------------------------------------------ GENERATE
    def generate(self):
        cx = self.width // 2
        cy = self.height // 2
        room_width = random.randint(5, 10)
        room_height = random.randint(5, 10)
        room_x = cx - room_width // 2
        room_y = cy - room_height // 2
        self.create_room(room_x, room_y, room_width, room_height)

        # Add more rooms and corridors |range(), creates distance|
        for i in range(20):
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            length = random.randint(3, 10)
            x, y = cx, cy
            for j in range(length):
                x += direction[0]
                y += direction[1]
                if x < 1 or x >= self.width - 1 or y < 1 or y >= self.height - 1:
                    print("why?")
                    break
                if self.tiles[x][y] == FLOOR:
                    print("l")
                    break
                else:    
                    self.create_room(x, y, 3, 3)
                    self.create_corridor(cx, cy, x, y)
#------------------------------------------------------------------------------------------------------------ DRAW IT
    def draw(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y] == WALL:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(surface, BLACK, rect)
                else:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(surface, WHITE, rect)
#------------------------------------------------------------------------------------------------------------ ROOM
    def create_room(self, x1, y1, x2, y2):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.tiles[x][y] = FLOOR
#------------------------------------------------------------------------------------------------------------ CORRIDOR
    def create_corridor(self, cx, cy, x, y):
        # choose a random tile type for the corridor ↑, →, or ↳
        tile_type = random.choice([FLOOR, WALL])

        # create a horizontal or vertical corridor, depending on the postitions given (to your mom)
        if cx == x:
            # vertical corridor ↑
            start_y, end_y = sorted([cy, y])
            for y in range(start_y, end_y + 1):
                self.tiles[cx][y] = tile_type
        elif cy == y:
            # horizontal corridor →
            start_x, end_x = sorted([cx, x])
            for x in range(start_x, end_x + 1):
                self.tiles[x][cy] = tile_type
        else:
            # L-shaped corridor ↳
            self.create_corridor(cx, cy, x, cy)
            self.create_corridor(x, cy, x, y)
#------------------------------------------------------------------------------------------------------------



#______CREATE DUNGEON_____
dungeon = Dungeon(20, 15)
dungeon.generate()

#______LOOP_______
while True:
    # QUIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Start Drawing...
    screen.fill(BLACK)

    # Draw the dungeon
    dungeon.draw(screen)

    # FLIPPER
    pygame.display.flip()