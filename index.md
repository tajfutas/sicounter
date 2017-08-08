---
layout: page
title: SICOUNTER
subtitle: SportIdent Punch and Read Out Counter
version: 0.1.3
repo: "https://github.com/tajfutas/sicounter"
download: "https://github.com/tajfutas/sicounter/releases/download/v0.1.3/sicounter.zip"
---


Introduction
------------

With the `sicounter.py` _Python 3_ script you can count the punches or read outs of one or more SportIdent stations.

Originally it was developed for the [Hungary Cup 2017](http://adatbank.mtfsz.hu/esemeny/show/esemeny_id/6363) with the desire to count the finished runners and be able to give gifts to each one hundredth of them.
The task got complicated by the fact that there were multiple finish and read out stations and in advance it was uncertain whether the finish stations would be wired into the computer network, so to have a plan B, the support of read out stations had to get developed as well.
Moreover, there are two kinds of read out mechanism: handshake ahd auto send.

To support all the above scenarios, SICOUNTER has three distinct counters:

* _TR_:
  This counts the punches of auto send control staions (Clear, Check, Start, Control, Finish).
  The types of the stations are ignored by this counter which result no distinction between the punches on different station types.

* _IN_:
  This counts the inserts into Read Out stations.
  The counter steps at the moment a new SI dongle gets inserted into the station but before the actual readed out of data.
  This counter works for Read Out stations with auto send set to off: this is called read out in handshake mode by the SportIdent reference.
  In this mode the station auto sends the insert or remove events with the chip number, and it is up to the software to command the station to send the any of the data chunks during the time the dongle is within the staion.
  The insert and remove message arrives lightning fast as it is very short containing only four bytes of payload with the chip number.

* _RO_:
  This counts the first incoming read out data blocks from the Read Out stations.
  The second and subsequent data blocks are irrelevant as the first one contains the chip number which is the only one the counter needs.
  Note that in handshake mode this data has to get asked explicitly by the organizer software, as it will not get sended automatically.
  As the block sizes are 128 bytes, this data arrives slower than those for the _IN_ counter.

As a matter of fact, the SICOUNTER deals ordinal numbers to the SportIdent chips.
The given numbers are fixed and will not change due to subsequent punches or read outs.
It is the first action what matters.

If someone does the action with a corresponding counter for the first time (e.g. punches) then a number get allocated to her dongle.
Subsequent punches wll not change the allocated number.
A second number gets allocated too, this time for the station and it indicates her place in the given station.
This latter number are shown inside parentheses.
For example somewone is the Nr 126 person who readed out in any of the three monitored read out stations, but the same person is also the Nr 48 who readed out in that particular station.

SICOUNTER logs the events in the `SICOUNTER.LOG` file which is loaded at start time, so the state of the counters are saved in case a restart is needed.

SICOUNTER also indicates the incoming data of other type which is unnecessary for the counters: after a star, the command and the length bytes are shown.

It is important to know that SICOUNTER never writes to the stations, it only passively reads the sended data.


Telepítés és használat
----------------------

1. Download and install the newest [_Python 3_ version](https://www.python.org/downloads/)!
   Hopefully the installer will offer you to add `python.exe` to the `$PATH` environment variable of the operating system.
   This one spares you the typing of full path of the Python executable into the command prompt when you want to start SICOUNTER.
   I advise you to pick that option.

2. Install and start [SICOMTRACE] for each SportIdent stations you want to monitor.
   In case of multiple stations connected to a single computer, different port numbers are required for the TCP/IP servers.
   SICOUNTER will connect to those servers.

3. [Download][DOWNLOAD] and unpack SICOUNTER to a directory you prefer.

3. Open a Command Prompt (Start button > Search for `cmd`).
   Go to the directory where you want to store the `SICOUNTER.LOG`file.
   From this location, start SICOUNTER with Python.
   The program will monitor the punches, inserts and read outs from that time.
   
   ![SICOUNTER in Command Prompt](https://raw.githubusercontent.com/tajfutas/sicounter/gh-pages-shared/screenshots/cmd.png)

   In the above screenshot I intended to present the most complicated command to start SICOMTRACE.
   This way the TAB completion really helps as it spares you the manual typing of the path by rotating the possible valid the path parts based on the typed part as for the `python.exe` in the screenshot.
   In case you added Python to the system path, then you can spare to type that long pathname of the EXE file as it can be replaced by a single word, `python`.

   Parts of the reported lines:
   1. time
   2. counter type (see above) is the first element of the part in square brackets
   3. chip number
   4. after the arrow, the station number as the last element of the part in square brackets
   5. global counter number (e.g. the 32th punch by someone who was not punched before in any of the monitored stations)
   6. counter number for the station (e.g. the 8th distinct punch in the station 76)

   The lines with star signs after the time indicate other kind of data.
   For these lines, the first hexadecimal number is the command byte and the second is the length byte.
   In the screenshot above, those lines were made due to reprogramming of the station by Config+.

   Naturally, connection can be made to not only the local TCP/IP server, but also to any number of remote servers with a known `IP:PORT` address.
   With more than one connection, the stations are effectively grouped in the aspect of the global counter.


Licence
-------

_Copyright © 2017, Szieberth Ádám_

All permissions are granted.

This work is free for any kind of usage, including but not limited to copy, modify, publish, distribute, sublicense, and to sell original or derivative copies of it.


[DOWNLOAD]: {{ page.download }}
[SICOMTRACE]: https://foot-o.github.io/sicomtrace
