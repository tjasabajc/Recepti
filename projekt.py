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
    cur.execute("SELECT recept.ime, (SELECT ime FROM uporabnik WHERE uporabnik.id = recept.avtor), "+
                "vrsta_jedi, cas_priprave, extract(year FROM datum_objave), extract(month FROM datum_objave)"+
                ",extract(day FROM datum_objave), navodilo, tezavnost, priloznost.ime, sestavine_objava.vse_skupaj FROM recept "+
                "LEFT JOIN primernost ON recept.id=primernost.recept LEFT JOIN sestavine_objava ON recept.id=sestavine_objava.recept LEFT JOIN priloznost ON priloznost.id=primernost.priloznost WHERE recept.id=%s", [id])
    recept=cur
    sez=[]
##    for (ime,avtor,vrsta_jedi,cas_priprave,leto, mesec, dan,navodilo,tezavnost, priloznost) in recept:
##        sez.append((ime,avtor,vrsta_jedi,cas_priprave,leto, mesec, dan,navodilo,tezavnost, priloznost))
##    cur.execute("SELECT recept.id,potrebuje.kolicina,sestavina.ime FROM recept "+
##                "LEFT JOIN potrebuje ON recept.id=potrebuje.recept LEFT JOIN sestavina ON potrebuje.sestavina=sestavina.id "+
##                "WHERE recept=%s", [id])
    return template('views/recept2.html', recept=cur)

@get('/')
def index():
    cur.execute("SELECT recept.ime,uporabnik.ime as avtor,recept.vrsta_jedi,recept.navodilo FROM recept JOIN uporabnik ON recept.avtor=uporabnik.id")
##    sez = [(20003, 'Hruškočoki'), (20007, 'Hitri puranji polpeti')]
##    id = 20007
##    ime = 'Hitri puranji polpeti'
##    cur.executemany("SELECT ime, id, vrsta_jedi, navodilo FROM recept WHERE recept.id = %s AND recept.ime=%s", sez)
    return template('views/domov.html', index=cur)

@get('/iskanje')
def iskanje_receptov():
    x1 = random.randint(20002, 20400)
    x2 = random.randint(20002, 20400)
    x3 = random.randint(20002, 20400)
    cur.execute("SELECT recept.id,recept.ime,recept.avtor,recept.vrsta_jedi,recept.cas_priprave,recept.datum_objave,recept.navodilo,recept.tezavnost FROM recept WHERE recept.id = %s OR recept.id = %s OR recept.id = %s", (x1, x2, x3))
    return template('views/iskanje_receptov23.html', rand_recepti=cur.fetchmany(3),
                    kljucne='', recept='', sestavina='', kategorija='', priloznost='',
                    cas='', tezavnost='', napaka=None, prvic=True, ustrezni=[x1, x2, x3])

@post('/iskanje')
def iskanje_receptov_post():
    x1 = random.randint(20002, 20400)
    x2 = random.randint(20002, 20400)
    x3 = random.randint(20002, 20400)
    kljucne='recept.NAVODILO='+request.forms.kljucne if request.forms.kljucne!='' else 'TRUE'
    recept="recept.ime='"+request.forms.recept+"'" if request.forms.recept!='' else 'TRUE'
    #sestavina='sestavina.ime=\''+request.forms.sestavina+'\'' if request.forms.sestavina!='' else 'TRUE'
    kategorija='recept.vrsta_jedi=\''+request.forms.kategorija+'\'' if request.forms.kategorija!='' else 'TRUE'
    priloznost='priloznost.ime=\''+request.forms.priloznost+'\'' if request.forms.priloznost!='' else 'TRUE'
    cas='recept.cas_priprave='+request.forms.cas[:request.forms.cas.index(' ')] if request.forms.cas!='' else 'TRUE'
    tezavnost='recept.tezavnost='+request.forms.tezavnost if request.forms.tezavnost!='' else 'TRUE'

    cur.execute('SELECT id,ime, navodilo FROM recept')
    ustrezni_id = []
    if kljucne != 'TRUE':
        kljucne = kljucne[16:]
        k = str(kljucne).lower()
        #isces besedo samo v stavku ali pa na koncu stavka ali pa pred vejico
        moznosti = [' '+k+' ', ' '+k+'.', ' '+k+',']
        for (id, ime, navodilo) in cur:
            for moznost in moznosti:
                if moznost in str(ime).lower() + str(navodilo).lower() and id not in ustrezni_id:
                    ustrezni_id.append(id)

    sestavina = request.forms.sestavina
    if sestavina != '':
        cur.execute("SELECT recept,sestavina FROM potrebuje WHERE sestavina = (SELECT id FROM sestavina WHERE sestavina.ime = '{}')".format(sestavina))
        for (id,sestavina) in cur:
            ustrezni_id.append(id)
    if sestavina == '' and kljucne == 'TRUE':
        ustrezni_id = range(20000,20500)
    try:
        cur.execute("SELECT recept.id,recept.ime,uporabnik.ime as avtor,recept.vrsta_jedi,recept.cas_priprave,recept.datum_objave,recept.navodilo,recept.tezavnost FROM recept"+
                    " JOIN uporabnik ON recept.avtor=uporabnik.id" +
                    " JOIN potrebuje ON recept.id=potrebuje.recept" +
                    " WHERE "+recept+" AND "+kategorija+" AND "+priloznost+" AND "+cas+" AND " + tezavnost)
        return template('views/iskanje_receptov23.html', prvic=False,rand_recepti=cur, kljucne='',
                        recept='', sestavina='', kategorija='', priloznost='',
                        cas=cas, tezavnost=tezavnost, napaka=None, ustrezni=ustrezni_id)
    # Ta zakomentirani del ne dela :::: NameError: name 'ustrezni1' is not defined
    except Exception as ex:
        return template('views/iskanje_receptov23.html', rand_recepti=cur,kljucne=kljucne,
                        recept=recept, sestavina=sestavina, kategorija=kategorija, priloznost=priloznost,
                        cas='',tezavnost='', napaka = 'Zgodila se je napaka: %s' % ex, prvic=False)
    
