import json
from pathlib import Path

import pygame


class Player:
    def __init__(self, x, y, speed, health, size, graphic):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.size = size
        self.graphic = graphic
        self.dir = "down"
        self.running = False
        self.font = pygame.font.SysFont("roboto", 32)

    def draw(self, screen, x):
        if self.running == True:
            if self.dir == "down":
                player_sheet = pygame.image.load(self.graphic + "/Walk/Char_walk_down.png").convert_alpha()
            elif self.dir == "left":
                player_sheet = pygame.image.load(self.graphic + "/Walk/Char_walk_left.png").convert_alpha()
            elif self.dir == "right":
                player_sheet = pygame.image.load(self.graphic + "/Walk/Char_walk_right.png").convert_alpha()
            elif self.dir == "up":
                player_sheet = pygame.image.load(self.graphic + "/Walk/Char_walk_up.png").convert_alpha()
        else:
            if self.dir == "down":
                player_sheet = pygame.image.load(self.graphic + "/Idle/Char_idle_down.png").convert_alpha()
            elif self.dir == "left":
                player_sheet = pygame.image.load(self.graphic + "/Idle/Char_idle_left.png").convert_alpha()
            elif self.dir == "right":
                player_sheet = pygame.image.load(self.graphic + "/Idle/Char_idle_right.png").convert_alpha()
            elif self.dir == "up":
                player_sheet = pygame.image.load(self.graphic + "/Idle/Char_idle_up.png").convert_alpha()

        player_image = player_sheet.subsurface(pygame.Rect(x, 0, 16, 16)).copy()
        screen.blit(player_image,(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def drawstats(self, screen):
        text_surface = self.font.render(f"Health: {self.health}", True, WHITE)
        text_rect = text_surface.get_rect(topleft=(20, 20))
        screen.blit(text_surface, text_rect)

    def relateX(self, x):
        X = x + SCREEN_WIDTH/2 - self.x
        return X
    
    def relateY(self, y):
            Y = y + SCREEN_HEIGHT/2 - self.y
            return Y

    def damage(self, damn):
        self.health -= damn

border = {
    "XLeft": 0,
    "XRight": 3200,
    "YTop": 0,
    "YBottom": 1600,
}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOUR = (32, 168, 32)
WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeons of Dagestan")

clock = pygame.time.Clock()
player = Player(15, border["YBottom"]/2, 5, 100, 32, "maps/Tiny Village Pack/Tiny Adventure Pack/Character/Char_one")


with Path("world_items.json").open(encoding="utf-8") as items_file:
    world_items = json.load(items_file)

item_images = {}
for item_data in world_items.values():
    path = item_data["path"]
    if path not in item_images:
        item_images[path] = pygame.image.load(path).convert_alpha()


def player_collides_with_buildings(x, y):
    player_rect = pygame.Rect(x, y, player.size, player.size)
    return any(
        not item_data.get("walkable", False)
        and
        player_rect.colliderect(
            pygame.Rect(
                item_data["x"],
                item_data["y"],
                item_data["width"],
                item_data["height"],
            )
        )
        for item_data in world_items.values()
    )


running = True
#animation box holders
x = 0
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controlls:
    keys = pygame.key.get_pressed()
    move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * player.speed
    move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * player.speed

    #animations
    if keys[pygame.K_s]:
        player.dir = "down"
        player.running = True
    elif keys[pygame.K_d]:
        player.dir = "right"
        player.running = True
    elif keys[pygame.K_w]:
        player.dir = "up"
        player.running = True
    elif keys[pygame.K_a]:
        player.dir = "left"
        player.running = True

    if not (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
        player.running = False
    

    if not player_collides_with_buildings(player.x + move_x, player.y):
        player.x += move_x
    if not player_collides_with_buildings(player.x, player.y + move_y):
        player.y += move_y

    # Bordering:
    if player.x <= border["XLeft"]:
        player.x = border["XLeft"]
    if player.x >= border["XRight"] - player.size:
        player.x = border["XRight"] - player.size
    if player.y <= border["YTop"]:
        player.y = border["YTop"]
    if player.y >= border["YBottom"] - player.size:
        player.y = border["YBottom"] - player.size

    screen.fill(BG_COLOUR)

    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(400), player.relateY(0), 10, 10))

    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(border["XLeft"]), player.relateY(0), 10, border["YBottom"]))
    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(border["XRight"] - 10), player.relateY(0), 10, border["YBottom"]))
    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(0), player.relateY(border["YTop"]), border["XRight"], 10))
    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(0), player.relateY(border["YBottom"] - 10), border["XRight"], 10))

    for item_name, item_data in world_items.items():
        image = item_images[item_data["path"]]
        position = (player.relateX(item_data["x"]), player.relateY(item_data["y"]))
        screen.blit(image, position)

    player.drawstats(screen)

    # drawing the player
    frame_count += 1
    if frame_count % 10 == 0 and player.running == True:
        x += 16
    if x == 96:
        x = 0
    player.draw(screen, x)

    # frame clean up
    if frame_count % 500 == 0:
        frame_count = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()