import socket
import struct
import pprint
import cStringIO

NETLINK_GENERIC = 16

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

def get_iface():
    con = new_generic()
    hdr  = new_genlmsg(
            {
                "cmd": netlink.NL80211_CMD_GET_SCAN,
                "version": 0,
                "reserved": 0
                }
            ) 
    attr = newnlattr(netlink.NL80211_ATTR_IFINDEX, new_policy_u32(3)) 
    payload = netlink.generic_wireless(hdr+attr, 0x12345) 
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
    

pprint.pprint(get_iface())
