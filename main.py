import json
from pathlib import Path

import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ZOOM = 1.5

BG_COLOUR = (200, 212, 93)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 255, 0)
YELLOW = (201, 165, 20)
BLUE = (0, 0, 255)
GREEN = (74, 196, 37)
LIGHT_GREEN = (60, 255, 0)
TRANSPARENT = (48, 84, 2, 128)

border = {
    "XLeft": 0,
    "XRight": 3200,
    "YTop": 0,
    "YBottom": 1600,
}


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
        self.dir = "down"
        self.running = False
        self.attacking = False
        self.attack_frame = 0
        self.attack_timer = 0
        self.rect = pygame.Rect(x, y, size, size)
        self.damn = False
        self.ching = False
        self.chong = False
        self.font = pygame.font.SysFont("roboto", 32)

        self.animation_sheets = {
            animation: {
                direction: pygame.image.load(
                    f"{graphic}/{folder}/Char_{prefix}_{direction}.png"
                ).convert_alpha()
                for direction in ("down", "left", "right", "up")
            }
            for animation, folder, prefix in (
                ("idle", "Idle", "idle"),
                ("walk", "Walk", "walk"),
                ("attack", "Attack", "atk"),
            )
        }

    def draw(self, screen, walk_frame):
        if self.attacking:
            sheet = self.animation_sheets["attack"][self.dir]
            frame_width = 23 if self.dir in ("down", "up") else 16
            frame_x = self.attack_frame * frame_width
        else:
            sheet = self.animation_sheets["walk" if self.running else "idle"][self.dir]
            frame_width = 16
            frame_x = walk_frame

        image = sheet.subsurface(
            pygame.Rect(frame_x, 0, frame_width, sheet.get_height())
        )
        image = pygame.transform.scale(
            image,
            (int(self.size * ZOOM), int(self.size * ZOOM)),
        )
        screen.blit(
            image,
            image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
        )

    def drawstats(self, screen):
        surface = pygame.Surface((180, 100), pygame.SRCALPHA)
        surface.fill(TRANSPARENT)
        screen.blit(surface, (10, 10))

        stats = (
            (f"Health: {self.health}/100", RED if self.damn else WHITE),
            (f"Gold: {self.gold}", YELLOW if self.ching else GOLD),
            (f"Level: {self.level}", BLUE),
            (f"XP: {self.xp}", LIGHT_GREEN if self.chong else GREEN),
        )

        for index, (text, colour) in enumerate(stats):
            image = self.font.render(text, True, colour)
            screen.blit(image, image.get_rect(topleft=(20, 20 + index * 20)))

    def relate_x(self, x):
        return (x - self.x) * ZOOM + SCREEN_WIDTH / 2

    def relate_y(self, y):
        return (y - self.y) * ZOOM + SCREEN_HEIGHT / 2

    def damage(self, amount):
        self.health -= amount

    def receive_money(self, amount):
        self.gold += amount

    def receive_xp(self, amount):
        self.xp += amount


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeons of Dagestan")
clock = pygame.time.Clock()

player = Player(
    15,
    border["YBottom"] / 2,
    5,
    100,
    16,
    "maps/Tiny Village Pack/Tiny Adventure Pack/Character/Char_one",
)

with Path("world_items.json").open(encoding="utf-8") as file:
    world_items = json.load(file)

item_images = {
    data["path"]: pygame.image.load(data["path"]).convert_alpha()
    for data in world_items.values()
}


def item_rect(data):
    return pygame.Rect(
        data["x"],
        data["y"],
        data["width"],
        data["height"],
    )


def collides(x, y):
    player.rect = pygame.Rect(x, y, player.size, player.size)

    return any(
        name not in excepting
        and not data.get("walkable", False)
        and player.rect.colliderect(item_rect(data))
        for name, data in world_items.items()
    )


def touching_items():
    return [
        (name, data)
        for name, data in world_items.items()
        if name not in excepting and player.rect.colliderect(item_rect(data))
    ]


def update_items():
    for name, data in touching_items():
        if frame_count % 10 == 0 and data["damage"] > 0:
            player.damage(data["damage"])
            player.damn = True

        if data["gold"] > 0:
            player.receive_money(data["gold"])
            player.ching = True

        if data["xp"] > 0:
            player.receive_xp(data["xp"])
            player.chong = True

        if data["destroy_on_impact"]:
            excepting.add(name)


def draw_border():
    left = player.relate_x(border["XLeft"])
    top = player.relate_y(border["YTop"])
    width = int((border["XRight"] - border["XLeft"]) * ZOOM)
    height = int((border["YBottom"] - border["YTop"]) * ZOOM)
    thickness = int(10 * ZOOM)

    pygame.draw.rect(screen, RED, (left, top, thickness, height))
    pygame.draw.rect(
        screen,
        RED,
        (
            player.relate_x(border["XRight"] - 10),
            top,
            thickness,
            height,
        ),
    )
    pygame.draw.rect(screen, RED, (left, top, width, thickness))
    pygame.draw.rect(
        screen,
        RED,
        (
            left,
            player.relate_y(border["YBottom"] - 10),
            width,
            thickness,
        ),
    )


def draw_items():
    for name, data in world_items.items():
        if name in excepting:
            continue

        image = item_images[data["path"]]
        size = (
            int(image.get_width() * ZOOM),
            int(image.get_height() * ZOOM),
        )
        image = pygame.transform.scale(image, size)

        screen.blit(
            image,
            (
                int(player.relate_x(data["x"])),
                int(player.relate_y(data["y"])),
            ),
        )


running = True
frame_count = 0
walk_frame = 0
excepting = set()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and not player.attacking
        ):
            player.attacking = True
            player.attack_frame = 0
            player.attack_timer = 0

    keys = pygame.key.get_pressed()

    move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * player.speed
    move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * player.speed

    directions = (
        (pygame.K_s, "down"),
        (pygame.K_d, "right"),
        (pygame.K_w, "up"),
        (pygame.K_a, "left"),
    )

    for key, direction in directions:
        if keys[key]:
            player.dir = direction
            player.running = True
            break
    else:
        player.running = False

    if not collides(player.x + move_x, player.y):
        player.x += move_x

    if not collides(player.x, player.y + move_y):
        player.y += move_y

    player.rect.topleft = player.x, player.y
    update_items()

    player.x = max(
        border["XLeft"],
        min(player.x, border["XRight"] - player.size),
    )
    player.y = max(
        border["YTop"],
        min(player.y, border["YBottom"] - player.size),
    )

    screen.fill(BG_COLOUR)
    draw_border()
    draw_items()
    player.drawstats(screen)

    if frame_count % 3 == 0:
        player.damn = False
        player.ching = False
        player.chong = False

    frame_count += 1

    if frame_count % 10 == 0 and player.running:
        walk_frame = (walk_frame + 16) % 96

    if player.attacking:
        player.attack_timer += 1

        if player.attack_timer % 6 == 0:
            player.attack_frame += 1

            if player.attack_frame == 6:
                player.attacking = False
                player.attack_frame = 0

    player.draw(screen, walk_frame)

    if frame_count >= 500:
        frame_count = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()