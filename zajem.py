import re
import orodja
import requests

def zajemi():
    for id in range(1, 401):
        osnovno = 'https://www.kulinarika.net/recepti/'
        naslov = ('{}{}'.format(osnovno, id))
        datoteka = 'Recepti/{:03}.html'.format(id)
        orodja.shrani(naslov, datoteka)


def pocisti(recept):
    podatki = recept.groupdict()
    podatki['ime_recepta'] = str(podatki['ime_recepta'])
    podatki['ime_uporabnika'] = str(podatki['ime_uporabnika'])
    podatki['leto'] = int(podatki['leto'])
    podatki['mesec'] = int(podatki['mesec'])
    podatki['dan'] = int(podatki['dan'])
    podatki['cas_priprave'] = str(podatki['cas_priprave'])
    return podatki

regex_recepta = re.compile(
    #r'<title>Recept: (?P<ime_recepta>(.*?))</title>.*?'
    r"itemprop='author'>(?P<ime_uporabnika>(.*?))<.*?"
    r"itemprop='datePublished'>(?P<dan>(\d{1,2})).(?P<mesec>(\d{1,2})).(?P<leto>(\d{4}))</span.*?"
    #r'''itemprop='datePublished'>(?P<dan>(\d{1,2})).(?P<mesec>(\d{1,2})).(?P<leto>(\d{4}))</span.*?'''
        #r'''<span class='cas'>(?P<cas_priprave>)'''
        , flags=re.DOTALL
        )


def izloci_podatke(imenik):
    recepti = []
    for html_datoteka in orodja.datoteke(imenik):
        print(orodja.vsebina_datoteke(html_datoteka))
        for recept in re.finditer(regex_recepta, orodja.vsebina_datoteke(html_datoteka)):
            print('     *')
            recepti.append(pocisti(recept))
    return recepti

# Zajemi se kliče samo enkrat, potem so html datoteke že v mapi in te funkcije ne potrebujemo več.
# zajemi()


#recepti = izloci_podatke('Recepti/')
#orodja.zapisi_tabelo(recepti, ['ime_uporabnika', 'leto', 'mesec'], 'test.csv')

vsebina1 = orodja.vsebina_datoteke('Recepti/001.html')

for x in re.finditer(regex_recepta, vsebina1):
    print(x)

# =================== K O N E C   D O K U M E N T A ============================
#             print(potres.group('id'))
