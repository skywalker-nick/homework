#define GENL_ID_GENERATE	0
#define END_OF_MSGTYPES_LIST	{ -1, -1, NULL }

enum {
        NL_ACT_UNSPEC,
        NL_ACT_NEW,
        NL_ACT_DEL,
        NL_ACT_GET,
        NL_ACT_SET,
        NL_ACT_CHANGE,
        __NL_ACT_MAX,
};

#define GENL_FAMILY(id, name) \
        { \
                { id, NL_ACT_UNSPEC, name }, \
                END_OF_MSGTYPES_LIST, \
        }



#define NLMSG_ALIGNTO   4U
#define NLMSG_ALIGN(len) ( ((len)+NLMSG_ALIGNTO-1) & ~(NLMSG_ALIGNTO-1) )

struct genlmsghdr {
        __u8    cmd;
        __u8    version;
        __u16   reserved;
};

#define GENL_HDRLEN     NLMSG_ALIGN(sizeof(struct genlmsghdr))
#define GENL_HDRSIZE(hdrlen) (GENL_HDRLEN + (hdrlen))

