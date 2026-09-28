import json
from pathlib import Path
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAMERA_ZOOM = 2
PLAYER_START_X = 15
PLAYER_SPEED = 2
PLAYER_HEALTH = 100
PLAYER_MAX_HEALTH = 100
PLAYER_STARTING_GOLD = 50
PLAYER_STARTING_LEVEL = 1
PLAYER_SIZE = 16
PLAYER_GRAPHIC_PATH = "maps/Tiny Village Pack/Tiny Adventure Pack/Character/Char_one"
WORLD_WIDTH = 3200
WORLD_HEIGHT = 1600
BG_COLOUR = (200, 212, 93)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

border = {"XLeft": 0, "XRight": WORLD_WIDTH, "YTop": 0, "YBottom": WORLD_HEIGHT}


class Player:
    def __init__(self, x, y, speed, health, max_health, gold, level, size, graphic):
        self.x, self.y = x, y
        self.speed = speed
        self.health, self.max_health = health, max_health
        self.gold, self.level = gold, level
        self.xp = 0
        self.size = size
        self.graphic = graphic
        self.dir = "down"
        self.running = self.attacking = False
        self.attack_frame = self.attack_timer = 0
        self.rect = pygame.Rect(x, y, size, size)
        self.font = pygame.font.SysFont("arial", 28)
        self.animation_sheets = {
            state: {
                direction: pygame.image.load(
                    f"{graphic}/{folder}/{prefix}{direction}.png"
                ).convert_alpha()
                for direction in ("down", "left", "right", "up")
            }
            for state, folder, prefix in (
                ("idle", "Idle", "Char_idle_"),
                ("walk", "Walk", "Char_walk_"),
                ("attack", "Attack", "Char_atk_"),
            )
        }

    def world_to_screen(self, world_x, world_y):
        return (
            SCREEN_WIDTH / 2 + (world_x - self.x) * CAMERA_ZOOM,
            SCREEN_HEIGHT / 2 + (world_y - self.y) * CAMERA_ZOOM,
        )

    def draw(self, screen, walk_frame):
        sheet = self.animation_sheets[
            "attack" if self.attacking else ("walk" if self.running else "idle")
        ][self.dir]

        frame_width = (
            23 if self.attacking and self.dir in ("down", "up") else 16
        )
        frame_x = (
            self.attack_frame * frame_width
            if self.attacking
            else walk_frame
        )

        image = sheet.subsurface(
            pygame.Rect(
                frame_x,
                0,
                frame_width,
                sheet.get_height() if self.attacking else 16,
            )
        ).copy()

        player_size = int(self.size * CAMERA_ZOOM)
        image = pygame.transform.scale(
            image,
            (player_size, player_size),
        )

        screen.blit(
            image,
            (
                SCREEN_WIDTH // 2 - player_size // 2,
                SCREEN_HEIGHT // 2 - player_size // 2,
            ),
        )

    def drawstats(self, screen):
        pygame.draw.rect(
            screen,
            (20, 20, 25),
            pygame.Rect(15, 15, 260, 140),
        )

        pygame.draw.rect(
            screen,
            (50, 50, 50),
            pygame.Rect(25, 25, 220, 22),
        )

        health_width = int(
            220 * max(0, min(1, self.health / self.max_health))
        )

        pygame.draw.rect(
            screen,
            (220, 50, 50),
            pygame.Rect(25, 25, health_width, 22),
        )

        stats = (
            (f"HP: {self.health}/{self.max_health}", (30, 55)),
            (f"Gold: {self.gold}", (30, 85)),
            (f"Level: {self.level}", (30, 110)),
            (f"XP: {self.xp}", (30, 135)),
        )

        for text, position in stats:
            screen.blit(
                self.font.render(text, True, WHITE),
                position,
            )

    def damage(self, amount):
        self.health = max(0, self.health - amount)

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= 100:
            self.xp -= 100
            self.level += 1
            self.max_health += 10
            self.health = self.max_health

    def add_gold(self, amount):
        self.gold += amount


pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("Dungeons of Dagestan")

clock = pygame.time.Clock()

player = Player(
    PLAYER_START_X,
    WORLD_HEIGHT / 2,
    PLAYER_SPEED,
    PLAYER_HEALTH,
    PLAYER_MAX_HEALTH,
    PLAYER_STARTING_GOLD,
    PLAYER_STARTING_LEVEL,
    PLAYER_SIZE,
    PLAYER_GRAPHIC_PATH,
)

