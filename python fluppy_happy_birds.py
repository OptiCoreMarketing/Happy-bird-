import pygame
import sys
import random

# --- Initialiser pygame ---
pygame.init()

# --- Farver ---
HVID = (255, 255, 255)
SORT = (0, 0, 0)
RØD = (255, 0, 0)
GRØN = (0, 200, 0)
BLÅ = (0, 0, 255)
GUL = (255, 200, 0)

# --- Skærm ---
SKÆRM_STØRRELSE = (800, 600)
skærm = pygame.display.set_mode(SKÆRM_STØRRELSE)
pygame.display.set_caption("Fluppy Happy Birds")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32)
stor_font = pygame.font.SysFont("arial", 48)

# --- Konstanter for spillet ---
TYNGDEKRAFT = 0.5
HOP_STYRKE = -8
HINDER_FART = 4
HINDER_AFSTAND = 300  # pixels mellem hver forhindring
HINDER_ÅBNING = 180   # hvor stort et hul fuglen skal flyve igennem


class Fugl:
    def __init__(self):
        self.x = 100
        self.y = SKÆRM_STØRRELSE[1] // 2
        self.radius = 20
        self.farve = RØD
        self.hastighed_y = 0
        self.liv = 3

    def hop(self):
        self.hastighed_y = HOP_STYRKE

    def opdater(self):
        self.hastighed_y += TYNGDEKRAFT
        self.y += self.hastighed_y

        # Kan ikke flyve uden for skærmen (top/bund tæller som ramt)
        if self.y - self.radius < 0:
            self.y = self.radius
            self.hastighed_y = 0
        if self.y + self.radius > SKÆRM_STØRRELSE[1]:
            self.y = SKÆRM_STØRRELSE[1] - self.radius
            self.liv = 0  # ramte jorden

    def tegn(self):
        pygame.draw.circle(skærm, self.farve, (self.x, int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius,
            self.radius * 2, self.radius * 2
        )


class Hinder:
    """Et par af forhindringer (top + bund) med en åbning imellem, ligesom rør i Flappy Bird."""

    def __init__(self, x):
        self.x = x
        self.bredde = 60
        self.farve = GRØN
        self.passeret = False  # bruges til scoring
        self.top_højde = random.randint(50, SKÆRM_STØRRELSE[1] - HINDER_ÅBNING - 50)
        self.bund_y = self.top_højde + HINDER_ÅBNING

    def opdater(self):
        self.x -= HINDER_FART

    def er_uden_for_skærm(self):
        return self.x + self.bredde < 0

    def tegn(self):
        pygame.draw.rect(skærm, self.farve, (self.x, 0, self.bredde, self.top_højde))
        pygame.draw.rect(
            skærm, self.farve,
            (self.x, self.bund_y, self.bredde, SKÆRM_STØRRELSE[1] - self.bund_y)
        )

    def kolliderer_med(self, fugl_rect):
        top_rect = pygame.Rect(self.x, 0, self.bredde, self.top_højde)
        bund_rect = pygame.Rect(self.x, self.bund_y, self.bredde, SKÆRM_STØRRELSE[1] - self.bund_y)
        return fugl_rect.colliderect(top_rect) or fugl_rect.colliderect(bund_rect)


class PowerUp:
    def __init__(self):
        self.respawn()
        self.radius = 10
        self.farve = BLÅ

    def respawn(self):
        self.x = random.randint(400, SKÆRM_STØRRELSE[0] - 50)
        self.y = random.randint(50, SKÆRM_STØRRELSE[1] - 50)

    def opdater(self):
        self.x -= HINDER_FART  # flyder med samme fart som forhindringerne

    def tegn(self):
        pygame.draw.circle(skærm, self.farve, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


def ny_spil_tilstand():
    fugl = Fugl()
    hindre = [Hinder(SKÆRM_STØRRELSE[0] + i * HINDER_AFSTAND) for i in range(3)]
    power_up = PowerUp()
    return fugl, hindre, power_up, 0  # sidste værdi = score


def tegn_tekst(tekst, font, farve, x, y, centreret=False):
    overflade = font.render(tekst, True, farve)
    rect = overflade.get_rect()
    if centreret:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    skærm.blit(overflade, rect)


def main():
    fugl, hindre, power_up, score = ny_spil_tilstand()
    spillet_er_slut = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if spillet_er_slut:
                        fugl, hindre, power_up, score = ny_spil_tilstand()
                        spillet_er_slut = False
                    else:
                        fugl.hop()

        skærm.fill(HVID)

        if not spillet_er_slut:
            fugl.opdater()

            # Opdater forhindringer og tilføj nye når de forsvinder ud af skærmen
            for hinder in hindre:
                hinder.opdater()
            if hindre[0].er_uden_for_skærm():
                hindre.pop(0)
                ny_x = hindre[-1].x + HINDER_AFSTAND
                hindre.append(Hinder(ny_x))

            # Kollision med forhindringer
            fugl_rect = fugl.get_rect()
            for hinder in hindre:
                if hinder.kolliderer_med(fugl_rect):
                    fugl.liv -= 1
                    if fugl.liv <= 0:
                        spillet_er_slut = True

                # Score når fuglen passerer en forhindring
                if not hinder.passeret and hinder.x + hinder.bredde < fugl.x:
                    hinder.passeret = True
                    score += 1

            if fugl.liv <= 0:
                spillet_er_slut = True

            # Power-up
            power_up.opdater()
            if power_up.x < -50:
                power_up.respawn()
                power_up.x = SKÆRM_STØRRELSE[0] + 50
            if fugl_rect.colliderect(power_up.get_rect()):
                score += 10
                power_up.respawn()
                power_up.x = SKÆRM_STØRRELSE[0] + 50

        # --- Tegning ---
        for hinder in hindre:
            hinder.tegn()
        power_up.tegn()
        fugl.tegn()

        tegn_tekst(f"Score: {score}", font, SORT, 10, 10)
        tegn_tekst(f"Liv: {fugl.liv}", font, SORT, 10, 50)

        if spillet_er_slut:
            tegn_tekst(
                "Game Over!", stor_font, RØD,
                SKÆRM_STØRRELSE[0] // 2, SKÆRM_STØRRELSE[1] // 2 - 30, centreret=True
            )
            tegn_tekst(
                "Tryk MELLEMRUM for at spille igen", font, SORT,
                SKÆRM_STØRRELSE[0] // 2, SKÆRM_STØRRELSE[1] // 2 + 30, centreret=True
            )

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
