#!/usr/bin/env python3
#2019-10-01 Jani Janttari <janttari@yandex.ru>
#
#dvbsub2srt käyttää tätä skriptiä luodakseen srt tekstitystiedoston luomistaan yksittäisistä
#tekstitiedostoista
#
import datetime, time, sys
from pathlib import Path

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
                alku=etsiValista(rivi,'start="','" end')
                falku=datetime.timedelta(seconds=float(alku))
                salku="0"+str(falku)[:-3].replace(".",",") #alkuaika tekstille
                loppu=etsiValista(rivi,'end="','" image')
                floppu=datetime.timedelta(seconds=float(loppu))
                sloppu="0"+str(floppu)[:-3].replace(".",",") #loppuaika tekstille
                kuva=etsiValista(rivi,'image="','" xoffset')
                numero=kuva[-8:-4]
                steksti =  Path(temppiHakemisto+'/'+alihakemisto+"/"+numero+".txt").read_text() #luetaan kyseinen tekstitystiedosto
                steksti=steksti.rstrip()
                kirjoitaSrt.write(str(kierros)+"\n")
                kirjoitaSrt.write(salku+" --> " +sloppu+"\n")
                kirjoitaSrt.write(steksti+"\n\n")
                kierros+=1
kirjoitaSrt.close()
