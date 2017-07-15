<a href="https://github.com/tajfutas/sicomtrace/blob/master/readme.md"><img alt="English documentation" src="https://raw.githubusercontent.com/tajfutas/sicomtrace/master/icons/flag_usa.png"/></a>

SICOUNTER (SportIdent lyukasztás és kiolvasás számláló)
=======================================================

v0.1
Készítette: Szieberth Ádám


Bevezetés
---------

The `sicounter.py`szkript segítségével számlálhatja az egy vagy több SportIdent dobozba történt lyukasztásokat vagy kiolvasásokat.

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


Telepítés és használat
----------------------
