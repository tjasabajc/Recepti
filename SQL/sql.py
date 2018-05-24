import csv

with open('naredi_sql_uporabniki1.txt','w') as g:
    with open('ime_uporabnika.csv','r') as f:
        for vrstica in f.readlines():
            if vrstica != '\n':
                id,ime_uporabnika = vrstica.split(',')
                ime_uporabnika = ime_uporabnika[:-1]
                text = 'INSERT INTO uporabnik (id, ime) VALUES ({}, \'{}\');\n'.format(id,ime_uporabnika)
                g.write(text)

