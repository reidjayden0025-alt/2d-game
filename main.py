import json
from pathlib import Path

import pygame


class Player:
    def __init__(self, x, y, speed, health, size, graphic):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.gold = 0
        self.level = 0
        self.xp = 0
        self.size = size
        self.graphic = graphic
        self.dir = "down"
        self.running = False
        self.attacking = False
        self.attack_frame = 0
        self.attack_timer = 0
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.damn = False
        self.ching = False
        self.chong = False
        self.font = pygame.font.SysFont("roboto", 32)

        self.animation_sheets = { # dont get confused looking at this, it's only 3 nested dictionairies that initialise animated images by themselves
            "idle": {
                direction: pygame.image.load(f"{graphic}/Idle/Char_idle_{direction}.png").convert_alpha()
                for direction in ("down", "left", "right", "up")
            },
            "walk": {
                direction: pygame.image.load(f"{graphic}/Walk/Char_walk_{direction}.png").convert_alpha()
                for direction in ("down", "left", "right", "up")
            },
            "attack": {
                direction: pygame.image.load(f"{graphic}/Attack/Char_atk_{direction}.png").convert_alpha()
                for direction in ("down", "left", "right", "up")
            },
        }

    def draw(self, screen, walk_frame):
        if self.attacking:
            player_sheet = self.animation_sheets["attack"][self.dir]
            frame_width = 23 if self.dir in ("down", "up") else 16
            frame_height = player_sheet.get_height()
            frame_x = self.attack_frame * frame_width
        else:
            animation = "walk" if self.running else "idle"
            player_sheet = self.animation_sheets[animation][self.dir]
            frame_width = 16
            frame_height = 16
            frame_x = walk_frame

        player_image = player_sheet.subsurface(pygame.Rect(frame_x, 0, frame_width, frame_height)).copy()
        player_image = pygame.transform.scale(player_image, (self.size, self.size))
        screen.blit(player_image,(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def drawstats(self, screen, healthcolour, goldcolour, levelcolour, xpcolour):

        transparent_surface = pygame.Surface((180, 100), pygame.SRCALPHA)
        transparent_surface.fill(TRANSPARENT)
        screen.blit(transparent_surface, (10, 10))

        health = self.font.render(f"Health: {self.health}/100", True, healthcolour)
        gold = self.font.render(f"Gold: {self.gold}", True, goldcolour)
        level = self.font.render(f"Level: {self.level}", True, levelcolour)
        xp = self.font.render(f"XP: {self.xp}", True, xpcolour)

        health_rect = health.get_rect(topleft=(20, 20))
        gold_rect = gold.get_rect(topleft=(20, 40))
        level_rect = level.get_rect(topleft=(20, 60))
        xp_rect = xp.get_rect(topleft=(20, 80))

        screen.blit(health, health_rect)
        screen.blit(gold, gold_rect)
        screen.blit(level, level_rect)
        screen.blit(xp, xp_rect)

    def relateX(self, x):
        X = x + SCREEN_WIDTH/2 - self.x
        return X
    
    def relateY(self, y):
            Y = y + SCREEN_HEIGHT/2 - self.y
            return Y

    def damage(self, damn):
        self.health -= damn

    def recieve_money(self, ammount):
        self.gold += ammount

    def recieve_xp(self, ammount):
        self.xp += ammount

border = {
    "XLeft": 0,
    "XRight": 3200,
    "YTop": 0,
    "YBottom": 1600,
}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOUR = (200, 212, 93)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 255, 0)
YELLOW = (201, 165, 20)
BLUE = (0, 0, 255)
GREEN = (74, 196, 37)
LIGHT_GREEN = (60, 255, 0)
alpha_val = 128  # 0 (invisible) to 255 (solid)
TRANSPARENT = (48, 84, 2, alpha_val)

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
    player.rect = pygame.Rect(x, y, player.size, player.size)
    return any(
        item_name not in excepting and
        not item_data.get("walkable", False)
        and
        player.rect.colliderect(
            pygame.Rect(
                item_data["x"],
                item_data["y"],
                item_data["width"],
                item_data["height"],
            )
        )
        for item_name, item_data in world_items.items()
    )


running = True
#animation box holders
x = 0
frame_count = 0
excepting = set()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not player.attacking:
                player.attacking = True
                player.attack_frame = 0
                player.attack_timer = 0

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

    #collisions
    if not player_collides_with_buildings(player.x + move_x, player.y):
        player.x += move_x
    if not player_collides_with_buildings(player.x, player.y + move_y):
        player.y += move_y

    # Damage system
    if frame_count % 10 == 0:
        for item_name, item_data in world_items.items():
            if item_name not in excepting:
                if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"],)) and item_data["damage"] > 0:
                    player.damage(item_data["damage"])
                    player.damn = True

    # Gold system
    for item_name, item_data in world_items.items():
        if item_name not in excepting:
            if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"],)) and item_data["gold"] > 0:
                player.recieve_money(item_data["gold"])
                player.ching = True
    # Xp system
    for item_name, item_data in world_items.items():
        if item_name not in excepting:
            if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"],)) and item_data["xp"] > 0:
                player.recieve_xp(item_data["xp"])
                player.chong = True

    for item_name, item_data in world_items.items():
        if item_name not in excepting:
            if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"],)) and item_data["destroy_on_impact"]:
                excepting.add(item_name)

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


    pygame.draw.rect(screen, RED, (player.relateX(border["XLeft"]), player.relateY(0), 10, border["YBottom"]))
    pygame.draw.rect(screen, RED, (player.relateX(border["XRight"] - 10), player.relateY(0), 10, border["YBottom"]))
    pygame.draw.rect(screen, RED, (player.relateX(0), player.relateY(border["YTop"]), border["XRight"], 10))
    pygame.draw.rect(screen, RED, (player.relateX(0), player.relateY(border["YBottom"] - 10), border["XRight"], 10))

    for item_name, item_data in world_items.items():
        if item_name not in excepting:
            image = item_images[item_data["path"]]
            position = (player.relateX(item_data["x"]), player.relateY(item_data["y"]))
            screen.blit(image, position)

    c1 = RED if player.damn else WHITE
    c2 = YELLOW if player.ching else GOLD
    c4 = LIGHT_GREEN if player.chong else GREEN

    player.drawstats(screen, c1, c2, BLUE, c4)

    if frame_count % 3 == 0:
        player.damn = False
        player.ching = False
        player.chong = False

    # drawing the player
    frame_count += 1
    if frame_count % 10 == 0 and player.running == True:
        x += 16
    if x == 96:
        x = 0

    if player.attacking:
        player.attack_timer += 1
        if player.attack_timer % 6 == 0:
            player.attack_frame += 1
            if player.attack_frame == 6:
                player.attacking = False
                player.attack_frame = 0

    player.draw(screen, x)

    # frame clean up
    if frame_count % 500 == 0:
        frame_count = 0



    pygame.display.flip()
    clock.tick(60)

pygame.quit()