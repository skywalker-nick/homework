from __future__ import print_function, unicode_literals, division 
from future_builtins import *

import socket
import struct
import pprint
import cStringIO

NETLINK_GENERIC = 16
F_REQUEST = 1
F_ROOT = 0x100
F_MATCH = 0x200
F_AOTMIC = 0x400
F_DUMP = F_ROOT | F_MATCH

genlmsg = (("cmd", "B"),
           ("version", "B"),
           ("reserved", "H"))

nlmsg = (("len", "I"),
         ("type", "H"),
         ("flags", "H"),
         ("seq", "I"),
         ("pid", "I"))

nlattr = (("len", "H"),
          ("type", "H"))

def new_conn(proto):
    s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, proto)
    s.bind((0, 0))
    return s

def new_struct(d, fmt):
    l = []
    fmts = "".join([x[1] for x in fmt])
    for i in fmt:
        l.append(d[i[0]])
    return struct.pack(fmts, *l)

def new_generic():
    return new_conn(NETLINK_GENERIC)

def new_nlmsg(tp, payload, seq, flags=F_REQUEST, pid=0):
    return new_struct({
        "len": 16 + len(payload),
        "type": tp,
        "flags": flags,
        "seq": seq,
        "pid": pid
        }, nlmsg) + payload

def new_genlmsg(d):
    return new_struct(d, genlmsg)

def newnlattr(tp, payload):
    x = new_struct({
        "len": 4 + len(payload),
        "type": tp
        }, nlattr) + payload
    l = len(x)
    #padding, align 4
    if l % 4:
        return x + "\x00" * (4 - l % 4)
    return x

def new_policy_u32(num):
    return struct.pack("I", num)

def parse_struct(b, fmt):
    d = {}
    fmts = "".join([x[1] for x in fmt])
    raw = b.read(struct.calcsize(fmts))
    raw = struct.unpack(fmts, raw)
    for i, item in enumerate(fmt):
        d[item[0]]= raw[i]
    return d

def parse_nlattr(b):
    at = parse_struct(b, nlattr)
    prev = b.tell()
    at["payload"] = b.read(at["len"] - 4)
    mark = b.tell()
    #align 4
    if mark % 4:
        b.seek(4 - (mark % 4), io.SEEK_CUR)
    return at

def parse_nlmsg(b):
    return parse_struct(b, nlmsg)

def parse_genlmsg(b):
    return parse_struct(b, genlmsg)

def parse_attrs(b, mlen):
    attrs = []
    while b.tell() < mlen:
        attr = parse_nlattr(b)
        attrs.append(attr)
    return attrs

def generic_wireless(payload, seq):
    hdr = new_nlmsg(25, payload, seq, flags=F_REQUEST|F_DUMP)
    return hdr

NL80211_ATTR_IFINDEX = 3
NL80211_CMD_GET_SCAN = 32

def get_iface():
    con = new_generic()
    hdr  = new_genlmsg(
            {
                "cmd": NL80211_CMD_GET_SCAN,
                "version": 0,
                "reserved": 0
                }
            ) 
    attr = newnlattr(NL80211_ATTR_IFINDEX, new_policy_u32(3)) 
    payload = generic_wireless(hdr+attr, 0x12345) 
    con.send(payload) 
    d = con.recv(4096)
    b = cStringIO.StringIO(d)
    msg = parse_nlmsg(b)
    mlen = b.tell() - 16 + msg["len"]
    payload = parse_genlmsg(b) 
    attrs = parse_attrs(b, mlen) 
    return {
            "msg": msg,
            "payload": payload,
            "attrs": attrs
            }

def prettify(message):
#    message['attrs'][0]['payload'] = message['attrs'][0]['payload'].decode('UTF-8')
    pprint.pprint(message)

prettify(get_iface())

