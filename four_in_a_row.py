import pygame
import sys
import random
import math

# Inicijalizacija Pygame-a
pygame.init()

# Konstante
BROJ_REDOVA = 6
BROJ_KOLONA = 7
IGRAC = 1
KOMPJUTER = 2
PRAZNO = 0
VELICINA_KVADRATA = 100
POLUPRECNIK = int(VELICINA_KVADRATA / 2 - 5)
sirina = BROJ_KOLONA * VELICINA_KVADRATA
visina = (BROJ_REDOVA + 1) * VELICINA_KVADRATA
velicina = (sirina, visina)
PLAVA = (0, 0, 255)
CRNA = (0, 0, 0)
CRVENA = (255, 0, 0)
ZUTA = (255, 255, 0)

# Inicijalizacija ekrana
ekran = pygame.display.set_mode(velicina)

# Fontovi
moj_font = pygame.font.SysFont("monospace", 75)

# Funkcije igre
def kreiraj_tablu():
    # Kreiranje table
    tabla = [[0 for _ in range(BROJ_KOLONA)] for _ in range(BROJ_REDOVA)]
    return tabla

def postavi_zeton(tabla, red, kol, zeton):
    # Postavljanje žetona na tablu
    tabla[red][kol] = zeton

def validna_lokacija(tabla, kol):
    # Provera da li je kolona validna za potez
    return tabla[0][kol] == 0

def sledeci_slobodan_red(tabla, kol):
    # Pronalaženje sledećeg slobodnog reda u koloni
    for r in range(BROJ_REDOVA - 1, -1, -1):
        if tabla[r][kol] == 0:
            return r

def ispisi_tablu(tabla):
    # Ispis table u konzoli
    for red in tabla:
        print(red)

def pobednicki_potez(tabla, zeton):
    # Provera da li je trenutni potez pobednički
    for c in range(BROJ_KOLONA - 3):
        for r in range(BROJ_REDOVA):
            if all(tabla[r][c + i] == zeton for i in range(4)):
                return True

    for c in range(BROJ_KOLONA):
        for r in range(BROJ_REDOVA - 3):
            if all(tabla[r + i][c] == zeton for i in range(4)):
                return True

    for c in range(BROJ_KOLONA - 3):
        for r in range(BROJ_REDOVA - 3):
            if all(tabla[r + i][c + i] == zeton for i in range(4)):
                return True

    for c in range(BROJ_KOLONA - 3):
        for r in range(3, BROJ_REDOVA):
            if all(tabla[r - i][c + i] == zeton for i in range(4)):
                return True

def evaluiraj_prozor(prozor, zeton):
    # Evaluacija prozora od četiri polja
    skor = 0
    protivnik_zeton = IGRAC
    if zeton == IGRAC:
        protivnik_zeton = KOMPJUTER

    if prozor.count(zeton) == 4:
        skor += 100
    elif prozor.count(zeton) == 3 and prozor.count(PRAZNO) == 1:
        skor += 5
    elif prozor.count(zeton) == 2 and prozor.count(PRAZNO) == 2:
        skor += 2

    if prozor.count(protivnik_zeton) == 3 and prozor.count(PRAZNO) == 1:
        skor -= 4

    return skor

