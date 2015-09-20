from __future__ import print_function, unicode_literals, division 
from future_builtins import *

import os
import socket
import struct
import pprint
import cStringIO

NETLINK_GENERIC = 16
NETLINK_ROUTE = 0
RTM_GETROUTE = 26
RT_SCOPE_UNIVERSE = 0
RT_TABLE_DEFAULT = 253

F_REQUEST = 1
F_ROOT = 0x100
F_MATCH = 0x200
F_AOTMIC = 0x400
F_DUMP = F_ROOT | F_MATCH

nlmsg = (("len", "I"),
         ("type", "H"),
         ("flags", "H"),
         ("seq", "I"),
         ("pid", "I"))

nlattr = (("len", "H"),
          ("type", "H"))

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

def parse_nlattr(b):
    at = parse_struct(b, nlattr)
    prev = b.tell()
    at["payload"] = b.read(at["len"] - 4)
    mark = b.tell()
    #align 4
    if mark % 4:
        b.seek(4 - (mark % 4), io.SEEK_CUR)
    return at

def parse_attrs(b, mlen):
    attrs = []
    while b.tell() < mlen:
        attr = parse_nlattr(b)
        attrs.append(attr)
    return attrs

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

def new_nlmsg(tp, payload, seq, flags=F_REQUEST, pid=0):
    return new_struct({
        "len": 16 + len(payload),
        "type": tp,
        "flags": flags,
        "seq": seq,
        "pid": pid
        }, nlmsg) + payload

def parse_struct(b, fmt):
    d = {}
    fmts = "".join([x[1] for x in fmt])
    raw = b.read(struct.calcsize(fmts))
    raw = struct.unpack(fmts, raw)
    for i, item in enumerate(fmt):
        d[item[0]]= raw[i]
    return d

def parse_nlmsg(b):
    return parse_struct(b, nlmsg)

#for GETROUTE
rtmsg = (
        ("family", "B"),
        ("dst_len", "B"),
        ("src_len", "B"),
        ("tos", "B"),
        ("table", "B"),
        ("protocol", "B"),
        ("scope", "B"),
        ("type", "B"),
        ("flags", "I")
        )


def new_rtmsg(d):
    return new_struct(d, rtmsg)

def parse_rtmsg(b):
    return parse_struct(b, rtmsg)

def route_message(payload, seq):
    hdr = new_nlmsg(RTM_GETROUTE, payload, seq, flags=F_REQUEST|F_DUMP)
    return hdr

def get_routes():
    con = new_conn(NETLINK_ROUTE)
    hdr = new_rtmsg({'family': 0,
                     'dst_len': 0,
                     'src_len': 0,
                     'tos': 0,
                     'table': RT_TABLE_DEFAULT,
                     'protocol': 0,
                     'scope': RT_SCOPE_UNIVERSE,
                     'type': 0,
                     'flags': 0})
    payload = route_message(hdr, 0x12345)

    con.send(payload) 
    d = con.recv(4096)

    prettify(d)

    b = cStringIO.StringIO(d)
    msg = parse_nlmsg(b)
    mlen = b.tell() - 16 + msg["len"]
    payload = parse_rtmsg(b)
    attrs = parse_attrs(b, mlen)
    return {
            "msg": msg,
            "payload": payload,
            "attrs": attrs
            }

def prettify(message):
    pprint.pprint(message)

prettify(get_routes())

