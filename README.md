# 2d-game
Name: Dungeons of Dagestan

Description: Dungeons of Dagestan is a massive, walkabout, 2d adventure game where you complete quests and 


Controls:
| Key | Binding|
|---|---|
| W | Up |
| A | Left |
| S | Down |
| D | Right |

Dependencies:
| Dependency | Link / Terminal Download |
|---|---|
| Python | https://python.org/downloads |
| Pygame | pip install pygame |
| Pillow/PIL | pip install Pillow |

developers:
| Developer | Credit |
|---|---|
| <ins>Jayden Reid</ins> | Lead developer / Art / Animations |
| <ins>Johan Hardick</ins> | Lead backend developer / kinetics |

---

> Dev Note to JAYDEN:

when adding a structure at a random coordinate make sure that it's x and y are plugged through the player.relateX() and player.relateY() functions as follows:
pygame.draw.rect(screen, (255, 0, 0), (player.relateX((((X)))), player.relateY((((Y)))), 10, 10))

the player.relate functions do the following:

    def relateX(self, x):
        X = x + SCREEN_WIDTH/2 - self.x
        return X
        
    def relateY(self, y):
        Y = y + SCREEN_HEIGHT/2 - self.y
        return Y
I did some sketches in a book to simulate what would happen if I anchored the player in the center of the screen and i wrote down what would happen to other objects relative to the anchored player. I used my observations to form these functions. Hence the names "relateX" and "relateY". whenever you have the x or y values of a specific object on the map just pump their coordinates through these functions first to ensure that they move relatively to the anchored player.

>> <sub>(In simple english) if you have an x and y put them though the "relate" functions before drawing them.</sub>


> Dev Note:

I have introduced an easy system for adding the images to the screen. I have added a for loop in the game loop that accesses a json file that holds the paths to specific image files and holds their coordinates on the game map. this loop is just the end of a beautiful process used to add images to the map easily. the loop looks like this:

    for item_name, item_data in world_items.items():
        screen.blit(item_images[item_name], (player.relateX(item_data["x"]), player.relateY(item_data["y"])),)

and the dictionsry that it refers to is declared earlier like this:

    with Path("world_items.json").open(encoding="utf-8") as items_file:
        world_items = json.load(items_file)

    item_images = {
        item_name: pygame.image.load(item_data["path"]).convert_alpha()
        for item_name, item_data in world_items.items()
    }

this basically takes all the data that the json stores and stores it so that the game loop can access it and show all of those coordinates and images on the map.

The json looks somewhat like this:

    {
        "H4Red": {
            "path": "maps/Tiny Village Pack/Outdoors/Buildings/House4_red.png",
            "x": 200,
            "y": 200,
            "width": 80,
            "height": 80,
            "walkable": false
        },
        "WH4Red": {
            "path": "maps/Tiny Village Pack/Outdoors/Buildings/Wooden_House4_red.png",
            "x": 200,
            "y": 400,
            "width": 80,
            "height": 80,
            "walkable": true
        }
    }

but this looks tedius to uphold, and it is. that is why i have also added a file (called <ins>add_to_map.py</ins>) that allows you to add an image straight from the terminal. the way in which it works is simple and here is a simple demonstration below:

    python add_to_map.py
    Input: which json do you want to edit? world_items.json or inventory_item_pics.png:    world_items.json
    Input: select the file name of the item to add:    Other:mailbox.png
    Input: type a nickname for this item (that is not already used in the json as a key):    Mailbox0
    Input: Should the player be able to walk over the object? Y/N:    N
    Input: insert x value:    200
    Input: insert y value:    290
    Info: Image dimensions: (16x16)
    Info: Successfully added 'Other:mailbox.png' to world_items.json!
    Input: Do you want to add another item or retry? Y/N: N