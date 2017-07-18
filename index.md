---
layout: page
title: SICOUNTER
subtitle: SportIdent lyukasztás és kiolvasás számláló
---

verziószám: 0.1.2  
_[LETÖLTÉS]_


Bevezetés
---------

The `sicounter.py` _Python 3_ szkript segítségével számlálhatja az egy vagy több SportIdent dobozba történt lyukasztásokat vagy kiolvasásokat.

Eredetileg a [2017-es Hungária Kupára](http://adatbank.mtfsz.hu/esemeny/show/esemeny_id/6363) készült azzal a céllal, hogy számolja a célba érkezőket, akik közül minden századik valamilyen ajándékban részesült.
A feladatot bonyolította, hogy több doboz fogadja a beérkezőket és ezeket együttesen kell figyelni, ráadásul nem lehetett előre tudni, hogy lesz-e lehetőség a céldobozok bekötésére, mert ha nem, akkor jobb híjján a kiolvasásokat kell számlálni.
A kiolvasásoknak azonban két módja van: _handshake_ és _auto send_.

Ennek megfelelően három különböző számlálót alkalmaz a SICOUNTER:

* _TR_:
  Ez számlálja az _auto send_ módba állított ellenőrződoboz (_Clear, Check, Start, Control, Finish_) által küldött lyukasztásokat.
  A doboz típusával a számláló nem foglalkozik, azaz ha több doboz lyukasztásait számlálja, és ezek a dobozok eltérő típusúak, a számláló nem különíti el ezeket.

* _IN_:
  Ez számlálja a kiolvasódobozba behelyezett dugókákat.
  A számláló a behelyezés pillanatában lép tovább, még az adatok tényleges kiolvasását megelőzően.
  Csak olyan _Readout_ módba állított dobozok esetén működik, melyeken nem lett beállítva _auto send_: ezt nevezi a SportIdent dokumentáció _handshake_ (azaz kézfogásos) módú kilvasásnak.
  Itt csupán a dugokák behelyezését és a kivételét küldi el a doboz automatikusan, az adatokat az így értesült szofvernek ezután külön ki kell kérnie a lyukasztási adatokat amíg a dugóka a dobozban van.
  A be- és kihelyezési üzenet csak a dugóka számát tartalmazza 4 bájton, ez tehát villámgyorsan érkezik.

* _RO_:
  Ez számlálja a első kiolvasási adatblokkok érkezését a kiolvasódobozokból.
  Azért az elsőkét, mert a számláló szempontjából csak a dugóka száma lényeges, és azt pedig az első blokkok tartalmazzák.
  Megjegyzendő, hogy _handshake_ mód esetén ezt az adatot a versenylebonyolító szoftvernek kifejezetten kérnie kell, azaz nem érkezik magától. 
  Mivel a blokkméret 128 bájt, ezért ez az adat valamiel lassabban érkezik meg, mint az _IN_ számláló esetében.

  Kiolvasások számlálásako
  Amennyiben a kiolvasás _handshake_ módban történik, úgy érdemes előnyben részesíteni az _IN_ számlálót, ám nagyon kis esélyt látok arra, hogy bármikor más értéket mutasson a kettő: ahhoz azonos időpillanatban kell kiolvasni több versenyzőnek, és az adatokat kérő szofvernek pedig eltérő ütemben reagálni az első kiolvasó kárára.

A SICOUNTER gyakorlatilag sorszámokat oszt az egyes dugókáknak.
A kapott sorszám rögzített, és későbbi, ismételt lyukasztásokkal vagy kiolvasásokkal sem változik.
Az első alkalom a mérvadó tehát.

Ha valaki valamelyik számláló által követett eseményt első ízben megvalósítja (pl. lyukaszt), akkor a dugókája kap egy sorszámot.
Ezt a sorszámot az ő későbbi lyukasztásai már nem befolyásolják.
Kap továbbá egy másik sorszámot a dobozra vonatkozólag, ami az adott dobozbeli sorrendjét jelöli.
Ez utóbbi szám látható majd zárójelek között.
Azaz valaki lehet a 126. személy aki kiolvasott a három figyelt dobozok valamelyikén, ám abban a dobozban, amelyikben kiolvasott, ő a 48. személy, aki kiolvasott.

A SICOUNTER naplózza is a számlálók alkulását a `SICOUNTER.LOG` fájlba, amit aztán a következő elinduláskor betölt, így egy esetleges újraindítás után is zavartalanul tudja folytatni a számlálást.

Ezen kívül a SICOUNTER jelzi a számlálás szempontjából érdektelen adatforgalmat is: ebben az esetben az utasítási bájtot és a hosszbájtot mutatja meg egy csillag jel után.

Fontos tudni, hogy a SICOUNTER nem ír semmit a SportIdent doboz felé, csak passzívan olvassa az onnan jövő adatokat.


Telepítés és használat
----------------------

1. Töltse le és telepítse a [_Python 3_ legújabb verzióját](https://www.python.org/downloads/)!
   Remélhetőleg a telepítő fel fogja ajánlani, hogy a `python.exe` fájl elérési útját hozzáadja a `$PATH` környezeti változóhoz, így nem kell a teljes elérési utat megadni indításkor.
   Éljen ezzel a lehetőséggel!

2. Telepítse és indítsa a [SICOMTRACE]-et minden egyes dobozra, amelyen számlálást kíván végezni!
   Amennyiben a dobozok azonos számítógéphez kapcsolódnak, akkor a TCP/IP szervereket más-más portokra kell állítani.
   A SICOUNTER ezekhez fog kapcsolódni.

3. [Töltse le][LETÖLTÉS] és csomagolja ki a SICOUNTER-t egy könyvtárba!

4. Nyisson egy Parancssort (Start gomb > Keresés `cmd`-re)!
   Lépjen be a könyvtárba ahova `SICOUNTER.LOG` fájlt szeretné.
   Innen indítsa a SICOUNTER szkriptet a Python segítségével.
   A program ettől kezdve számlálja a lyukasztásokat, a kiolvasási behelyezéseket és a kiolvasásokat.
   
   ![SICOUNTER szkript parancssorból](https://raw.githubusercontent.com/tajfutas/sicounter/gh-pages-shared/screenshots/cmd.png)

   A fenti képernyőképen igyekeztem a legkörülményes indítási parancsot ábrázolni.
   Ilyen esetben is sokat segít a TAB billentyű használata, ez ugyanis kiegészíti a beírt részeket és jelentősen meggyorsítja az olyan elérési utak beírását mint például a `python.exe` fájlé a képernyőképen.
   Ha azonban az 1. pontban a `$PATH`-hez adta a Pythont, akkor a teljes elérési út helyett elég annyit beírni, hogy `python`.

   Jelentéssor elemek:
   1. idő
   2. a számláló azonosítója (lást fent) az első eleme a szögletes zárójelben foglalt résznek
   3. a dugóka száma
   4. a nyíl után a doboz száma, mint a szögletes zárójelben foglalt rész utolsó eleme
   5. a globális sorszám (például a 32. lyukasztás olyasvalaki által, aki korábban még nem lyukasztott semelyik figyelt dobozban sem)
   6. zárójelben a doboz szerinti sorszám (például a 8. lyukasztás a 76-os dobozban)

   Az idő után csillaggal jelölt sorok egyéb adatforgalmat jeleznek.
   Ilyenkor az első bájt a parancs kódja, a második pedig a parancs hossza.
   A pélában a doboz átprogramozása történt azokon a helyeken.

   Természetesen nem csak a saját számítógépre, hanem bármilyen `IP:PORT`-on futó TCP/IP szerverre csatlakozhat, akár többre is egyszerre, mely esetben gyakorlatilag csoportosítja a dobozokat a globális sorszám tekintetében.


Engedély
--------

_Copyright © 2017, Szieberth Ádám_

Minden engedély megadva.

Ez a munka szabadon felhasználható mindennemű célból nem kizárólagosan ideértve a használatot, másolást, módosítást, közlést, terjesztést, újraengedélyezést, és az eredeti vagy a derivatív példányok üzleti célú értékesítését.


[LETÖLTÉS]: https://github.com/tajfutas/sicounter/releases/download/v0.1.2/sicounter.zip
[SICOMTRACE]: http://tajfutas.github.io/sicomtrace
