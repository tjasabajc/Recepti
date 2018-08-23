import csv
import webbrowser

#UPORABNIKI
##with open('SQL/naredi_sql_uporabniki1.txt','w') as g:
##    with open('CSV/uporabniki.csv','r') as f:
##        for vrstica in f.readlines():
##            if vrstica != '\n':
##                ime_uporabnika,naziv1,naziv2,dan,mesec,leto = vrstica.split(',')
##                leto = leto[:-1]
##                if ime_uporabnika != 'ď»żime_uporabnika':
##                    datum = '{}.{}.{}'.format(int(dan),int(mesec),int(leto))
##                    opis = '{}, {}'.format(naziv1, naziv2)
##                    text = 'INSERT INTO uporabnik (ime, datum, opis) VALUES (\'{}\',\'{}\',\'{}\');\n'.format(ime_uporabnika, datum, opis)
##                    g.write(text)

#RECEPTI
##slovar = {}
##with open('CSV/uporabniki_id.csv','r') as g:
##    for vrstica in g.readlines():
##        if vrstica != '\n':
##            ime_uporabnika,id = vrstica.split(',')
##            id = id[:-1]
##            if id != 'id':
##                slovar[ime_uporabnika] = int(id)
##
##navodila = {}
##with open('CSV/navodilo.csv','r') as g:
##    for vrstica in g.readlines():
##        if vrstica != '\n':
##            id,navodilo = vrstica.split(',')
##            navodilo = navodilo[:-1]
##            #print(id)
##            if id != 'id':
##                navodila[id] = navodilo
##
##with open('SQL/naredi_sql_recepti1.txt','w') as g:
##    with open('CSV/skupaj_recept_uporanbik.csv','r') as f:
##        for vrstica in f.readlines():
##            if vrstica != '\n':
##                id,ime_recepta,ime_uporabnika,vrsta_jedi,dan,mesec,leto,cas_priprave,tezavnost = vrstica.split(',')
##                #id = id[8:13]
##                tezavnost = tezavnost[:-1]
##                if id != 'ď»żid':
##                    avtor = slovar.get(ime_uporabnika,'')
##                    cas_priprave = int(cas_priprave[:-6])
##                    datum = '{}.{}.{}'.format(int(dan),int(mesec),int(leto))
##                    navodilo = navodila.get(id,'')
##                    navodilo = navodilo[1:-1]
##                    if navodilo == '':
##                        url = 'https://www.kulinarika.net/recepti/{}'.format(id)
##                        webbrowser.open_new_tab(url)
##                        a = 0
##                        for i in range(10000000):
##                            a += 1
##                    text = 'INSERT INTO recept (id, ime, avtor, vrsta jedi, cas priprave, datum, tezavnost, navodilo) VALUES ({}, \'{}\', {}, \'{}\', {}, \'{}\', \'{}\', {});\n'.format(int(id), ime_recepta, avtor, vrsta_jedi, cas_priprave, datum, navodilo, tezavnost)
##                    #print(text)
##                    g.write(text)

#OBJAVA
##slovar = {}
##with open('CSV/uporabniki_id.csv','r') as g:
##    for vrstica in g.readlines():
##        if vrstica != '\n':
##            ime_uporabnika,id = vrstica.split(',')
##            id = id[:-1]
##            if id != 'id':
##                slovar[ime_uporabnika] = int(id)
##
##with open('SQL/naredi_sql_objava1.txt','w') as g:
##    with open('CSV/ime_uporabnika.csv','r') as f:
##        for vrstica in f.readlines():
##            if vrstica != '\n':
##                id,ime_uporabnika = vrstica.split(',')
##                ime_uporabnika = ime_uporabnika[:-1]
##                if id != 'ď»żid':
##                    avtor = slovar.get(ime_uporabnika,'')
##                    text = 'INSERT INTO objava (recept, avtor) VALUES ({}, {});\n'.format(id, avtor)
##                    g.write(text)

#PRIMERNOST
##with open('SQL/primernost1.txt','w') as g:
##    with open('CSV/primerno_za.csv','r') as f:
##        for vrstica in f.readlines():
##            if vrstica != '\n':
##                id_recepta,id_priloznosti = vrstica.split(',')
##                id_priloznosti = id_priloznosti[:-1]
##                if id_recepta != 'ď»żid':
##                    text = 'INSERT INTO primernost (recept, priloznost) VALUES ({}, {});\n'.format(id_recepta, id_priloznosti)
##                    g.write(text)

##SESTAVINA
##sez = []
##with open('SQL/naredi_sql_sestavina1.txt','w') as g:
##    with open('kljucne_nove.txt','r') as f:
##        for vrstica in f.readlines():
##            if vrstica != '\n':
##                id,sestavina = vrstica.split(',')
##                id = id[8:13]
##                sestavina = sestavina[:-1]
##                if sestavina not in sez:
##                    sez.append(sestavina)
##    for sestavina in sez:
##        text = 'INSERT INTO sestavina (ime) VALUES (\'{}\');\n'.format(sestavina)
##        g.write(text)

#POTREBUJE
slovar = {}
with open('CSV/sestavina_id.csv','r') as g:
    for vrstica in g.readlines():
        if vrstica != '\n':
            id,sestavina = vrstica.split(',')
            sestavina = sestavina[:-1]
            if id != 'ď»żid':
                slovar[sestavina] = int(id)

with open('SQL/naredi_sql_potrebuje.txt','w') as g:
    with open('kljucne_nove_kolicina.txt','r') as f:
        for vrstica in f.readlines():
            if vrstica != '\n':
                id,kolicina,sestavina = vrstica.split(',')
                sestavina = sestavina[:-1]
                if id != 'ď»żid':
                    if kolicina != '':
                        if sestavina != '[]':
                            id_sestavine = slovar.get(sestavina,'')
                            text = 'INSERT INTO potrebuje (recept, sestavina, kolicina) VALUES ({}, {}, \'{}\');\n'.format(id, id_sestavine, kolicina)
                            g.write(text)

