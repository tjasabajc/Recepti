import re
import orodja
import requests

def zajemi_recepte():
    for id in range(20002, 20401):
        osnovno = 'https://www.kulinarika.net/recepti/'
        naslov = ('{}{}'.format(osnovno, id))
        datoteka = 'Recepti/{:03}.html'.format(id)
        orodja.shrani(naslov, datoteka)

def zajemi_uporabnike():
    for i in range(1, 10):
        osnovno = 'https://www.kulinarika.net/uporabniki/seznam/?offset'
        naslov = ('{}={}'.format(osnovno, (i-1)*20))
        datoteka = 'Uporabniki/{:02}.html'.format(i)
        orodja.shrani(naslov, datoteka)
        
def zajemi_ocene():
    with open('CSV/zajemi_ocene.csv','r') as f:
        for naslov in f.readlines():
            i = naslov.index('=')
            id = naslov[i+1:i+6]
            print(id)
            print(naslov)
            datoteka = 'Ocene/{}.html'.format(str(id))
            orodja.shrani(naslov, datoteka)

def pocisti(recept,datoteka):
    podatki = recept.groupdict()
    podatki['id'] = str(datoteka)
##    podatki['ime_recepta'] = str(podatki['ime_recepta'])
##    podatki['ime_uporabnika'] = str(podatki['ime_uporabnika'])
##    podatki['naziv1'] = str(podatki['naziv1'])
##    podatki['naziv2'] = str(podatki['naziv2'])
##    podatki['leto'] = int(podatki['leto'])
##    podatki['mesec'] = int(podatki['mesec'])
##    podatki['dan'] = int(podatki['dan'])
##    podatki['cas_priprave'] = str(podatki['cas_priprave'])
    podatki['ocena'] = int(podatki['ocena'])
##    podatki['stevilo_mnenj'] = int(podatki['stevilo_mnenj'])
##    podatki['navodilo'] = str(podatki['navodilo'])
##    podatki['vrsta_jedi'] = str(podatki['vrsta_jedi'])
##    podatki['kolicina'] = str(podatki['kolicina'])
##    podatki['sestavina'] = str(podatki['sestavina'])
##    podatki['priloznost'] = str(podatki['priloznost'])
##    podatki['one'] = str(podatki['one'])
##    podatki['two'] = str(podatki['two'])
##    podatki['three'] = str(podatki['three'])
##    podatki['four'] = str(podatki['four'])
##    podatki['five'] = str(podatki['five'])
    podatki['stevilo_ocen'] = int(podatki['stevilo_ocen'])
    podatki['link'] = str(podatki['link'])
    return podatki

regex_recepta = re.compile(
##    r'<title>Recept: (?P<ime_recepta>(.*?))</title>.*?'
##    r"itemprop='author'>(?P<ime_uporabnika>(.*?))<.*?"
##    r"itemprop='datePublished'>(\d{1,2}).(\d{1,2}).(\d{4})</span.*?"
##    r"itemprop='datePublished'>(?P<dan>(\d{1,2})).(?P<mesec>(\d{1,2})).(?P<leto>(\d{4}))</span.*?"
##    r"</span><span class='after1'>priložnost: (?P<priloznost>(.*?))</span>.*?"
##    r"<span class='cas'>(?P<cas_priprave>(.*?))</span>.*?"
##    r"<span class='tiptip' title='1 ocena'> povprečna ocena: <a href='/baze/popup-ocene.asp?ID=1' id='popup-oceneseznam-holder'><span itemprop='ratingvalue'>(?P<ocena>(\d{1}))</span></a></span><span itemprop='reviewcount'>(?P<stevilo_mnenj>(\d{1}))</span>.*?"
##    r'''<p class="cf" itemprop="recipeInstructions"><span class="label"></span><span class="fullwidth data">(?P<navodilo>(.*?))</span></p>.*?'''
##    r"<span itemprop='recipeCategory' style='display:none'>(?P<vrsta_jedi>(.*?))</span>.*?"
##    r'''<p class="cf" itemprop="recipeIngredient"><span class="label">(?P<kolicina>(.*?))</span><span class="label-value">(?P<sestavina>(.*?))</span>'''
##    r'''<li class='zahtevnost'><img src='/grafika6/ikona-(?P<one>(.*?)).png' alt='Zahtevnost' title='zahtevnost'><img src='/grafika6/ikona-(?P<two>(.*?)).png' alt='Zahtevnost' title='zahtevnost'><img src='/grafika6/ikona-(?P<three>(.*?)).png' alt='Zahtevnost' title='zahtevnost'><img src='/grafika6/ikona-(?P<four>(.*?)).png' alt='Zahtevnost' title='zahtevnost'><img src='/grafika6/ikona-(?P<five>(.*?)).png' alt='Zahtevnost' title='zahtevnost'></li>'''
##    r'''<h3 class='username'><a class='username' href='.*?'>(?P<ime_uporabnika>(.*?))</a></h3><p class='skor'><span class='bold'>(?P<naziv1>(.*?))</span> ((?P<naziv2>(.*?)))</p><p class='username'>Član od: <span class='bold'>(?P<dan>(\d{1,2})).(?P<mesec>(\d{1,2})).(?P<leto>(\d{4}))</span>.*?'''
    r'''<span class='tiptip' title='.*?'> povprečna ocena: <a href='(?P<link>(.*?))' id='popup-oceneseznam-holder'><span itemprop='ratingvalue'>(?P<ocena>(\d{1}))</span></a></span><span itemprop='reviewcount'>(?P<stevilo_ocen>(\d{1,2}))</span>.*?'''
        , flags=re.DOTALL
        )


def izloci_podatke(imenik):
    recepti = []
    for html_datoteka in orodja.datoteke(imenik):
        #print(orodja.vsebina_datoteke(html_datoteka))
        for recept in re.finditer(regex_recepta, orodja.vsebina_datoteke(html_datoteka)):
            #print('     *')
            recepti.append(pocisti(recept,html_datoteka))
    return recepti

# Zajemi se kliče samo enkrat, potem so html datoteke že v mapi in te funkcije ne potrebujemo več.
# zajemi_recepte()
# zajemi_uporabnike()
#zajemi_ocene()


#recepti = izloci_podatke('Recepti/')
#orodja.zapisi_tabelo(recepti, ['id','ocena','stevilo_ocen','link'], 'CSV/ocene.csv')

#uporanbiki = izloci_podatke('Uporabniki/')
#orodja.zapisi_tabelo(uporanbiki, ['id','ocena','stevilo_ocen','link'], 'CSV/kaj.csv')

vsebina1 = orodja.vsebina_datoteke('Recepti/20010.html')

for x in re.finditer(regex_recepta, vsebina1):
    print(x)
def pripravi():
    with open('CSV/zajemi_ocene.csv','r') as f:
        for naslov in f.readlines():
            print('orodja.shrani('+"'{}'".format(naslov)+', '+"'Ocene/{}.html'".format(naslov[-6:-1]) + ')')
pripravi()
    
    
# =================== K O N E C   D O K U M E N T A ============================
#             print(potres.group('id'))
