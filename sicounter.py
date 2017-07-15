import asyncio
import datetime
import os
import re
import struct

inserted = set()
readed_out = set()
transmitted = set()
LOG_FILE = 'sicounter.log'

def nowstr():
  N = datetime.datetime.now()
  return f'{N:%H:%M:%S}.' + f'{round(N.microsecond/10000):0>2}'


def get_siid(siid_data):
    siid = struct.unpack('>L', b'\x00' + siid_data[1:4])[0]
    if siid < 500000:
      series = siid_data[1]
      number = struct.unpack('>H', siid_data[2:4])[0]
      siid = 100000 * series + number
    return siid


def init_sets():
  re_pat_log_s = '^[\d:\.]+?\s+(\w\w)-(\d+)\s+\((\d+)\)$'
  re_pat_log = re.compile(re_pat_log_s)
  events = {'IN': inserted, 'RO': readed_out, 'TR': transmitted}
  if LOG_FILE and os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf8') as f:
      log_entries = f.readlines()
  for row in log_entries:
    print(row[:-1])
    m = re_pat_log.match(row[:-1])
    if m:
      ev, nr, siid = m.groups()
      events[ev].add(int(siid))


class Protocol(asyncio.Protocol):

  CMD = {
      b'\xB1': 'on_read_out_si5',
      b'\xD3': 'on_transmit_record',
      b'\xE1': 'on_read_out_si6',
      b'\xE5': 'on_inserted',
      b'\xE6': 'on_inserted',
      b'\xE7': 'on_ignored',
      b'\xE8': 'on_inserted',
      b'\xEA': 'on_ignored',
      b'\xEF': 'on_read_out_si8',
    }
  STATES = 'stx', 'cmd', 'len', 'body', 'crc', 'etx'

  def reset(self):
    self.buf = bytearray()
    self.state = 0

  def connection_made(self,transport):
    self.reset()
    self.tr = transport

  def data_received(self, data):
    #print(data)
    self.buf.extend(data)
    self.data_received_on_state()

  def data_received_on_state(self):
    state = self.STATES[self.state]
    methodname = f'data_received_on_{state}'
    #print(methodname, self.buf)
    getattr(self, methodname)()

  def data_received_on_stx(self):
    for i, b in enumerate(self.buf):
      if b == 2:
        break
    else:
      self.reset()
      return
    self.buf = self.buf[i:]
    self.state += 1
    self.data_received_on_state()

  def data_received_on_cmd(self):
    if len(self.buf) < 2:
      return
    self.state += 1
    self.data_received_on_state()

  def data_received_on_len(self):
    if len(self.buf) < 3:
      return
    self.state += 1
    self.data_received_on_state()

  def data_received_on_body(self):
    bodylen = self.buf[2]
    if len(self.buf) < 3 + bodylen:
      return
    self.state += 1
    self.data_received_on_state()

  def data_received_on_crc(self):
    bodylen = self.buf[2]
    if len(self.buf) < 5 + bodylen:
      return
    self.state += 1
    self.data_received_on_state()

  def data_received_on_etx(self):
    cmd_code = self.buf[1]
    bodylen = self.buf[2]
    if len(self.buf) < 6 + bodylen:
      return
    cmd = self.CMD.get(bytes(self.buf[1:2]), '')
    if cmd:
      getattr(self, cmd)()
    else:
      self.print(f'{nowstr()} * {cmd_code:0>2X} {bodylen:0>2X}')
      #    for x in command_bytes))
      #command_bytes = self.buf[:6 + bodylen]
      #print(f'{nowstr()} * ' + ' '.join(f'{x:0>2X}'
      #    for x in command_bytes))
    self.state = 0
    self.buf = self.buf[6 + bodylen:]
    self.data_received_on_state()

  def on_ignored(self):
    pass

  def on_inserted(self):
    siid_data = self.buf[5:9]
    siid = get_siid(siid_data)
    if siid in inserted:
      return
    inserted.add(siid)
    self.print(f'{nowstr()} IN-{len(inserted)} ({siid})')

  def on_read_out(self, siid_data):
    siid = get_siid(siid_data)
    if siid in readed_out:
      return
    readed_out.add(siid)
    self.print(f'{nowstr()} RO-{len(readed_out)} ({siid})')

  def on_read_out_si5(self):
    chip_data = self.buf[5:133]
    cns = chip_data[0x06:0x07]
    sn1sn0 = chip_data[0x11:0x13]
    siid_data = b'\x00' + cns + sn1sn0
    self.on_read_out(siid_data)

  def on_read_out_si6(self):
    bn = self.buf[5]
    if bn == 0:
      chip_data = self.buf[6:134]
      siid_data = chip_data[0x1A:0x1E]
      self.on_read_out(siid_data)

  def on_read_out_si8(self):
    bn = self.buf[5]
    if bn == 0:
      chip_data = self.buf[6:134]
      siid_data = chip_data[0x18:0x1C]
      self.on_read_out(siid_data)

  def on_transmit_record(self):
    siid_data = self.buf[5:9]
    siid = get_siid(siid_data)
    if siid in transmitted:
      return
    transmitted.add(siid)
    self.print(f'{nowstr()} TR-{len(transmitted)} ({siid})')

  def print(self, s):
    print(s)
    if LOG_FILE:
      with open(LOG_FILE, 'a', encoding='utf8') as f:
        f.write(s + '\n')




def main():
  global LOG_FILE

  import sys

  print('SICOUNTER v0.1 by Szieberth Adam')

  LOG_FILE = 'sicounter.log'
  re_pat = re.compile(
      r'^(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
      r'(?::(?P<port>\d{1,5}))?$'
    )
  addresses = set()
  if len(sys.argv) < 2:
    print('Usage: python sicounter.py '
        '<TCP_HOST_1> [TCP_HOST_2 ...]')
    print('"D" as host is a shortcut to default localhost '
        '(127.0.0.1:7487)')
    sys.exit(1)
  for a in sys.argv[1:]:
    if a.lower() == 'default'[:min(len(a), 7)]:
      a = '127.0.0.1:7487'
    m = re_pat.match(a)
    if not m:
      print(f'Invalid address: {a}')
      print('Valid address formats: XXX.XXX.XXX.XXX; '
          'XXX.XXX.XXX.XXX:YYYYY')
      sys.exit(1)
    host, port = m.groups()
    if not port:
      port = '7487'
    if not all((0 <= int(x) <= 255) for x in host.split('.')):
      print(f'Invalid IP address: {host}')
      sys.exit(1)
    if not (0 < int(port) <= 65535):
      print(f'Invalid port: {port}')
      sys.exit(1)
    addresses.add((host, port))

  init_sets()

  loop = asyncio.get_event_loop()

  for (host, port) in addresses:
    coro = loop.create_connection(Protocol, host=host,
        port=port)
    try:
      loop.run_until_complete(coro)
    except OSError as e:
      print(e)
      sys.exit(2)
    else:
      print(f'connected to {host}:{port}')

  # https://stackoverflow.com/a/36925722/2334951
  async def wakeup():
      while True:
          await asyncio.sleep(1)
  wakeup_task = asyncio.async(wakeup())

  try:
    loop.run_forever()
  except (KeyboardInterrupt, SystemExit):
    pass
  finally:
    print('exiting...')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()
    loop.run_forever()
    loop.close()

  sys.exit(0)


if __name__ == '__main__':
  main()