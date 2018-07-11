#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth as auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

# odkomentiraj, če želiš sporočila o napakah
# debug(True)

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static') # to je treba spremenit nazaj v samo static

@get('/recept/<id>')
def recept():
    cur.execute("SELECT id FROM recept WHERE recept.id = %s", id)
    # return template('views/recept.html, recept=cur)
    # v spremenjivki recept bodo ime, avtor, sestavine ...
    # To potem daš v html na spletno stran tako kot imava zdaj na prvi strani
    # for ime, avtor, sestavine ... in recept
    return template('views/recept.html', recept=cur)

@get('/')
def index():
    cur.execute("SELECT * FROM recept")
    return template('views/domov.html', index=cur)

@get('/iskanje')
def iskanje_receptov():
    cur.execute("SELECT * FROM recept")
    return template('views/iskanje_receptov.html', iskanje_receptov=cur)

@get('/dodaj_transakcijo')
def dodaj_transakcijo():
    return template('views/dodaj_transakcijo.html', znesek='', racun='', opis='', napaka=None)

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

######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
print(666)