@get('/uporabnik')
def uporabniki():
    cur.execute("SELECT * FROM uporabnik")
    return template('views/uporabnik2.html', uporabnik=cur)

@get('/prijava')
def prijava():
    return template('views/prijava2.html', napaka=None)

@post('/prijava')
def prijava_registracija():
    #prijavljen = False
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

@get('/odjava')
def odjavi():
    return template('views/odjava.html')

@post('/odjava')
def odjavi():
    cur.execute("SELECT recept.ime,uporabnik.ime as avtor,recept.vrsta_jedi,recept.navodilo FROM recept JOIN uporabnik ON recept.avtor=uporabnik.id")
##    sez = [(20003, 'Hruškočoki'), (20007, 'Hitri puranji polpeti')]
##    id = 20007
##    ime = 'Hitri puranji polpeti'
##    cur.executemany("SELECT ime, id, vrsta_jedi, navodilo FROM recept WHERE recept.id = %s AND recept.ime=%s", sez)
    return template('views/domov.html', index=cur)

@get('/dodajanje')
def dodan_recept():
    return template('views/hvala.html')

@post('/dodajanje')
def dodan_recept():
##    recept=request.forms.recept
##    kategorija=request.forms.kategorija
##    priloznost=request.forms.priloznost
##    cas=request.forms.cas
##    tezavnost=request.forms.tezavnost
##    sestavine=request.forms.sestavine
##    navodilo=request.forms.navodilo
##    print(recept,kategorija,priloznost,cas,tezavnost,sestavine,navodilo)
##    #nekako dobiti ime uporabnika, ker je prijavlnej naj bi to vedla
##    cur.execute("INSERT INTO recept (ime, avtor, vrsta_jedi, cas_priprave,  navodilo, tezavnost) VALUES (%s, %s, %s, %s, %s, %s)",
##                [recept,avtor,kategorija,cas,navodilo,tezavnost])
##    cur.execute("SELECT id FROM recept WHERE ime=%s",[recept])
##    uporabnik=cur
##    for id in uporabnik:
##        id_recept=id
##    cur.execute("SELECT id FROM uporabnik WHERE ime=%s",[avtor])
##    uporabnik=cur
##    for id in uporabnik:
##        id_uporabnik=id
##    cur.execute("INSERT INTO objava (recept,avtor) VALUES (%s, %s)",
##                [id_recept,id_uporabnik])
##    cur.execute("SELECT id FROM priloznost WHERE ime=%s",[priloznost])
##    uporabnik=cur
##    for id in uporabnik:
##        id_priloznost=id
##    cur.execute("INSERT INTO primernost (recept,priloznost) VALUES (%s, %s)",
##                [id_recept,id_priloznost])
##    cur.execute("SELECT id FROM sestavina WHERE ime=%s",[sestavina])
##    uporabnik=cur
##    for id in uporabnik:
##        id_sestavina=id
##    #nekako dobiti iz texta sestavine in količine
##    cur.execute("INSERT INTO potrebuje (recept,sestavina,kolicina) VALUES (%s, %s, %s)",
##                [id_recept,id_sestavina,kolicina])
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
