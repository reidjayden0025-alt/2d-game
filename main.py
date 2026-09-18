import pygame


class Player:
    def __init__(self, x, y, speed, health, graphic):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.graphic = graphic
        self.font = pygame.font.SysFont("arial", 32)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2, self.graphic, self.graphic))

    def drawstats(self, screen):
        text_surface = self.font.render(f"Health: {self.health}", True, WHITE)
        text_rect = text_surface.get_rect(topleft=(20, 20))
        screen.blit(text_surface, text_rect)

    def relateX(self, x):
        X = x + SCREEN_WIDTH/2 - self.x
        return X
    
    def relateY(self, y):
            Y = y + SCREEN_HEIGHT/2 - self.y
            return Y

    def damage(self, damn):
        self.health -= damn

border = {
    "XLeft": 0,
    "XRight": 3200,
    "YTop": 0,
    "YBottom": 1600,
}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOUR = (30, 30, 30)
WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeons of Dagestan")

clock = pygame.time.Clock()
player = Player(15, border["YBottom"]/2, 10, 100, 20)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controlls:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= player.speed
    if keys[pygame.K_d]:
        player.x += player.speed
    if keys[pygame.K_w]:
        player.y -= player.speed
    if keys[pygame.K_s]:
        player.y += player.speed

    # Bordering:
    if player.x <= border["XLeft"]:
        player.x = border["XLeft"]
    if player.x >= border["XRight"] - player.graphic:
        player.x = border["XRight"] - player.graphic
    if player.y <= border["YTop"]:
        player.y = border["YTop"]
    if player.y >= border["YBottom"] - player.graphic:
        player.y = border["YBottom"] - player.graphic

    screen.fill(BG_COLOUR)

    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(400), player.relateY(0), 10, 10))

    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(border["XLeft"]), player.relateY(0), 10, border["YBottom"]))
    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(border["XRight"] - 10), player.relateY(0), 10, border["YBottom"]))
    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(0), player.relateY(border["YTop"]), border["XRight"], 10))
    pygame.draw.rect(screen, (255, 0, 0), (player.relateX(0), player.relateY(border["YBottom"] - 10), border["XRight"], 10))

    player.drawstats(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()