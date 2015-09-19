import netlink
import pprint
import cStringIO

def get_iface():
    con = netlink.new_generic()
    hdr  = netlink.new_genlmsg(
            {
                "cmd": netlink.NL80211_CMD_GET_SCAN,
                "version": 0,
                "reserved": 0
                }
            ) 
    attr = netlink.newnlattr(netlink.NL80211_ATTR_IFINDEX, netlink.new_policy_u32(3)) 
    payload = netlink.generic_wireless(hdr+attr, 0x12345) 
    con.send(payload) 
    d = con.recv(4096)
    b = cStringIO.StringIO(d)
    msg = netlink.parse_nlmsg(b)
    mlen = b.tell() - 16 + msg["len"]
    payload = netlink.parse_genlmsg(b) 
    attrs = netlink.parse_attrs(b, mlen) 
    return {
            "msg": msg,
            "payload": payload,
            "attrs": attrs
            }
    

pprint.pprint(get_iface())
