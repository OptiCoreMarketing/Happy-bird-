import pygame
import sys
import random

# Initialiser pygame
pygame.init()

# Definerer nogle farver
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Sætter skærmens størrelse
SKÆRM_STØRRELSE = (800, 600)
skærm = pygame.display.set_mode(SKÆRM_STØRRELSE)

# Sætter titlen på spillet
pygame.display.set_caption("Fluppy Happy Birds")

# Definerer fuglene
class Fugl:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.bredde = 50
        self.højde = 50
        self.farve = RED
        self.fart = 1
        self.liv = 3

    def tegn(self):
        pygame.draw.rect(skærm, self.farve, (self.x, self.y, self.bredde, self.højde))

    def flyt(self):
        self.x += self.fart
        if self.x > SKÆRM_STØRRELSE[0]:
            self.x = 0

# Definerer hinderne
class Hinder:
    def __init__(self):
        self.x = random.randint(0, SKÆRM_STØRRELSE[0])
        self.y = random.randint(0, SKÆRM_STØRRELSE[1])
        self.bredde = 50
        self.højde = 50
        self.farve = GREEN

    def tegn(self):
        pygame.draw.rect(skærm, self.farve, (self.x, self.y, self.bredde, self.højde))

# Definerer power-up'erne
class PowerUp:
    def __init__(self):
        self.x = random.randint(0, SKÆRM_STØRRELSE[0])
        self.y = random.randint(0, SKÆRM_STØRRELSE[1])
        self.bredde = 20
        self.højde = 20
        self.farve = BLUE

    def tegn(self):
        pygame.draw.rect(skærm, self.farve, (self.x, self.y, self.bredde, self.højde))

# Opretter en fugl, et hinder og en power-up
fugl = Fugl()
hinder = [Hinder() for _ in range(5)]
power_up = PowerUp()

# Opretter en score-tæller
score = 0

# Hovedloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Tegner baggrunden
    skærm.fill(WHITE)

    # Flytter og tegner fuglen
    fugl.flyt()
    fugl.tegn()

    # Tegner hinderne
    for hinder in hinder:
        hinder.tegn()
        if fugl.x + fugl.bredde > hinder.x and fugl.x < hinder.x + hinder.bredde and fugl.y + fugl.højde > hinder.y and fugl.y < hinder.y + hinder.højde:
            fugl.liv -= 1
            if fugl.liv == 0:
                print("Game over! Din score var:", score)
                pygame.quit()
                sys.exit()

    # Tegner power-up'erne
    power_up.tegn()
    if fugl.x + fugl.bredde > power_up.x and fugl.x < power_up.x + power_up.bredde and fugl.y + fugl.højde > power_up.y and fugl.y < power_up.y + power_up.højde:
        score += 10
        power_up.x = random.randint(0, SKÆRM_STØRRELSE[0])
        power_up.y = random.randint(0, SKÆRM_STØRRELSE[1])

    # Opdaterer skærmen
    pygame.display.flip()
    pygame.time.Clock().tick(60)

    # Øger scoren hvis fuglen flyver forbi et bestemt punkt på skærmen
    if fugl.x > SKÆRM_STØRRELSE[0] // 2:
        score += 1