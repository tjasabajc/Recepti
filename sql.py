import csv

##with open('naredi_sql_uporabniki1.txt','w') as g:
##    with open('uporabniki.csv','r') as f:
##        for vrstica in f.readlines():
##            if vrstica != '\n':
##                id,ime_uporabnika = vrstica.split(',')
##                id = id[8:11]
##                ime_uporabnika = ime_uporabnika[:-1]
##                text = 'INSERT INTO uporabniki ({}, {});\n'.format(id,ime_uporabnika)
##                g.write(text)

sez1 = {}
sez2 = {}
sez3 = {}
sez4 = {}
with open('recepti.csv','w') as g:
    with open('ime_recepta.csv','r') as f:
        for vrstica in f.readlines():
            if vrstica != '\n':
                id,ime_recepta = vrstica.split(',')
                ime_recepta = ime_recepta[:-1]
                sez1[id] = ime_recepta
    with open('cas_priprave.csv','r') as i:
        for vrstica in i.readlines():
            if vrstica != '\n':
                id,cas_priprave = vrstica.split(',')
                cas_priprave = cas_priprave[:-1]
                sez2[id] = cas_priprave
    with open('vrsta_jedi.csv','r') as j:
        for vrstica in j.readlines():
            if vrstica != '\n':
                id,vrsta_jedi = vrstica.split(',')
                vrsta_jedi = vrsta_jedi[:-1]
                sez3[id] = vrsta_jedi
    with open('navodilo.csv','r') as k:
        for vrstica in k.readlines():
            if vrstica != '\n':
                id,navodilo = vrstica.split(',')
                navodilo = navodilo[:-1]
                sez4[id] = navodilo
        with open('datum.csv','r') as h:
            for vrstica in h.readlines():
                if vrstica != '\n':
                    id,dan,mesec,leto = vrstica.split(',')
                    leto = leto[:-1]
                    text = '{},{},{},{},{},{},{}\n'.format(id,sez1[id],sez3[id],dan,mesec,leto,sez2[id],sez4[id])
                    sez1.pop(id)
                    sez2.pop(id)
                    sez3.pop(id)
                    sez4.pop(id)
                    g.write(text)
print(sez1)
print(sez2)
print(sez3)
print(sez4)



