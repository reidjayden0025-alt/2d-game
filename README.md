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


NOTE: make the speed a variable if u need help i can show you my old code, we can do this so that it is easily adjusted and we can make items that increse or decrease speed. Also make the movement four way not eight, this will create a better vibe in the game and will work much better with my animations