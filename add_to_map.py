import json
import os

buildings_path = "maps/Tiny Village Pack/Outdoors/Buildings"
buildings = {
    "House1_blue.png": (buildings_path + "/House1_blue.png"),
    "House1_green.png": (buildings_path + "/House1_green.png"),
    "House1_red.png": (buildings_path + "/House1_red.png"),
    "House1_spritesheet.png": (buildings_path + "/House1_spritesheet.png"),
    "House2_blue.png": (buildings_path + "/House2_blue.png"),
    "House2_green.png": (buildings_path + "/House2_green.png"),
    "House2_red.png": (buildings_path + "/House2_red.png"),
    "House2_spritesheet.png": (buildings_path + "/House2_spritesheet.png"),
    "House3_blue.png": (buildings_path + "/House3_blue.png"),
    "House3_green.png": (buildings_path + "/House3_green.png"),
    "House3_red.png": (buildings_path + "/House3_red.png"),
    "House3_spritesheet.png": (buildings_path + "/House3_spritesheet.png"),
    "House4_blue.png": (buildings_path + "/House4_blue.png"),
    "House4_green.png": (buildings_path + "/House4_green.png"),
    "House4_red.png": (buildings_path + "/House4_red.png"),
    "House4_spritesheet.png": (buildings_path + "/House4_spritesheet.png"),
    "Wooden_House1_blue.png": (buildings_path + "/Wooden_House1_blue.png"),
    "Wooden_House1_green.png": (buildings_path + "/Wooden_House1_green.png"),
    "Wooden_House1_red.png": (buildings_path + "/Wooden_House1_red.png"),
    "Wooden_House2_blue.png": (buildings_path + "/Wooden_House2_blue.png"),
    "Wooden_House2_green.png": (buildings_path + "/Wooden_House2_green.png"),
    "Wooden_House2_red.png": (buildings_path + "/Wooden_House2_red.png"),
    "Wooden_House3_blue.png": (buildings_path + "/Wooden_House3_blue.png"),
    "Wooden_House3_green.png": (buildings_path + "/Wooden_House3_green.png"),
    "Wooden_House3_red.png": (buildings_path + "/Wooden_House3_red.png"),
    "Wooden_House4_blue.png": (buildings_path + "/Wooden_House4_blue.png"),
    "Wooden_House4_green.png": (buildings_path + "/Wooden_House4_green.png"),
    "Wooden_House4_red.png": (buildings_path + "/Wooden_House4_red.png"),
}

def main():
    json_file = input("which json do you want to edit? world_items.json or inventory_item_pics.png: ")

    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
        print("file does not exitst yet")

    item_to_add = input("select the file name of the item to add: ")
    item_name = input("type a nickname for this item (that is not already used in the json as a key): ")
    if item_to_add in buildings:

        x = int(input("insert x value: "))
        y = int(input("insert y value: "))

        data[item_name] = {
            "path": buildings[item_to_add],
            "x": x,
            "y": y
        }

        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Successfully added '{item_to_add}' to {json_file}!")
    else:
        print("item not found in buildings")

    again = input("Dow you want to add another item or retry? Y/N: ")
    if again == "Y":
        main()

main()