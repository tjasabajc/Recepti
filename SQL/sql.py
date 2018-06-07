import csv

with open('naredi_sql_recepti.txt','w') as g:
    with open('ime_uporabnika.csv','r') as f:
        for vrstica in f.readlines():
            if vrstica != '\n':
                id,ime_uporabnika,_ = vrstica.split(',')
                id = id[8:13]
                ime_uporabnika = ime_uporabnika[:-1]
                text = 'INSERT INTO recept (id, avtor) VALUES ({}, \'{}\');\n'.format(id, ime_uporabnika)
                print(text)
                g.write(text)