with Path("world_items.json").open(encoding="utf-8") as items_file:
    world_items = json.load(items_file)

item_images = {}

for item_data in world_items.values():
    path = item_data["path"]

    if path not in item_images:
        item_images[path] = pygame.image.load(path).convert_alpha()


def player_collides_with_buildings(x, y):
    player.rect = pygame.Rect(
        x,
        y,
        player.size,
        player.size,
    )

    return any(
        not item.get("walkable", False)
        and player.rect.colliderect(
            pygame.Rect(
                item["x"],
                item["y"],
                item["width"],
                item["height"],
            )
        )
        for item in world_items.values()
    )


running = True
frame_count = 0
walk_frame = 0
removed_items = set()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and not player.attacking
        ):
            player.attacking = True
            player.attack_frame = 0
            player.attack_timer = 0

    keys = pygame.key.get_pressed()

    move_x = (
        keys[pygame.K_d] - keys[pygame.K_a]
    ) * player.speed

    move_y = (
        keys[pygame.K_s] - keys[pygame.K_w]
    ) * player.speed

    if move_x != 0:
        move_y = 0

    for key, direction in (
        (pygame.K_a, "left"),
        (pygame.K_d, "right"),
        (pygame.K_w, "up"),
        (pygame.K_s, "down"),
    ):
        if keys[key]:
            player.dir = direction
            player.running = True
            break
    else:
        player.running = False

    if not player_collides_with_buildings(
        player.x + move_x,
        player.y,
    ):
        player.x += move_x

    if not player_collides_with_buildings(
        player.x,
        player.y + move_y,
    ):
        player.y += move_y

    player.x = max(
        border["XLeft"],
        min(
            player.x,
            border["XRight"] - player.size,
        ),
    )

    player.y = max(
        border["YTop"],
        min(
            player.y,
            border["YBottom"] - player.size,
        ),
    )

    for name, item in world_items.items():
        if name in removed_items:
            continue

        item_rect = pygame.Rect(
            item["x"],
            item["y"],
            item["width"],
            item["height"],
        )

        if player.rect.colliderect(item_rect):
            if (
                frame_count % 10 == 0
                and item.get("damage", 0) > 0
            ):
                player.damage(item["damage"])

            if item.get("gold", 0) > 0:
                player.add_gold(item["gold"])

            if item.get("xp", 0) > 0:
                player.gain_xp(item["xp"])

            if item.get("destroy_on_impact", False):
                removed_items.add(name)

    screen.fill(BG_COLOUR)

    border_rects = (
        (
            player.world_to_screen(border["XLeft"], 0),
            (
                10 * CAMERA_ZOOM,
                WORLD_HEIGHT * CAMERA_ZOOM,
            ),
        ),
        (
            player.world_to_screen(border["XRight"] - 10, 0),
            (
                10 * CAMERA_ZOOM,
                WORLD_HEIGHT * CAMERA_ZOOM,
            ),
        ),
        (
            player.world_to_screen(0, border["YTop"]),
            (
                WORLD_WIDTH * CAMERA_ZOOM,
                10 * CAMERA_ZOOM,
            ),
        ),
        (
            player.world_to_screen(0, border["YBottom"] - 10),
            (
                WORLD_WIDTH * CAMERA_ZOOM,
                10 * CAMERA_ZOOM,
            ),
        ),
    )

    for position, size in border_rects:
        pygame.draw.rect(
            screen,
            RED,
            (*position, *size),
        )

    for name, item in world_items.items():
        if name in removed_items:
            continue

        image = item_images[item["path"]]

        image_width = int(image.get_width() * CAMERA_ZOOM)
        image_height = int(image.get_height() * CAMERA_ZOOM)

        image = pygame.transform.scale(
            image,
            (image_width, image_height),
        )

        screen.blit(
            image,
            player.world_to_screen(
                item["x"],
                item["y"],
            ),
        )

    player.drawstats(screen)

    frame_count += 1

    if frame_count % 10 == 0 and player.running:
        walk_frame = (walk_frame + 16) % 96

    if player.attacking:
        player.attack_timer += 1

        if player.attack_timer % 6 == 0:
            player.attack_frame += 1

            if player.attack_frame >= 6:
                player.attacking = False
                player.attack_frame = 0

    player.draw(screen, walk_frame)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()