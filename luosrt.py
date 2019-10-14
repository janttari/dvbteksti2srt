#!/usr/bin/env python3
#2019-10-14 Jani Janttari <janttari@yandex.ru>
#
#dvbsub2srt käyttää tätä skriptiä luodakseen srt tekstitystiedoston luomistaan yksittäisistä
#tekstitiedostoista
#
import datetime, time, sys, os
from pathlib import Path

maxNayttoaika=10.0 # Tekstityksen maksimi näyttöaika sekunteina
aikaOffset=0.0 # korjataan tekstityksen ajoitusta sekuntia


temppiHakemisto=str(sys.argv[1])


def etsiValista( s, eka, vika ): #merkkijono josta etsitään sananA ja sananB välistä
    try:
        alku = s.index(eka) + len(eka)
        loppu = s.index( vika, alku )
        return s[alku:loppu]
    except ValueError:
        return ""

if os.path.isfile(temppiHakemisto+"/subs.xml"): #************************ xml created by ccextactor ****
    print("ccextactor xml")
    kirjoitaSrt=open(temppiHakemisto+"/tekstit.srt", "w")
    with open(temppiHakemisto+"/subs.xml", "r") as fp:
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
                    salku="0"+str(falku)
                    if not "." in salku: #jos aika on tasasekunti ilman desimaalinollia, niin lisätään ne
                        salku+=".000000"
                    salku=salku[:-3].replace(".",",")

                    floppu=datetime.timedelta(seconds=float(loppu))
                    sloppu="0"+str(floppu)
                    if not "." in sloppu: #jos aika on tasasekunti ilman desimaalinollia, niin lisätään ne
                        sloppu+=".000000"
                    sloppu=sloppu[:-3].replace(".",",") #poistetaan lopusta kolme nollaa ja muutetaan piste pilkuksi

                    kuva=etsiValista(rivi,'image="','" xoffset')
                    numero=kuva[-8:-4]
                    steksti =  Path(temppiHakemisto+'/'+"subs.d"+"/"+numero+".txt").read_text() #luetaan kyseinen tekstitystiedosto
                    steksti=steksti.rstrip()
                    kirjoitaSrt.write(str(kierros)+"\n")
                    kirjoitaSrt.write(salku+" --> " +sloppu+"\n")
                    kirjoitaSrt.write(steksti+"\n\n")
                    kierros+=1
    kirjoitaSrt.close()


elif os.path.isfile(temppiHakemisto+"/png/subs.xml"): #************************ xml created by subp2png ****
    print("subp2png  xml")
    kirjoitaSrt=open(temppiHakemisto+"/tekstit.srt", "w")
    with open(temppiHakemisto+"/png/subs.xml", "r") as fp:
        kierros=1 #Tämä on srt-tiedostoon tulostettava indeksi
        for rivi in fp:
            if(len(rivi))>1:
                rivi=rivi.rstrip()
                if rivi.startswith("  <subtitle i"): #tällä rivillä tarvittavat tiedot
                    alku=etsiValista(rivi,'start="','" stop')
                    #sekAlku=aikaOffset+float(alku[6:])
                    #if sekAlku<0: #jos aikaOffset vääntää pakkaselle
                    #    sekAlku=0
                    loppu=etsiValista(rivi,'stop="','">')
                    #print(">"+loppu+"<")
                    #sekLoppu=aikaOffset+float(loppu[6:])
                    #if sekLoppu<0: #jos aikaOffset vääntää pakkaselle
                    #    sekLoppu=0         
                    alkuDateTime = datetime.datetime.strptime(alku, '%H:%M:%S.%f')+datetime.timedelta(seconds=aikaOffset)
                    loppuDateTime = datetime.datetime.strptime(loppu, '%H:%M:%S.%f')+datetime.timedelta(seconds=aikaOffset)
                    #tähän tsekkaa jos pakkaselle offsetin takia
                    salku=str(alkuDateTime)[11:-3]
                    sloppu=str(loppuDateTime)[11:-3]
                    diff=loppuDateTime-alkuDateTime
                    if diff.seconds>maxNayttoaika:
                        ssLoppu=str(alkuDateTime+datetime.timedelta(seconds=maxNayttoaika))[11:-3]
                    kuva=etsiValista(rivi,'id="','" start')
                    numero=("0000"+kuva)[-4:]
                    steksti =  Path(temppiHakemisto+'/'+"png"+"/"+numero+".txt").read_text() #luetaan kyseinen tekstitystiedosto
                    steksti=steksti.rstrip()
                    kirjoitaSrt.write(str(kierros)+"\n")
                    kirjoitaSrt.write(salku+" --> " +sloppu+"\n")
                    kirjoitaSrt.write(steksti+"\n\n")
                    kierros+=1
    kirjoitaSrt.close()
