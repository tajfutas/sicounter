<a href="https://github.com/tajfutas/sicounter/blob/master/readme.md"><img alt="English documentation" src="https://raw.githubusercontent.com/tajfutas/sicounter/master/icons/flag_usa.png"/></a>

SICOUNTER (SportIdent lyukasztás és kiolvasás számláló)
=======================================================

v0.11
Készítette: Szieberth Ádám


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
  A számláló a behelyezés pillanatában lép tovább.
  Csak olyan _Readout_ módba állított dobozok esetén működik, melyeken nem lett beállítva _auto send_: ezt nevezi a SportIdent dokumentáció _handshake_ (azaz kézfogásos) módú kilvasásnak.
  Itt csupán a dugokák behelyezését és a kivételét küldi el a doboz automatikusan, az adatokat az így értesült szofvernek ezután külön ki kell kérnie a lyukasztási adatokat amíg a dugóka a dobozban van.
  A be- és kihelyezési üzenet csak a dugóka számát tartalmazza 4 bájton, ez tehát villámgyorsan érkezik.

* _RO_:
  Ez számlálja a kiolvasódobozból érkezett lyukasztási 128 bájt hosszú adatcsomagok közül az elsők beérkezését.
  Azért az elsőkét, mert az a csomag tartalmazza a dugóka számát, más adat pedig a számláló szempontjából nem lényeges.
  Ez a számláló minden kiolvasódoboz esetében emelkedni fog.
  Amennyiben a kiolvasás több dobozba és _handshake_ módban történik, úgy érdemes előnyben részesíteni az _IN_ számlálót, ám nagyon kis esélyt látok arra, hogy bármikor más értéket mutasson a kettő: ahhoz azonos időpillanatban kell kiolvasni több versenyzőnek, és az adatokat kérő szofvernek pedig eltérő ütemben reagálni az első kiolvasó kárára.

A SICOUNTER naplózza is a számlálók alkulását a `SICOUNTER.LOG` fájlba, így egy esetleges újraindítás után is zavartalanul tudja folytatni a számlálást.

Ezen kívül a SICOUNTER jelzi a számlálás szempontjából érdektelen adatforgalmat is: ebben az esetben az utasítási bájtot és a hosszbájtot mutatja meg kettő csillag jel után.

Fontos tudni, hogy a SICOUNTER nem ír semmit a SportIdent doboz felé, csak olvassa az onnan jövő adatokat.


Telepítés és használat
----------------------

1. Töltse le és telepítse a [_Python 3_ legújabb verzióját](https://www.python.org/downloads/)!
   Remélhetőleg a telepítő fel fogja ajánlani, hogy a `python.exe` fájl elérési útját hozzáadja a `$PATH` környezeti változóhoz, így nem kell a teljes elérési utat megadni indításkor.
   Éljünk ezzel a lehetőséggel.

2. Telepítse és indítsa a [SICOMTRACE-et](https://github.com/tajfutas/sicomtrace/blob/master/olvassel.md) minden egyes dobozra, amelyen számlálást kíván végezni.
   Amennyiben a dobozok azonos számítógéphez kapcsolódnak, akkor a TCP/IP szervereket más-más portokra kell állítani. A SICOUNTER ezekhez fog kapcsolódni.

3. Nyisson egy Parancssort (Start gomb > Keresés `cmd`-re).
   Lépjen be a könyvtárba ahol a naplófájlok lesznek.
   Innen indítsa a SICOUNTER szkriptet a Python segítségével.
   A program ettől kezdve számlálja a lyukasztásokat, a kiolvasási behelyezéseket és a kiolvasásokat.
   
   ![SICOUNTER szkript parancssorból](https://raw.githubusercontent.com/tajfutas/sicounter/master/screenshots/cmd.png)

   Ha a képernyőkép alapján nem sikerül indítania a SICOUNTERT, akkor lehetséges, hogy a `python.exe` vagy a `sicounter.py`, vagy mindkettő teljes elérési útját meg kell adni a parancsban.
   Például `E:\verseny_adat>"c:\Program Files (x86)\Python36-32\python.exe" e:\sicounter\sicounter.py 192.168.1.111:7487`.

   Jelentéssor elemek:
   1. idő
   2. számláló azonosítója szögletes zárójelben (lást fent)
   3. a dugóka számláló szerinti értéke, minden figyelt dobozra vonatkozólag (például a tizedik lyukasztás mind közül, vagy a huszonötödik kiolvasás mind közül)
   4. a dugóka melyik számú dobozba lett behelyezve, szögletes zárójelben
   5. a dugóka számláló szerinti értéke, az adott dobozra vonatkozólag (például a nyolcadik lyukasztás a 88-as dobozban)
   6. perjel, majd a doboz számláló szerinti értéke a dugókára vonatkozólag (például az adott dugóka harmadik lyukasztott doboza volt az iménti 88-as)

