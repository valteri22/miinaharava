'''
Globaalit sanakirjat sekä moduulit, joista peli on riippuvainen.
Sanakirjoihin peli tallentaa arvoja.
'''

import haravasto
import random
import time

tilastot = {
    "pelaajan_nimi": None, # Pelaajan nimi.
    "alue_x": 0, # Pelialueen leveys.
    "alue_y": 0, # Pelialueen korkeus.
    "uusi_peli": True, # Työkalu käsittelijäfunktioille, jolla aloittetaan uusi peli.
    "miinojen_lkm": 0, # Miinojen lukumäärä.
    "pelin_ajankohta": None, # Päivämäärä, kellonaika.
    "pelin_kesto": 0, # Pelin kesto minuutteina ja sekunteina.
    "vuorojen_lkm": 0, # Käytännössä kuinka monta kertaa pelaaja on avannut uuden ruudun.
    "tila": "Pause", # Pelin tila (Voitto, Tappio, Pause)
    "ruutuja_jaljella": 0, # Jäljellä olevat avaamattomat tyhjät ruudut.
    "end": False # Määrittää grafiikan piirtymisen: True = peli kiinni.
}

miinat_alueessa = {"alue": None} # Miinat kentällä

pelialue = {"alue": None} # Pelaajan näkemä kenttä



def pelialueen_koko():
    '''
    Pelaaja määrittää pelialueen leveyden ja korkeuden kokonaislukuina 
    (ruutuina). Tarkastaa myös syötteen oikeellisuuden.
    '''

    while True:
        try:
            leveys = int(input("Leveys (ruutua): "))
            korkeus = int(input("Korkeus (ruutua): "))
            return korkeus, leveys
        except ValueError:
            print("Virhe! Syötä leveys ja korkeus kokonaislukuina.")


def miinojen_lukumaara(alueen_koko):
    '''
    Pelaaja määrittää halutun määrän miinoja kokonaislukuina. Funktio päivittää 
    miinojen määrän tilastoihin. Tarkastaa myös syötteen oikeellisuuden
    ja miinojen määrän olevan mahdollinen.

    :param alueen_koko: pelialueen koko ruuduissa.
    '''

    while True:
        try:
            miinojen_maara = int(input("Miinat (lkm): "))
        except ValueError:
            print("Virhe! Syötä miinojen lukumäärä kokonaislukuna.")
        else:
            if 0 < miinojen_maara < alueen_koko:
                tilastot["miinojen_lkm"] = miinojen_maara
                return
            else:
                print("Virhe! Miinoja täytyy olla enemmän kuin 0, mutta vähemmän kuin ruutuja yhteensä.")


def piirra_alue():
    '''
    Piirtää pelin grafiikan käsittelemällä pelialueen listan. Funktiota kutsutaan, 
    kun peliruutu täytyy päivittää esim. ruutua klikatessa.
    '''

    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()

    solun_koko = 40

    for rivin_indeksi, rivi in enumerate(pelialue["alue"]):
        for sarakkeen_indeksi, value in enumerate(rivi):
            x_sijainti = sarakkeen_indeksi * solun_koko
            y_sijainti = rivin_indeksi * solun_koko
            haravasto.lisaa_piirrettava_ruutu(value, x_sijainti, y_sijainti)

    haravasto.piirra_ruudut()


def valinnat():
    '''
    Terminaaliin tulostuva valikko. Tarkistaa syötteen olevan kokonaisluku
    väliltä 1-3 ja syötteen olevan vain aktiviteettia vastaava luku.
    '''

    while True:
        print("\nValitse aktiviteetti:")
        print("1. Aloita")
        print("2. Tilastot")
        print("3. Lopeta")
        
        try:
            print()
            valinta = int(input("(1, 2 tai 3): "))
            print()
            if 1 <= valinta <= 3:
                return valinta
            else:
                print()
                print("Virhe! Vain numerot 1, 2 ja 3 ovat valittavissa.")
        except ValueError:
            print()
            print("Virhe! Anna pelkkä aktiviteettia vastaava numero.")



def luo_pelialue(ruudut):
    '''
    Päivittää sanakirjoihin pelialueen koon.

    :param ruudut: sisältää pelialueen koon
    '''

    miinat_alueessa["alue"] = [[" " for _ in range(ruudut[1])] for _ in range(ruudut[0])]
    pelialue["alue"] = [[" " for _ in range(ruudut[1])] for _ in range(ruudut[0])]


def miinoita(miinat, alue, alku):
    '''
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.

    :param miinat: miinojen lukumäärä
    :param alue: miinoitettava alue
    :param alku: ensimmäisenä avatun ruudun koordinaatit. Varmistaa, 
                 ettei siihen tule miinaa.
    '''

    tilastot["ruutuja_jaljella"] = len(alue) * len(alue[0]) - miinat

    viimeiset = set((x, y) for x in range(len(alue[0])) for y in range(len(alue)))
    viimeiset.discard(alku)

    for _ in range(miinat):
        if not viimeiset:
            break
        x, y = random.choice(list(viimeiset))
        viimeiset.remove((x, y))
        alue[y][x] = "x"


