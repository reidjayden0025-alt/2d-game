import json
from pathlib import Path
import pygame

# Constants & Configuration
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
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
TRANSPARENT = (0, 0, 0, 0)

wrld_file = "world_items.json"
tel = False
excepting = set()

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
        self.running = False
        self.attacking = False
        self.attack_frame = 0
        self.attack_timer = 0
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.damn = False
        self.gesond = False
        self.ching = False
        self.chong = False
        self.font = pygame.font.SysFont("roboto", 32)

        self.animation_sheets = {  # dont get confused looking at this, it's only 3 nested dictionairies that initialise animated images by themselves
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
        player_size = int(self.size * CAMERA_ZOOM)
        player_image = pygame.transform.scale(player_image, (player_size, player_size))
        screen.blit(
            player_image,
            (
                SCREEN_WIDTH // 2 - player_size // 2,
                SCREEN_HEIGHT // 2 - player_size // 2,
            ),
        )

    def drawstats(self, screen, healthcolour=WHITE, goldcolour=GOLD, levelcolour=WHITE, xpcolour=GREEN):
        # Combined transparent HUD and rendered text display
        transparent_surface = pygame.Surface((180, 100), pygame.SRCALPHA)
        transparent_surface.fill(TRANSPARENT)
        screen.blit(transparent_surface, (10, 10))

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

        health = self.font.render(f"Health: {self.health}/{self.max_health}", True, healthcolour)
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
        X = x + SCREEN_WIDTH / 2 - self.x
        return X

    def relateY(self, y):
        Y = y + SCREEN_HEIGHT / 2 - self.y
        return Y

    def damage(self, damn):
        self.health = max(0, self.health - damn)

    def heal(self, hoeveelheid):
        self.health = min(self.max_health, self.health + hoeveelheid)

    def recieve_money(self, ammount):
        self.gold += ammount

    def add_gold(self, amount):
        self.gold += amount

    def recieve_xp(self, ammount):
        self.xp += ammount

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= 100:
            self.xp -= 100
            self.level += 1
            self.max_health += 10
            self.health = self.max_health


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

with Path(wrld_file).open(encoding="utf-8") as items_file:
    world_items = json.load(items_file)

with Path("telport_rects.json").open(encoding="utf-8") as file:
    teleport_rectangles = json.load(file)

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

    if tel == True:
        with Path(wrld_file).open(encoding="utf-8") as items_file:
            world_items = json.load(items_file)

    # Controlls:
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

    # Damage system
    if frame_count % 10 == 0:
        for item_name, item_data in world_items.items():
            if item_name not in excepting and item_name not in removed_items:
                if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"])) and item_data.get("damage", 0) > 0:
                    player.damage(item_data["damage"])
                    player.damn = True

    # Health system
    if frame_count % 10 == 0:
        for item_name, item_data in world_items.items():
            if item_name not in excepting and item_name not in removed_items:
                if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"])) and item_data.get("health", 0) > 0:
                    player.heal(item_data["health"])
                    player.gesond = True

    # Gold system
    for item_name, item_data in world_items.items():
        if item_name not in excepting and item_name not in removed_items:
            if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"])) and item_data.get("gold", 0) > 0:
                player.recieve_money(item_data["gold"])
                player.ching = True

    # Xp system
    for item_name, item_data in world_items.items():
        if item_name not in excepting and item_name not in removed_items:
            if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"])) and item_data.get("xp", 0) > 0:
                player.recieve_xp(item_data["xp"])
                player.chong = True

    for item_name, item_data in world_items.items():
        if item_name not in excepting and item_name not in removed_items:
            if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"])) and item_data.get("destroy_on_impact", False):
                excepting.add(item_name)
                removed_items.add(item_name)

    # Teleporting
    for item_name, item_data in teleport_rectangles.items():
        if player.rect.colliderect(pygame.Rect(item_data["x"], item_data["y"], item_data["width"], item_data["height"])) and wrld_file == item_data["application_wrld"]:
            wrld_file = item_data["wrld"]
            tel = True

    # Bordering:
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
        if name in removed_items or name in excepting:
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

    c1 = RED if player.damn else WHITE
    c1 = LIGHT_GREEN if player.gesond else c1
    c2 = YELLOW if player.ching else GOLD
    c4 = LIGHT_GREEN if player.chong else GREEN

    player.drawstats(screen, c1, c2, WHITE, c4)

    if frame_count % 3 == 0:
        player.damn = False
        player.gesond = False
        player.ching = False
        player.chong = False
        player.tel = False

    if player.health > player.max_health:
        player.health = player.max_health

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