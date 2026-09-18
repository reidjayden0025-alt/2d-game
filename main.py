import pygame


class Player:
    def __init__(self, x, y, speed, graphic):
        self.x = x
        self.y = y
        self.speed = speed
        self.graphic = graphic

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.graphic, self.graphic))


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOUR = (30, 30, 30)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeons of Dagestan")

clock = pygame.time.Clock()
player = Player(0, 0, 10, 20)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= player.speed
    if keys[pygame.K_d]:
        player.x += player.speed
    if keys[pygame.K_w]:
        player.y -= player.speed
    if keys[pygame.K_s]:
        player.y += player.speed

    screen.fill(BG_COLOUR)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()