def evaluiraj_poziciju(tabla, zeton):
    # Evaluacija pozicije na tabli
    skor = 0

    centar_niz = [int(i) for i in list(map(lambda x: x[BROJ_KOLONA // 2], tabla))]
    broj_u_centru = centar_niz.count(zeton)
    skor += broj_u_centru * 3

    for r in range(BROJ_REDOVA):
        red_niz = tabla[r]
        for c in range(BROJ_KOLONA - 3):
            prozor = red_niz[c:c + 4]
            skor += evaluiraj_prozor(prozor, zeton)

    for c in range(BROJ_KOLONA):
        kol_niz = [tabla[r][c] for r in range(BROJ_REDOVA)]
        for r in range(BROJ_REDOVA - 3):
            prozor = kol_niz[r:r + 4]
            skor += evaluiraj_prozor(prozor, zeton)

    for r in range(BROJ_REDOVA - 3):
        for c in range(BROJ_KOLONA - 3):
            prozor = [tabla[r + i][c + i] for i in range(4)]
            skor += evaluiraj_prozor(prozor, zeton)

    for r in range(BROJ_REDOVA - 3):
        for c in range(BROJ_KOLONA - 3):
            prozor = [tabla[r + 3 - i][c + i] for i in range(4)]
            skor += evaluiraj_prozor(prozor, zeton)

    return skor

def cvor_kraja(tabla):
    # Provera da li je igra završena
    return pobednicki_potez(tabla, IGRAC) or pobednicki_potez(tabla, KOMPJUTER) or len(dobi_validnu_lokaciju(tabla)) == 0

def minimax(tabla, dubina, alfa, beta, max_igrac):
    # Minimax algoritam sa alfa-beta orezivanjem
    validne_lokacije = dobi_validnu_lokaciju(tabla)
    je_kraj = cvor_kraja(tabla)
    if dubina == 0 or je_kraj:
        if je_kraj:
            if pobednicki_potez(tabla, KOMPJUTER):
                return (None, 100000000000000)
            elif pobednicki_potez(tabla, IGRAC):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, evaluiraj_poziciju(tabla, KOMPJUTER))
    if max_igrac:
        vrednost = -math.inf
        kolona = random.choice(validne_lokacije)
        for kol in validne_lokacije:
            red = sledeci_slobodan_red(tabla, kol)
            b_copy = [red[:] for red in tabla]
            postavi_zeton(b_copy, red, kol, KOMPJUTER)
            new_score = minimax(b_copy, dubina - 1, alfa, beta, False)[1]
            if new_score > vrednost:
                vrednost = new_score
                kolona = kol
            alfa = max(alfa, vrednost)
            if alfa >= beta:
                break
        return kolona, vrednost

    else:
        vrednost = math.inf
        kolona = random.choice(validne_lokacije)
        for kol in validne_lokacije:
            red = sledeci_slobodan_red(tabla, kol)
            b_copy = [red[:] for red in tabla]
            postavi_zeton(b_copy, red, kol, IGRAC)
            new_score = minimax(b_copy, dubina - 1, alfa, beta, True)[1]
            if new_score < vrednost:
                vrednost = new_score
                kolona = kol
            beta = min(beta, vrednost)
            if alfa >= beta:
                break
        return kolona, vrednost

def dobi_validnu_lokaciju(tabla):
    # Dobijanje liste validnih lokacija za potez
    validne_lokacije = []
    for kol in range(BROJ_KOLONA):
        if validna_lokacija(tabla, kol):
            validne_lokacije.append(kol)
    return validne_lokacije

def odaberi_najbolji_potez(tabla, zeton):
    # Odabir najboljeg poteza za trenutnog igrača
    validne_lokacije = dobi_validnu_lokaciju(tabla)
    najbolji_skor = -10000
    najbolja_kolona = random.choice(validne_lokacije)

    for kol in validne_lokacije:
        red = sledeci_slobodan_red(tabla, kol)
        temp_tabla = [red[:] for red in tabla]
        postavi_zeton(temp_tabla, red, kol, zeton)
        skor = evaluiraj_poziciju(temp_tabla, zeton)
        if skor > najbolji_skor:
            najbolji_skor = skor
            najbolja_kolona = kol

    return najbolja_kolona

def nacrtaj_tablu(tabla):
    # Crtanje table
    for c in range(BROJ_KOLONA):
        for r in range(BROJ_REDOVA):
            pygame.draw.rect(ekran, PLAVA, (c * VELICINA_KVADRATA, r * VELICINA_KVADRATA + VELICINA_KVADRATA, VELICINA_KVADRATA, VELICINA_KVADRATA))
            pygame.draw.circle(ekran, CRNA, (int(c * VELICINA_KVADRATA + VELICINA_KVADRATA / 2), int(r * VELICINA_KVADRATA + VELICINA_KVADRATA + VELICINA_KVADRATA / 2)), POLUPRECNIK)
    
    for c in range(BROJ_KOLONA):
        for r in range(BROJ_REDOVA):
            if tabla[r][c] == IGRAC:
                pygame.draw.circle(ekran, CRVENA, (int(c * VELICINA_KVADRATA + VELICINA_KVADRATA / 2), int((r+1) * VELICINA_KVADRATA + VELICINA_KVADRATA / 2)), POLUPRECNIK)
            elif tabla[r][c] == KOMPJUTER:
                pygame.draw.circle(ekran, ZUTA, (int(c * VELICINA_KVADRATA + VELICINA_KVADRATA / 2), int((r+1) * VELICINA_KVADRATA + VELICINA_KVADRATA / 2)), POLUPRECNIK)
    pygame.display.update()

tabla = kreiraj_tablu()
kraj_igre = False
turn = 0  # 0 za igrača, 1 za AI

nacrtaj_tablu(tabla)

while not kraj_igre:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION and turn == 0:
            pygame.draw.rect(ekran, CRNA, (0, 0, sirina, VELICINA_KVADRATA))
            posx = event.pos[0]
            pygame.draw.circle(ekran, CRVENA, (posx, int(VELICINA_KVADRATA / 2)), POLUPRECNIK)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
            pygame.draw.rect(ekran, CRNA, (0, 0, sirina, VELICINA_KVADRATA))
            posx = event.pos[0]
            kol = int(posx // VELICINA_KVADRATA)

            if validna_lokacija(tabla, kol):
                red = sledeci_slobodan_red(tabla, kol)
                postavi_zeton(tabla, red, kol, IGRAC)

                if pobednicki_potez(tabla, IGRAC):
                    label = moj_font.render("Pobedio si", 1, CRVENA)
                    ekran.blit(label, (40, 10))
                    kraj_igre = True

                turn = 1
                nacrtaj_tablu(tabla)

    if turn == 1 and not kraj_igre:
        kol, minimax_score = minimax(tabla, 5, -math.inf, math.inf, True)

        if validna_lokacija(tabla, kol):
            red = sledeci_slobodan_red(tabla, kol)
            postavi_zeton(tabla, red, kol, KOMPJUTER)

            if pobednicki_potez(tabla, KOMPJUTER):
                label = moj_font.render("Izgubio si", 1, ZUTA)
                ekran.blit(label, (40, 10))
                kraj_igre = True

            turn = 0
            nacrtaj_tablu(tabla)

    if kraj_igre:
        pygame.time.wait(3000)
