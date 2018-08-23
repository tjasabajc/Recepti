#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth as auth

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
    cur.execute("SELECT ime, (SELECT ime FROM uporabnik WHERE uporabnik.id = recept.avtor), "+
                "vrsta_jedi, cas_priprave, extract(year FROM datum_objave), extract(month FROM datum_objave)"+
                ",extract(day FROM datum_objave), navodilo, tezavnost FROM recept WHERE recept.id=%s", [id])
    return template('views/recept2.html', recept=cur)

@get('/')
def index():
    cur.execute("SELECT recept.id,recept.ime,uporabnik.ime as avtor,recept.vrsta_jedi,recept.navodilo FROM recept JOIN uporabnik ON recept.avtor=uporabnik.id")
    return template('views/domov.html', index=cur.fetchmany(5))

@get('/iskanje')
def iskanje_receptov():
    x1 = random.randint(20002, 20400)
    x2 = random.randint(20002, 20400)
    x3 = random.randint(20002, 20400)
    cur.execute("SELECT recept.id,recept.ime,recept.avtor,recept.vrsta_jedi,recept.cas_priprave,recept.datum_objave,recept.navodilo,recept.tezavnost,uporabnik.id,uporabnik.ime FROM recept JOIN uporabnik ON recept.avtor=uporabnik.id WHERE recept.id = %s OR recept.id = %s OR recept.id = %s", (x1, x2, x3))
    return template('views/iskanje_receptov23.html', rand_recepti=cur.fetchmany(3),
                    kljucne='', recept='', sestavina='', kategorija='', priloznost='',
                    cas='', tezavnost='', napaka=None)

@post('/iskanje')
def iskanje_receptov_post():
    x1 = random.randint(20002, 20400)
    x2 = random.randint(20002, 20400)
    x3 = random.randint(20002, 20400)
    kljucne=request.forms.kljucne
    recept=request.forms.recept
    sestavina=request.forms.sestavina
    kategorija=request.forms.kategorija
    priloznost=request.forms.priloznost
    cas=request.forms.cas
    tezavnost=request.forms.tezavnost
    print(kljucne,recept,sestavina,kategorija,priloznost,cas[:2],tezavnost)
    try:
        cur.execute("SELECT recept.id,recept.ime,uporabnik.ime as avtor,recept.vrsta_jedi,recept.cas_priprave,recept.datum_objave,recept.navodilo,recept.tezavnost,priloznost.ime as priloznost,sestavina.ime as sestavina FROM recept"+
                    " JOIN primernost ON recept.id=primernost.recept JOIN priloznost ON priloznost.id=primernost.priloznost" +
                    " JOIN uporabnik ON recept.avtor=uporabnik.id" +
                    " JOIN potrebuje ON recept.id=potrebuje.recept JOIN sestavina ON potrebuje.sestavina=sestavina.id" +
                    " WHERE recept.ime=%s OR sestavina.ime=%s OR recept.vrsta_jedi=%s OR priloznost.ime=%s OR recept.cas_priprave=%s OR recept.tezavnost=%s"
                    ,[recept,sestavina,kategorija,priloznost,int(cas[:2]),int(tezavnost)])
        return template('views/iskanje_receptov23.html', rand_recepti=cur,kljucne=kljucne,
                        recept=recept, sestavina=sestavina, kategorija=kategorija, priloznost=priloznost,
                        cas=cas, tezavnost=tezavnost, napaka=None)
    except Exception as ex:
        return template('views/iskanje_receptov23.html', rand_recepti=cur,kljucne=kljucne,
                        recept=recept, sestavina=sestavina, kategorija=kategorija, priloznost=priloznost,
                        cas=cas,tezavnost=tezavnost, napaka = 'Zgodila se je napaka: %s' % ex)
    #redirect("/")
    
@get('/uporabnik')
def uporabniki():
    cur.execute("SELECT * FROM uporabnik")
    return template('views/uporabnik2.html', uporabnik=cur.fetchmany(5))

@get('/prijava')
def prijava():
    return template('views/prijava2.html', napaka=None)

@post('/prijava')
def prijava_registracija():
    upIme = request.forms.upIme
    geslo1 = request.forms.geslo1
    geslo2 = request.forms.geslo2
    if geslo1==geslo2:
        try:
            cur.execute("INSERT INTO uporabnik (ime, opis) VALUES (%s,'Začetnik,')",[upIme])
            cur.execute("SELECT * FROM uporabnik WHERE ime=%s",[upIme])
            uporabnik=cur
            for (id,ime,datum,opis) in uporabnik:
                cur.execute("INSERT INTO geslo (id, ime, geslo) VALUES (%s,%s,%s)",[id,upIme,geslo1])
            return template('views/prijava2.html')
        except Exception as ex:
            return template('views/prijava2.html', upIme=upIme, geslo1=geslo1, geslo2=geslo2,
                        napaka = 'Zgodila se je napaka: %s' % ex)
    redirect("/")

@get('/midva')
def midva():
    return template('views/midva.html')

@get('/dodaj_transakcijo')
def dodaj_transakcijo():
    return template('views/dodaj_transakcijo.html')

@post('/dodaj_transakcijo')
def dodaj_transakcijo_post():
    znesek = request.forms.znesek
    racun = request.forms.racun
    opis = request.forms.opis
    try:
        cur.execute("INSERT INTO transakcija (znesek, racun, opis) VALUES (%s, %s, %s)",
                    (znesek, racun, opis))
    except Exception as ex:
        return template('views/dodaj_transakcijo.html', znesek=znesek, racun=racun, opis=opis,
                        napaka = 'Zgodila se je napaka: %s' % ex)
    redirect("/")

@get('/vsi_recepti')
def vsi_recepti():
    cur.execute("SELECT id,ime, navodilo FROM recept")
    return template('views/vsi_recepti.html', vsi=cur)

@get('/rezultati_iskanja')
def vsi_recepti():
    cur.execute("SELECT id,ime, navodilo FROM recept")
    return template('views/rezultati.html', vsi=cur)
    
######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
print(666)
