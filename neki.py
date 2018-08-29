
with open('SQL/naredi_novi_recept.txt','w') as g:
    i=1
    with open('SQL/naredi_sql_recept.txt','r') as f:
        i=2
        for vrstica in f.readlines():
            nova = vrstica[105:-3]
            g.write(nova+"\n")


