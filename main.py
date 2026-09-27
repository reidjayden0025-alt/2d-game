import json
from pathlib import Path

import pygame


class Player:
    def __init__(self, x, y, speed, health, max_health, gold, level, size, graphic):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.max_health = max_health
        self.gold = gold
        self.level = level
        self.xp = 0
        self.size = size
        self.graphic = graphic
        self.dir = "down"
        self.running = False
        self.attacking = False
        self.attack_frame = 0
        self.attack_timer = 0
        self.rect = pygame.Rect(x, y, size, size)
        self.damn = self.ching = self.chong = False
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

    def draw(self, screen, walk_frame):
        sheet = self.animation_sheets["attack" if self.attacking else ("walk" if self.running else "idle")][self.dir]
        frame_width = 23 if self.attacking and self.dir in ("down", "up") else 16
        frame_height = sheet.get_height() if self.attacking else 16
        frame_x = self.attack_frame * frame_width if self.attacking else walk_frame
        image = sheet.subsurface(pygame.Rect(frame_x, 0, frame_width, frame_height)).copy()
        screen.blit(pygame.transform.scale(image, (self.size, self.size)), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def drawstats(self, screen):
        pygame.draw.rect(screen, (20, 20, 25), pygame.Rect(15, 15, 260, 140))
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(25, 25, 220, 22))
        health_width = int(220 * max(0, min(1, self.health / self.max_health)))
        pygame.draw.rect(screen, (220, 50, 50), pygame.Rect(25, 25, health_width, 22))
        for text, position in (
            (f"HP: {self.health}/{self.max_health}", (30, 55)),
            (f"Gold: {self.gold}", (30, 85)),
            (f"Level: {self.level}", (30, 110)),
            (f"XP: {self.xp}", (30, 135)),
        ):
            screen.blit(self.font.render(text, True, WHITE), position)

    def relateX(self, value):
        return value + SCREEN_WIDTH / 2 - self.x

    def relateY(self, value):
        return value + SCREEN_HEIGHT / 2 - self.y

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

    def recieve_money(self, amount):
        self.add_gold(amount)

    def recieve_xp(self, amount):
        self.gain_xp(amount)


border = {"XLeft": 0, "XRight": 3200, "YTop": 0, "YBottom": 1600}
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOUR = (30, 150, 30)
WHITE, RED = (255, 255, 255), (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeons of Dagestan")
clock = pygame.time.Clock()
player = Player(15, border["YBottom"] / 2, 10, 100, 100, 50, 1, 32, "maps/Tiny Village Pack/Tiny Adventure Pack/Character/Char_one")

with Path("world_items.json").open(encoding="utf-8") as items_file:
    world_items = json.load(items_file)

item_images = {}
for item_data in world_items.values():
    path = item_data["path"]
    item_images.setdefault(path, pygame.image.load(path).convert_alpha())


def player_collides_with_buildings(x, y):
    player.rect = pygame.Rect(x, y, player.size, player.size)
    return any(
        not item.get("walkable", False)
        and player.rect.colliderect(pygame.Rect(item["x"], item["y"], item["width"], item["height"]))
        for item in world_items.values()
    )


running = True
frame_count = walk_frame = 0
removed_items = set()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not player.attacking:
            player.attacking = True
            player.attack_frame = player.attack_timer = 0

    keys = pygame.key.get_pressed()
    move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * player.speed
    move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * player.speed
    if move_x:
        move_y = 0
    for key, direction in ((pygame.K_a, "left"), (pygame.K_d, "right"), (pygame.K_w, "up"), (pygame.K_s, "down")):
        if keys[key]:
            player.dir, player.running = direction, True
            break
    else:
        player.running = False

    if not player_collides_with_buildings(player.x + move_x, player.y):
        player.x += move_x
    if not player_collides_with_buildings(player.x, player.y + move_y):
        player.y += move_y

    for name, item in world_items.items():
        if name in removed_items:
            continue
        collision = player.rect.colliderect(pygame.Rect(item["x"], item["y"], item["width"], item["height"]))
        if collision and frame_count % 10 == 0 and item.get("damage", 0) > 0:
            player.damage(item["damage"])
            player.damn = True
        if collision and item.get("gold", 0) > 0:
            player.add_gold(item["gold"])
            player.ching = True
        if collision and item.get("xp", 0) > 0:
            player.gain_xp(item["xp"])
            player.chong = True
        if collision and item.get("destroy_on_impact", False):
            removed_items.add(name)

    player.x = max(border["XLeft"], min(player.x, border["XRight"] - player.size))
    player.y = max(border["YTop"], min(player.y, border["YBottom"] - player.size))
    screen.fill(BG_COLOUR)
    pygame.draw.rect(screen, RED, (player.relateX(border["XLeft"]), player.relateY(0), 10, border["YBottom"]))
    pygame.draw.rect(screen, RED, (player.relateX(border["XRight"] - 10), player.relateY(0), 10, border["YBottom"]))
    pygame.draw.rect(screen, RED, (player.relateX(0), player.relateY(border["YTop"]), border["XRight"], 10))
    pygame.draw.rect(screen, RED, (player.relateX(0), player.relateY(border["YBottom"] - 10), border["XRight"], 10))
    for name, item in world_items.items():
        if name not in removed_items:
            screen.blit(item_images[item["path"]], (player.relateX(item["x"]), player.relateY(item["y"])))

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
