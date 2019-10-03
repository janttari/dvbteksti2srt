#!/usr/bin/env python3
#2019-10-03 Jani Janttari <janttari@yandex.ru>
#
#dvbsub2srt käyttää tätä skriptiä luodakseen srt tekstitystiedoston luomistaan yksittäisistä
#tekstitiedostoista
#
import datetime, time, sys
from pathlib import Path

maxNayttoaika=10.0 # Tekstityksen maksimi näyttöaika sekunteina
aikaOffset=0.0 # korjataan tekstityksen ajoitusta sekuntia


temppiHakemisto=str(sys.argv[1])
projektiNimi=str(sys.argv[2])
alihakemisto="muokatutKuvat"

def etsiValista( s, eka, vika ): #merkkijono josta etsitään sananA ja sananB välistä
    try:
        alku = s.index(eka) + len(eka)
        loppu = s.index( vika, alku )
        return s[alku:loppu]
    except ValueError:
        return ""

kirjoitaSrt=open(temppiHakemisto+"/tekstit.srt", "w")
with open(temppiHakemisto+"/"+projektiNimi+".xml") as fp:
    kierros=1 #Tämä on srt-tiedostoon tulostettava indeksi
    for rivi in fp:
        if(len(rivi))>1:
            rivi=rivi.rstrip()
            if rivi.startswith("<spu"): #tällä rivillä tarvittavat tiedot
                alku=aikaOffset+float(etsiValista(rivi,'start="','" end'))
                if alku<0: #jos aikaOffset vääntää pakkaselle
                    alku=0
                loppu=aikaOffset+float(etsiValista(rivi,'end="','" image'))
                if loppu<0: #jos aikaOffset vääntää pakkaselle
                    loppu=0
                kesto=(loppu-alku)
                if (kesto<0) or (kesto>maxNayttoaika): # jos näyttöaika liian lyhyt tai liian pitkä. liian lyhyt se voi olla kesken pätkäistyssä transport streamissa
                    loppu=alku+maxNayttoaika
                falku=datetime.timedelta(seconds=float(alku))
                salku=str(falku)
                if not "." in salku: #jos aika on tasasekunti ilman desimaalinollia, niin lisätään ne
                    salku+=".000000"
                salku=salku[:-3].replace(".",",")

                floppu=datetime.timedelta(seconds=float(loppu))
                sloppu=str(floppu)
                if not "." in sloppu: #jos aika on tasasekunti ilman desimaalinollia, niin lisätään ne
                    sloppu+=".000000"
                sloppu=sloppu[:-3].replace(".",",") #poistetaan lopusta kolme nollaa ja muutetaan piste pilkuksi

                kuva=etsiValista(rivi,'image="','" xoffset')
                numero=kuva[-8:-4]
                steksti =  Path(temppiHakemisto+'/'+alihakemisto+"/"+numero+".txt").read_text() #luetaan kyseinen tekstitystiedosto
                steksti=steksti.rstrip()
                kirjoitaSrt.write(str(kierros)+"\n")
                kirjoitaSrt.write(salku+" --> " +sloppu+"\n")
                kirjoitaSrt.write(steksti+"\n\n")
                kierros+=1
kirjoitaSrt.close()
