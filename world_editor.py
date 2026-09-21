import json
import math
import os
from pathlib import Path
from PIL import Image
import pygame

class crossbar:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = 15

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH//2 - 5, SCREEN_HEIGHT//2, self.size, 3))
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 5, 3, self.size))
        pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 1, 1))

    def relateX(self, x):
        X = x + SCREEN_WIDTH/2 - self.x
        return X
    
    def relateY(self, y):
            Y = y + SCREEN_HEIGHT/2 - self.y
            return Y

buildings_path = "maps/Tiny Village Pack/Outdoors/Buildings"
images = {
    "Buildings:House1_blue.png": (buildings_path + "/House1_blue.png"),
    "Buildings:House1_green.png": (buildings_path + "/House1_green.png"),
    "Buildings:House1_red.png": (buildings_path + "/House1_red.png"),
    "Buildings:House1_spritesheet.png": (buildings_path + "/House1_spritesheet.png"),
    "Buildings:House2_blue.png": (buildings_path + "/House2_blue.png"),
    "Buildings:House2_green.png": (buildings_path + "/House2_green.png"),
    "Buildings:House2_red.png": (buildings_path + "/House2_red.png"),
    "Buildings:House2_spritesheet.png": (buildings_path + "/House2_spritesheet.png"),
    "Buildings:House3_blue.png": (buildings_path + "/House3_blue.png"),
    "Buildings:House3_green.png": (buildings_path + "/House3_green.png"),
    "Buildings:House3_red.png": (buildings_path + "/House3_red.png"),
    "Buildings:House3_spritesheet.png": (buildings_path + "/House3_spritesheet.png"),
    "Buildings:House4_blue.png": (buildings_path + "/House4_blue.png"),
    "Buildings:House4_green.png": (buildings_path + "/House4_green.png"),
    "Buildings:House4_red.png": (buildings_path + "/House4_red.png"),
    "Buildings:House4_spritesheet.png": (buildings_path + "/House4_spritesheet.png"),
    "Buildings:Wooden_House1_blue.png": (buildings_path + "/Wooden_House1_blue.png"),
    "Buildings:Wooden_House1_green.png": (buildings_path + "/Wooden_House1_green.png"),
    "Buildings:Wooden_House1_red.png": (buildings_path + "/Wooden_House1_red.png"),
    "Buildings:Wooden_House2_blue.png": (buildings_path + "/Wooden_House2_blue.png"),
    "Buildings:Wooden_House2_green.png": (buildings_path + "/Wooden_House2_green.png"),
    "Buildings:Wooden_House2_red.png": (buildings_path + "/Wooden_House2_red.png"),
    "Buildings:Wooden_House3_blue.png": (buildings_path + "/Wooden_House3_blue.png"),
    "Buildings:Wooden_House3_green.png": (buildings_path + "/Wooden_House3_green.png"),
    "Buildings:Wooden_House3_red.png": (buildings_path + "/Wooden_House3_red.png"),
    "Buildings:Wooden_House4_blue.png": (buildings_path + "/Wooden_House4_blue.png"),
    "Buildings:Wooden_House4_green.png": (buildings_path + "/Wooden_House4_green.png"),
    "Buildings:Wooden_House4_red.png": (buildings_path + "/Wooden_House4_red.png"),

    "Farm:blue_veggie.png": ("maps/Tiny Village Pack/Outdoors/Farm/blue_veggie.png"),
    "Farm:blue_veggie_2.png": ("maps/Tiny Village Pack/Outdoors/Farm/blue_veggie_2.png"),
    "Farm:farm_spot_dry.png": ("maps/Tiny Village Pack/Outdoors/Farm/farm_spot_dry.png"),
    "Farm:farm_spot_wet.png": ("maps/Tiny Village Pack/Outdoors/Farm/farm_spot_wet.png"),
    "Farm:orange_veggie.png": ("maps/Tiny Village Pack/Outdoors/Farm/orange_veggie.png"),
    "Farm:orange_veggie_2.png": ("maps/Tiny Village Pack/Outdoors/Farm/orange_veggie_2.png"),
    "Farm:red_veggie.png": ("maps/Tiny Village Pack/Outdoors/Farm/red_veggie.png"),
    "Farm:red_veggie_2.png": ("maps/Tiny Village Pack/Outdoors/Farm/red_veggie_2.png"),
    "Farm:sprout.png": ("maps/Tiny Village Pack/Outdoors/Farm/sprout.png"),
    "Farm:white_veggie.png": ("maps/Tiny Village Pack/Outdoors/Farm/white_veggie.png"),
    "Farm:white_veggie_2.png": ("maps/Tiny Village Pack/Outdoors/Farm/white_veggie_2.png"),

    "dirt path.png": ("maps/Tiny Village Pack/Tilesets/dit path.png"),
    "Other:bench.png": ("maps/Tiny Village Pack/Outdoors/Other/bench.png"),
    "Other:mailbox.png": ("maps/Tiny Village Pack/Outdoors/Other/mailbox.png"),
    "Other:sign.png": ("maps/Tiny Village Pack/Outdoors/Other/sign.png"),
    "Other:sign_2_left.png": ("maps/Tiny Village Pack/Outdoors/Other/sign_2_left.png"),
    "Other:sign_2_right.png": ("maps/Tiny Village Pack/Outdoors/Other/sign_2_right.png"),
    "Other:streetlight.png": ("maps/Tiny Village Pack/Outdoors/Other/streetlight.png"),
    "Other:coin.png": "maps/Tiny Village Pack/Tiny Adventure Pack/Other/Coin.png",
    "Sword": "maps/Inventory Ui items/Rusty Sword.png"

}

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOUR = (32, 168, 32)
RED = (255, 0 , 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeons of Dagestan world editor")

clock = pygame.time.Clock()

with Path("world_items.json").open(encoding="utf-8") as items_file:
    world_items = json.load(items_file)

item_images = {}
for item_data in world_items.values():
    path = item_data["path"]
    if path not in item_images:
        item_images[path] = pygame.image.load(path).convert_alpha()

border = {
    "XLeft": 0,
    "XRight": 3200,
    "YTop": 0,
    "YBottom": 1600,
}

crossbar = crossbar(0, 0, 1)
P_COOLDOWN_MS = 500
last_p_press = 0
pastes = 0
name = ""

def main():
    global last_p_press


    json_file = "world_items.json"

    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
        print("Info: file does not exitst yet")

    item_to_add = input("Input: select the file name of the item to add:    ")
    item_name = input("Input: type a nickname for this item (that is not already used in the json as a key):    ")

    walkQ = input("Input: Should the player be able to walk over the object? Y/N:    ")
    walkable = True if walkQ == "Y" else False

    dq = input("Input: should the object be destroyed on impact? Y/N:    ")
    destroy_on_impact = True if dq == "Y" else False

    
    if item_to_add in images:


        damage = int(input("Input: How much damamge does the charechter take when coming into contact with this object? 0 if none:    "))
        gold  = int(input("Input: How much gold is this item when picked up? 0 if not gold:    "))
        xp = int(input("Input: How much xp is this item when picked up? 0 if not xp:    "))

        with Image.open(images[item_to_add]) as img:
            width, height = img.size
            print(f"Info: Image dimensions: ({width}x{height})")
            print(f"INSTRUCTION: check the game window")
            print(f"INSTRUCTION: WASD = move; Arrows = fast move")
            print(f"INSTRUCTION: P: paste")
            print(f"INSTRUCTION: U: undo paste")
            print(f"INSTRUCTION: C: get crossbar coords")
            print(f"INSTRUCTION: I: get closest object information")
    

        running = True
        name = ""

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    now = pygame.time.get_ticks()
                    if now - last_p_press >= P_COOLDOWN_MS:
                        global pastes
                        last_p_press = now
                        pastes += 1
                        x = int(crossbar.x)
                        y = int(crossbar.y)
                        print(f"Player position saved: ({x}, {y})")
                        name = f"{item_name}{pastes}"
                        image_path = images[item_to_add]

                        data[name] = {
                            "path": image_path,
                            "x": x,
                            "y": y,
                            "width": width,
                            "height": height,
                            "walkable": walkable,
                            "destroy_on_impact": destroy_on_impact,
                            "damage": damage,
                            "gold": gold,
                            "xp": xp
                        }

                        with open(json_file, "w") as f:
                            json.dump(data, f, indent=4)

                        print(f"Info: Successfully added '{item_to_add}' to {json_file}!")

                        world_items[name] = data[name]
                        if image_path not in item_images:
                            item_images[image_path] = pygame.image.load(image_path).convert_alpha()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    print(f"X: {crossbar.x}; Y: {crossbar.y}")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    with open("world_items.json", "r", encoding="utf-8") as f:
                        data = json.load(f)

                        key_to_delete = f"{item_name}{pastes}"
                        pastes -= 1

                        if key_to_delete in data:
                            data.pop(key_to_delete, None)
                        with open("world_items.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4)

                        world_items.pop(key_to_delete, None)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    closest_items = [
                        (item_name, item, math.hypot(
                            crossbar.x - item["x"],
                            crossbar.y - item["y"],
                        ))
                        for item_name, item in data.items()
                    ]

                    if closest_items:
                        closest_name, closest_item, closest_distance = min(
                            closest_items, key=lambda item: item[2]
                        )
                        print(
                            f"Name: {closest_name}\n"
                            f"Distance: {closest_distance:.2f}\n"
                            f"Coords: {closest_item['x']}x{closest_item['y']}\n"
                            f"Dimensions: {closest_item['width']}x{closest_item['height']}\n"
                            f"Walkable: {closest_item['walkable']}\n"
                            f"Destroy_on_impact: {closest_item['destroy_on_impact']}\n"
                            f"Damage: {closest_item['damage']}\n"
                            f"Gold: {closest_item['gold']}\n"
                            f"Xp: {closest_item['xp']}"
                        )

            keys = pygame.key.get_pressed()
            move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * crossbar.speed
            move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * crossbar.speed
            move_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5*crossbar.speed
            move_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5*crossbar.speed

            crossbar.x += move_x
            crossbar.y += move_y

            # Bordering:
            if crossbar.x <= border["XLeft"]:
                crossbar.x = border["XLeft"]
            if crossbar.x >= border["XRight"] - crossbar.size:
                crossbar.x = border["XRight"] - crossbar.size
            if crossbar.y <= border["YTop"]:
                crossbar.y = border["YTop"]
            if crossbar.y >= border["YBottom"] - crossbar.size:
                crossbar.y = border["YBottom"] - crossbar.size


            # Drawing
            screen.fill(BG_COLOUR)

            # borders:
            pygame.draw.rect(screen, RED, (crossbar.relateX(border["XLeft"]), crossbar.relateY(0), 10, border["YBottom"]))
            pygame.draw.rect(screen, RED, (crossbar.relateX(border["XRight"] - 10), crossbar.relateY(0), 10, border["YBottom"]))
            pygame.draw.rect(screen, RED, (crossbar.relateX(0), crossbar.relateY(border["YTop"]), border["XRight"], 10))
            pygame.draw.rect(screen, RED, (crossbar.relateX(0), crossbar.relateY(border["YBottom"] - 10), border["XRight"], 10))

            for item_data in world_items.values():
                image = item_images[item_data["path"]]
                position = (crossbar.relateX(item_data["x"]), crossbar.relateY(item_data["y"]))
                screen.blit(image, position)
                image_rect = image.get_rect(topleft=position)
                pygame.draw.rect(screen, (0, 50, 0), image_rect, width=1)
                pygame.draw.rect(screen, (255, 0, 0), (crossbar.relateX(item_data["x"]), crossbar.relateY(item_data["y"]), 1, 1))

            crossbar.draw(screen)

            image = pygame.image.load(images[item_to_add]).convert_alpha()
            image.set_alpha(128)
            screen.blit(image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            pygame.draw.rect(screen, (152, 179, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2, width, height), width=1)
            pygame.display.flip()
            clock.tick(60)
    else:
        print("Info: item not found in images")



main()