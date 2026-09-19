import json
import os
from pathlib import Path
from PIL import Image

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

    "Other:bench.png": ("maps/Tiny Village Pack/Outdoors/Other/bench.png"),
    "Other:mailbox.png": ("maps/Tiny Village Pack/Outdoors/Other/mailbox.png"),
    "Other:sign.png": ("maps/Tiny Village Pack/Outdoors/Other/sign.png"),
    "Other:sign_2_left.png": ("maps/Tiny Village Pack/Outdoors/Other/sign_2_left.png"),
    "Other:sign_2_right.png": ("maps/Tiny Village Pack/Outdoors/Other/sign_2_right.png"),
    "Other:streetlight.png": ("maps/Tiny Village Pack/Outdoors/Other/streetlight.png"),
    "Sword": "maps/Inventory Ui items/Rusty Sword.png"

}


def main():
    json_file = input("Input: which json do you want to edit? world_items.json or inventory_item_pics.png:    ")

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

        x = int(input("Input: insert x value:    "))
        y = int(input("Input: insert y value:    "))

        damage = input("Input: How much damamge does the charechter take when coming into contact with this object? 0 if none:    ")
        gold  = input("Input: How much gold is this item when picked up? 0 if not gold:    ")
        xp = input("Input: How much xp is this item when picked up? 0 if not xp:    ")

        with Image.open(images[item_to_add]) as img:
            width, height = img.size
            print(f"Info: Image dimensions: ({width}x{height})")

        data[item_name] = {
            "path": images[item_to_add],
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
    else:
        print("Info: item not found in images")

    again = input("Input: Do you want to add another item or retry? Y/N: ")
    if again == "Y":
        main()

main()