#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth_public as auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras, random
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

# odkomentiraj, če želiš sporočila o napakah
# debug(True)

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static') # to je treba spremenit nazaj v samo static

@get('/recept/<id>')
def recept(id):
    cur.execute("SELECT recept.ime, (SELECT ime FROM uporabnik WHERE uporabnik.id = recept.avtor), "+
                "vrsta_jedi, cas_priprave, extract(year FROM datum_objave), extract(month FROM datum_objave)"+
                ",extract(day FROM datum_objave), navodilo, tezavnost, priloznost.ime, sestavine_objava.vse_skupaj FROM recept "+
                "LEFT JOIN primernost ON recept.id=primernost.recept LEFT JOIN sestavine_objava ON recept.id=sestavine_objava.recept LEFT JOIN priloznost ON priloznost.id=primernost.priloznost WHERE recept.id=%s", [id])
    return template('views/recept2.html', recept=cur)

@get('/')
def index():
    cur.execute("SELECT recept.ime,uporabnik.ime as avtor,recept.vrsta_jedi,recept.navodilo FROM recept JOIN uporabnik ON recept.avtor=uporabnik.id")
    return template('views/domov.html', index=cur)

@get('/iskanje')
def iskanje_receptov():
    x1 = random.randint(20002, 20400)
    x2 = random.randint(20002, 20400)
    x3 = random.randint(20002, 20400)
    cur.execute("SELECT recept.id,recept.ime,recept.avtor,recept.vrsta_jedi,recept.cas_priprave,recept.datum_objave,recept.navodilo,recept.tezavnost FROM recept WHERE recept.id = %s OR recept.id = %s OR recept.id = %s", (x1, x2, x3))
    return template('views/iskanje_receptov23.html', rand_recepti=cur.fetchmany(3),
                    kljucne='', recept='', sestavina='', kategorija='', priloznost='',
                    cas='', tezavnost='', napaka=None, prvic=True)

@post('/iskanje')
def iskanje_receptov_post():
    pogoji = []
    pogoji = [(k, o, v) for k, o, v in [('recept.navodilo', 'ILIKE', request.forms.kljucne),
                                    ('recept.ime', 'ILIKE', request.forms.recept),
                                    ('recept.vrsta_jedi', '=', request.forms.kategorija),
                                    ('priloznost.ime', '=', request.forms.priloznost),
                                    ('sestavina.ime', '=', request.forms.sestavina),
                                    ('recept.cas_priprave', '=',
                                    request.forms.cas[:request.forms.cas.index(' ')] if ' ' in request.forms.cas else ''),
                                    ('recept.tezavnost', '=', request.forms.tezavnost)]
                                    if v != '']             # (ime stolpca, operator, podatek)
    print('PPPPOGOJI?', pogoji)
    where = ''
    where = ' AND '.join('{} {} {}'.format(k, o, "'%%'||%s||'%%'" if 'LIKE' in o else '%s')
            for k, o, v in pogoji) # pri (I)LIKE iščemo podniz
    if where != '': # če imamo kak pogoj, dodamo WHERE
        where = 'WHERE {}'.format(where)
        print(where)
        print('WHERE {}'.format(where))
    podatki = [v for k, o, v in pogoji]
    cur.execute("""
    SELECT recept.id, recept.ime, uporabnik.ime AS avtor, recept.vrsta_jedi,
           recept.cas_priprave, recept.datum_objave, recept.navodilo, recept.tezavnost
    FROM recept JOIN uporabnik ON recept.avtor = uporabnik.id
                JOIN potrebuje ON recept.id = potrebuje.recept
                JOIN sestavina ON sestavina.id = potrebuje.sestavina
                LEFT JOIN primernost ON recept.id = primernost.recept
                LEFT JOIN priloznost ON primernost.priloznost = priloznost.id
    {}""".format(where), podatki)
    return template('views/iskanje_receptov23.html', prvic=False,rand_recepti=cur.fetchall(),
                    kljucne='', recept='', sestavina='', kategorija='', priloznost='',
                    cas='', tezavnost='', napaka=None)
   
@get('/uporabnik')
def uporabniki():
    cur.execute("SELECT * FROM uporabnik")
    return template('views/uporabnik2.html', uporabnik=cur)

@get('/prijava')
def prijava():
    return template('views/prijava2.html', napaka=None)

@post('/prijava')
def prijava_registracija():
    upIme1 = request.forms.upIme1
    geslo = request.forms.geslo
    upIme2 = request.forms.upIme2
    geslo1 = request.forms.geslo1
    geslo2 = request.forms.geslo2
    if upIme2=='':
        try:
            cur.execute("SELECT id,ime FROM uporabnik WHERE ime=%s",[upIme1])
            uporabnik=cur
            for (id,ime) in uporabnik:
                cur.execute("SELECT * FROM geslo WHERE id=%s",[id])
                uporabnik=cur
                for (id,ime,geslo0) in uporabnik:
                    if ime==upIme1 and geslo==geslo0:
                        prijavljen = True
            if prijavljen:
                napaka = 'Uspešno ste prijavljeni!'
                return template('views/domov.html')
            else:
                napaka = 'Prijava neuspešna!'
                return template('views/prijava2.html',napaka = napaka)
            print(prijavljen)
            
        except Exception as ex:
                return template('views/prijava2.html', upIme1=upIme1, geslo=geslo,
                            napaka = 'Zgodila se je napaka: %s' % ex, prijavljen=prijavljen)
    elif upIme1=='':
        if geslo1==geslo2:
            try:
                cur.execute("INSERT INTO uporabnik (ime, opis) VALUES (%s,'Začetnik,')",[upIme2])
                cur.execute("SELECT * FROM uporabnik WHERE ime=%s",[upIme2])
                uporabnik=cur
                for (id,ime,datum,opis) in uporabnik:
                    cur.execute("INSERT INTO geslo (id, ime, geslo) VALUES (%s,%s,%s)",[id,upIme2,geslo1])
                return template('views/prijava2.html')
            except Exception as ex:
                if ex=='no results to fetch':
                    napaka = ''
                else:
                    napaka ='Zgodila se je napaka: %s' % ex
                print(ex)
                return template('views/prijava2.html', upIme2=upIme2, geslo1=geslo1, geslo2=geslo2,
                            napaka = napaka)
    redirect("/")

@get('/midva')
def midva():
    return template('views/midva.html')

@get('/dodaj_recept')
def dodaj_receot():
    return template('views/dodajanje.html', ime='', sestavine='', kategorija='', priloznost='',
                    cas='', tezavnost='')

@get('/vsi_recepti')
def vsi_recepti():
    cur.execute("SELECT id,ime, navodilo FROM recept")
    return template('views/vsi_recepti.html', vsi=cur)

@get('/rezultati_iskanja')
def vsi_recepti():
    cur.execute("SELECT id,ime, navodilo FROM recept")
    return template('views/rezultati.html', vsi=cur)

@get('/odjava')
def odjavi():
    return template('views/odjava.html')

@post('/po_odjavi')
def odjavi():
    cur.execute("SELECT recept.ime,uporabnik.ime as avtor,recept.vrsta_jedi,recept.navodilo FROM recept JOIN uporabnik ON recept.avtor=uporabnik.id")
    return template('views/domov.html', index=cur)

@get('/dodajanje')
def vnesi_recept():
    return template('views/hvala.html')

@get('/hvala')
def dodaj_recept():
    # Zaradi časovne stiske nedokončana funkcija. Želela sva sicer omogočiti uporabnikom dodajanje receptov v bazo,
    # ampak trenutno ta možnost ne deluje.
    return template('views/hvala.html')
    
######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
print(666)
