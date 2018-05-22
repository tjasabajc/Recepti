import csv

with open('naredi_sql_uporabniki.txt','w') as g:
    with open('test1.csv','r') as f:
        for vrstica in f.readlines():
            if vrstica != '\n':
                id,ime_uporabnika = vrstica.split(',')
                id = id[8:11]
                ime_uporabnika = ime_uporabnika[:-1]
                text = 'INSERT INTO uporabniki ({}, {});\n'.format(id,ime_uporabnika)
                g.write(text)