def tarkista_koordinaatit(x, y):
    '''
    Tarkistaa koordinaattien olevan pelialueella.

    :param x: x-koordinaatti
    :param y: y-koordinaatti
    '''

    return not (0 <= x < tilastot["alue_x"] and 0 <= y < tilastot["alue_y"])

def laske_miinat_ymparilla(x, y):
    '''
    Laskee miinojen lukumäärän solun ympärillä.

    :param x: x-koordinaatti
    :param y: y-koordinaatti
    '''

    miinojen_lkm = 0
    for i in range(max(0, x - 1), min(tilastot["alue_x"], x + 2)):
        for j in range(max(0, y - 1), min(tilastot["alue_y"], y + 2)):
            if miinat_alueessa["alue"][j][i] == 'x':
                miinojen_lkm += 1
    return miinojen_lkm

def paljasta_vierus(x, y):
    '''
    Tekee tarvittavat laskut ja paljastaa solun viereiset solut funktiota kutsuttaessa.

    :param x: x-koordinaatti
    :param y: y-koordinaatti
    '''

    for i in range(max(0, x - 1), min(tilastot["alue_x"], x + 2)):
        for j in range(max(0, y - 1), min(tilastot["alue_y"], y + 2)):
            paljasta_solu(i, j)

def paljasta_solu(x, y):
    '''
    Paljastaa solun sitä klikattaessa. Tarkastaa koordinaattien oikeellisuuden,
    laskee miinat, päivittää tilastot ja kutsuu paljasta_vierus-funktiota mikäli
    klikatun solun ympärillä ei ole miinoja.

    :param x: x-koordinaatti
    :param y: y-koordinaatti
    '''

    if tarkista_koordinaatit(x, y) or pelialue["alue"][y][x] != " ":
        return

    miinojen_lkm = laske_miinat_ymparilla(x, y)

    pelialue["alue"][y][x] = str(miinojen_lkm)
    tilastot["ruutuja_jaljella"] -= 1

    if miinojen_lkm == 0:
        paljasta_vierus(x, y)

def kasittele_tyhja_solu(x, y):
    '''
    Mikäli peli on uusi, kutsuu miinoita-funktiota. Paljastaa solun kutsumalla
    sen funktiota. Laskee vuorojen lukumäärän ja kutsuu voiton käsittelevää funktiota
    mikäli ruutuja on jäljellä 0.

    :param x: x-koordinaatti
    :param y: y-koordinaatti
    '''

    if tilastot["uusi_peli"]:
        miinoita(tilastot["miinojen_lkm"], miinat_alueessa["alue"], (x, y))
        tilastot["uusi_peli"] = False
    paljasta_solu(x, y)
    haravasto.aseta_piirto_kasittelija(piirra_alue)
    tilastot["vuorojen_lkm"] += 1
    if tilastot["ruutuja_jaljella"] == 0:
        kasittele_voitto()


def kasittele_tappio(x, y):
    '''
    Funktiota kutsutaan, jos pelaaja häviää pelin klikkaamalla miinasta.
    Päivittää myös häviöön liittyvät tilastot.

    :param x: x-koordinaatti
    :param y: y-koordinaatti
    '''

    tilastot["tila"] = "Tappio"
    pelialue["alue"][y][x] = "x"
    haravasto.aseta_piirto_kasittelija(piirra_alue)
    tilastot["end"] = True
    print("Hävisit!")

def kasittele_voitto():
    '''
    Käsittelee voiton ja päivittää tilastot.
    '''

    tilastot["tila"] = "Voitto"
    tilastot["end"] = True
    print("Voitit!")



def kasittele_hiiri(x, y, button, _):
    '''
    Käsittelee hiiren pelissä. Kutsuu hiiren vasemman tai oikean
    käsittelevää funktiota niitä painettaessa.

    :param x: Klikattu x-arvo.
    :param y: Klikattu y-arvo.
    :param button: Painettu hiiren painike.
    '''

    solun_koko = 40
    x //= solun_koko
    y //= solun_koko

    if x >= tilastot["alue_x"]:
        x -= 1
    if y >= tilastot["alue_y"]:
        y -= 1

    if tilastot["end"]:
        haravasto.lopeta()
        return

    if button == haravasto.HIIRI_VASEN:
        kasittele_hiiri_vasen(x, y)
    elif button == haravasto.HIIRI_OIKEA:
        kasittele_hiiri_oikea(x, y)

