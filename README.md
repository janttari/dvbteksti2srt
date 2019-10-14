# dvbteksti2srt
Muuttaa-graafisen DVB tekstityksen SRT-muotoon hyödyntäen ccextractor, convert ja tesseract-ocr
ccectractorin purkamat bittikartat muokataan convertilla paremmin koneluettavaan muotoon ja
sitten tesseract tulkitsee ne.
Lopuksi luosrt.py yhdistää yksittäiset tekstit .srt-tiedostoksi.

http://www.huoltovalikko.com/threads/hd-tallenteiden-jatkojalostus-linuxilla-etenkin-tekstitykset.13745/#post-173104

asennus:

    git clone https://github.com/janttari/dvbteksti2srt.git
    sudo ./asennaohjelmat

päivitys (projektihakemistossa):

    git pull && sudo ./update

käyttöesimerkkejä:

    dvbteksti2srt -lang=swe video.ts
    dvbteksti2srt -lang=nor video.ts
    dvbteksti2srt -lang=fin video.ts
    dvbteksti2srt video.ts #ilman -lang -valintaa kieli=fin
    dvbteksti2srt -font=testi1 -lang=fin video.ts #muuttaa fontin käsittelyn asetuksia
    dvbteksti2srt -font=testi2 -lang=fin video.ts #muuttaa fontin käsittelyn asetuksia
    dvbteksti2srt -nodelete /media/loop/VIDEO_TS/ #DVD-levyn lukeminen tekstiksi. -nodelete jättää /tmp/dvbteksti2srt hakemistoon tiedostot
    
Parametrit:
    -lang {fin, swe, nor}
    -font {norm, testi1, testi2, dvd} #OCR-tunnistuksen parametrejä
    -nodelete #jättää temppihakemistoon tiedostot.
##### TODO:

