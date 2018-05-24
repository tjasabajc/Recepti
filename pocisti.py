
slovar = {
    #A
    'avokada' : 'avokado',
    #B
    #C
    'čebule' : 'čebula',
    'čebuli' : 'čebula',
    'česna' : 'česen',
    'cimeta' : 'cimet',
    #D
    #E
    #F
    #G
    #H
    #I
    'ingverja' : 'ingver',
    #J
    'jajc' : 'jajca',
    'jajce' : 'jajca',
    'jajci' : 'jajca',
    'jogurta' : 'jogurt',
    #K
    'kisa' : 'kis',
    'kolerabe' : 'koleraba',
    'korenček' : 'korenje',
    'korenčke' : 'korenje',
    'korenja' : 'korenje',
    'krompirji' : 'krompir',
    'krompirja' : 'krompir',
    'kruha' : 'kruh',
    'kumar' : 'kumara',
    #L
    'limon' : 'limona',
    'limone' : 'limona',
    'limonine' : 'limona',
    'limoninega' : 'limona',
    #M
    'mandljev' : 'mandlji',
    'marelic' : 'marelice',
    'masla' : 'maslo',
    'mleka' : 'mleko',
    'moke' : 'moka',
    #N
    #O
    'olja' : 'olje',
    'orehov' : 'orehi',
    #P
    'paprike' : 'paprika',
    'paradižnika' : 'paradižnik',
    'paradižnikove' : 'paradižnik',
    'paradižnikovega' : 'paradižnik',
    'peteršilja' : 'peteršilj',
    'popra' : 'poper',
    'pora' : 'por',
    'porovo' : 'por',
    #R
    'rakcev' : 'rakci',
    'riža' : 'riž',
    'ruma' : 'rum',
    #S
    'sira' : 'sir',
    'sladkorja' : 'sladkor',
    'smetane' : 'smetana',
    'soli' : 'sol',
    #Š
    'šalotke' : 'šalotka',
    #T
    'timijana' : 'timijan',
    #U
    #V
    'vode' : 'voda',
    #Z
    'zelene' : 'zelena'
    }

brisi = [
    #A
    'a',
    'ali',
    #B
    'bel',
    'bela',
    'bele',
    'belega',
    #C
    'cel',
    'cela',
    'cele',
    'celo',
    'cl',
    'cvrenje',
    'cvrtje',
    #Č
    'črnega',
    #D
    'dag',
    'dl',
    'do',
    'dobro',
    'dobrega',
    'drobno',
    #E
    'ena',
    'ene',
    'eno',
    'Eno',
    #F
    #G
    'glava',
    #H
    #I    
    'in',
    'iz',
    #J
    'je',
    'jedilna',
    'jedilne',
    'jedilnega',
    'jušna',
    'jušne',
    'jušno',
    #K
    'kg',
    'kg.',
    'kock',
    'kocka',
    'kocke',
    'kocko',
    'količina',
    'kolobarčke',
    'kolobarje',
    'korenino',
    'kos',
    'kose',
    'košček',
    'koščke',
    'kuhana'
    'kuhanega',
    'kuhanih',
    'kuhano',
    #L
    'litrov',
    'lonček',
    'lupina',
    'lupinica',
    #M
    'majhen',
    'majhna',
    'malo',
    'manjša',
    'mehke',
    'mlade',
    'mladega',
    'mladi',
    'mladih',
    'mlet',
    'mleta',
    'mlete',
    'mletega',
    'močna',
    'močne',
    'mokasta',
    #N
    'na',
    'namočenih',
    'nastrgana',
    'nastrgane',
    'narezanega',
    'nastrganih',
    'narezan',
    'narezana',
    'narezane',
    'narezani',
    'narezanih',
    'narezano',
    'nariban',
    'naribana',
    'naribanega',
    'nekaj',
    'nemastnega',
    #O
    'okusu',
    'olivno',
    'olivnega',
    'olupljen',
    'olupljena',
    'olupljene',
    'olupljenih',
    'osnove',
    'oz',
    #P
    'pekoče',
    'po',
    'popečen',
    'popečenega',
    'posipanje',
    'potrebi',
    'prahu',
    #R
    'rdeče',
    'rdečega',
    'rezin',
    'rezina',
    'rezine',
    'rjavega',
    #S
    's',
    'se',
    'sesekljan',
    'sesekljana',
    'sesekljane',
    'sesekljanega',
    'sesekljanih',
    'skodelica',
    'skodela',
    'skodele',
    'skodeli',
    'sok',
    'soka',
    'span',
    'stepene',
    'steblo',
    'stopljenega',
    'strok',
    'stroka',
    'stroke',
    'stroki',
    'strtega',
    'svetlega',
    'svežega',
    'suhega',
    'surovega',
    #Š
    'šcepec',
    'ščepec',
    #T
    'tenkega',
    'temnega',
    'trd',
    'trdo',
    'tudi',
    #U
    #V
    'v',
    'velik',
    'velika',
    'velikih',
    'večja',
    'večje',
    'večji',
    'vinskega',
    'vinski',
    'vlečenega',
    'voda',
    'vode',
    'vroča',
    'vroče',
    #Z
    'z',
    'za',
    'začinko',
    'zmlet',
    'zmleta',
    'zmletih',
    'zrn',
    'zrnih',
    #Ž
    'želji',
    'žlic',
    'žlica',
    'žlice'
    ]

def odstrani(beseda):
    if len(beseda) > 0:        
        if beseda[0] in '"<(0123456789ˇ;./':
            beseda = odstrani(beseda[1:])
        if len(beseda) > 1:
            if beseda[-1] in '"\n.;,>/)':
                beseda = odstrani(beseda[:-1])
            if 'https://www.' in beseda:
                i = beseda.index('>')
                beseda = beseda[i + 1:-3]
    return beseda

    
def pocisti(sestavina):
    besede = sestavina.split(' ')
    kljucna = []
    for i in range(len(besede)):
        b = odstrani(besede[i])
        #print(i, ' ', b)
        if b in slovar:
            kljucna.append(slovar[b])
        elif b not in brisi and b != '\n':      # and len(b) <= 1
            kljucna.append(b)
    #print('KONEC ', kljucna)
    #if [] in kljucna:
    #    kljucna.remove([])
    if len(kljucna) == 1:
        k = kljucna[0]
    else:
        k = sestavina + 'OSTANE : ' + str(kljucna)  
    return k

#print(pocisti('močne jušne osnove ali vode z jušno kocko'))

with open('kljucne_sestavine.txt','w') as g:
    with open('CSV/sestavina_loceno.csv','r') as f:
        for vrstica in f.readlines():
            id, sestavina = vrstica.split(',')
            g.write(str(pocisti(sestavina)) + '\n')