def kasittele_hiiri_vasen(x, y):
    '''
    Funktiota kutsutaan, kun hiiren vasenta klikataan. Mikäli pelaaja
    klikkaa miinasta, kutsutaan funktiota, jossa häviö käsitellään. Mikäli
    pelaaja klikkaa tyhjästä solusta, kutsutaan funktiota, jossa tyhjä solu
    käsitellään.

    :param x: Klikattu x-arvo.
    :param y: Klikattu y-arvo.
    '''

    if miinat_alueessa["alue"][y][x] == "x" and pelialue["alue"][y][x] != "f":
        kasittele_tappio(x, y)
    elif miinat_alueessa["alue"][y][x] == " " and pelialue["alue"][y][x] != "f":
        kasittele_tyhja_solu(x, y)

def kasittele_hiiri_oikea(x, y):
    '''
    Funktiota kutsutaan, kun hiiren oikeaa klikataan. Tällöin se asettaa tai poistaa lipun.

    :param x: Klikattu x-arvo.
    :param y: Klikattu y-arvo.
    '''

    if pelialue["alue"][y][x] == " ":
        pelialue["alue"][y][x] = "f"
    elif pelialue["alue"][y][x] == "f":
        pelialue["alue"][y][x] = " "
    haravasto.aseta_piirto_kasittelija(piirra_alue)



def tulokset(tila, tilastot):
    '''
    Tallentaa tai lukee pelin tulokset tekstitiedostoon/tiedostosta.
    Tarkistaa löytyykö tiedostoa jossa tulokset sijaitsevat.

    :param tila: export/import (tulosten tallennus tai lukeminen)
    :param tilastot: tilastot
    '''

    tiedoston_sijainti = "tulokset_miinaharava_2023.txt"

    try:
        with open(tiedoston_sijainti, "a" if tila == "export" else "r") as kohdetiedosto:
            if tila == "export":
                aika = time.strftime("%d.%m.%Y %H:%M", time.localtime(tilastot["pelin_ajankohta"]))
                minuutit, sekunnit = divmod(tilastot["pelin_kesto"], 60)
                pyorista_sekunnit = round(sekunnit, 2)
                kohdetiedosto.write(f"{tilastot['pelaajan_nimi']},{aika},{minuutit},{pyorista_sekunnit},{tilastot['vuorojen_lkm']},"
                                    f"{tilastot['alue_x']},{tilastot['alue_y']},{tilastot['miinojen_lkm']},{tilastot['tila']}\n")
            elif tila == "import":
                content = kohdetiedosto.read()
                if content:
                    for line in content.splitlines():
                        lista = line.split(",")
                        print()
                        print(f"{lista[0]}, {lista[1]}")
                        print(f"Kesto: {lista[2]} minuuttia {lista[3]} sekuntia.")
                        print(f"Alue: {lista[5]}x{lista[6]}.")
                        print(f"Miinoja: {lista[7]}.")
                        print(f"Tulos: {lista[8]} {lista[4]}. vuorolla.")
                else:
                    print("Ei tuloksia.")
    except FileNotFoundError:
        print(f"Virhe! Tiedostoa ei löytynyt: {tiedoston_sijainti}")
    except IOError as e:
        print(f"Virhe {tila} tulokset: {e}")
    except Exception as e:
        print(f"Odottamaton virhe tapahtui: {e}")



if __name__ == "__main__":
    # Kutsutaan pelin logiikan ja grafiikan funktioita ja käsitellään tietoja.
    # Päivitetään sanakirjoja.

    # ladataan spritet.

    print("Miinaharava 2023")
    print()
    tilastot["pelaajan_nimi"] = input("Nimesi?: ")

    while True:
        valinta = valinnat()

        if valinta == 1:
            tilastot.update({
                "uusi_peli": True,
                "miinojen_lkm": 0,
            })

            ruudukon_koko = pelialueen_koko()
            tilastot.update({
                "alue_x": ruudukon_koko[1],
                "alue_y": ruudukon_koko[0],
            })

            miinojen_lukumaara(ruudukon_koko[0] * ruudukon_koko[1])
            luo_pelialue(ruudukon_koko)

            haravasto.lataa_kuvat("spritet")
            haravasto.luo_ikkuna(ruudukon_koko[1] * 40, ruudukon_koko[0] * 40)
            haravasto.aseta_piirto_kasittelija(piirra_alue)
            haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)

            tilastot.update({
                "pelin_ajankohta": time.time(),
                "pelin_kesto": 0,
                "vuorojen_lkm": 0,
                "tila": "Pause",
            })

            haravasto.aloita()
            tilastot["pelin_kesto"] = time.time() - tilastot["pelin_ajankohta"]
            tulokset("export", tilastot)
            tilastot["end"] = False

        elif valinta == 2:
            print("Tulokset: ")
            tulokset("import", tilastot)

        else:
            break
