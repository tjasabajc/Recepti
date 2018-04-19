import re
import orodja
import requests

def zajemi():
    for id in range(1, 30):
        osnovno = 'https://www.kulinarika.net/recepti/'
        naslov = ('{}{}'.format(osnovno, id))
        datoteka = 'Recepti/{:02}.html'.format(id)
        orodja.shrani(naslov, datoteka)


def pocisti(potres):
    podatki = potres.groupdict()
    podatki['ime_uporabnika'] = str(podatki['ime_uporabnika'])
    podatki['leto'] = int(podatki['leto'])
    podatki['mesec'] = int(podatki['mesec'])
    podatki['dan'] = int(podatki['dan'])
    return podatki

regex_potresa = re.compile(
        r''''<div class='podatki linki'>'''
        r'''itemprop='author'>(?P<ime_uporabnika>)<'''
        r'''itemprop='datePublished'>(?P<dan>(\d{2})).(?P<mesec>(\d{1,2}))-(?P<leto>(\d{4})).*?'''
        , flags=re.DOTALL
        )


def izloci_podatke(imenik):
    potresi = []
    for html_datoteka in orodja.datoteke(imenik):
        for potres in re.finditer(regex_potresa, orodja.vsebina_datoteke(html_datoteka)):
            potresi.append(pocisti(potres))
    return potresi

potresi = izloci_podatke('Recepti/')
orodja.zapisi_tabelo(potresi, ['ime_uporabnika', 'leto', 'mesec', 'dan'], 'receptitest.csv')

# =================== K O N E C   D O K U M E N T A ============================
#             print(potres.group('id'))
