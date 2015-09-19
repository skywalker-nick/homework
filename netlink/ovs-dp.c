/*
 * lib/openvswitch/datapath.c           Open vSwitch datapath
 *
 *      This library is free software; you can redistribute it and/or
 *      modify it under the terms of the GNU Lesser General Public
 *      License as published by the Free Software Foundation version 2.1
 *      of the License.
 *
 * Copyright (c) 2013 Thomas Graf <tgraf@suug.ch>
 */

/**
 * @defgroup openvswitch Open vSwitch (libnl-ovs)
 */

/**
 * @ingroup openvswitch
 * @defgroup ovs_datapath Open vSwitch Datapath (Fast Path)
 *
 * @details
 * @{
 */
#include "ovs-dp.h"

#include <netlink-private/netlink.h>
#include <netlink-private/genl.h>
#include <netlink/netlink.h>
#include <netlink/attr.h>
#include <netlink/utils.h>
#include <netlink/object.h>
#include <netlink/openvswitch/openvswitch.h>
#include <netlink/genl/genl.h>
#include <netlink/genl/mngt.h>
#include <linux/openvswitch.h>

/** @cond SKIP */
struct ovs_dp {
        NLHDR_COMMON

        char                    dp_name[IFNAMSIZ];
        int                     dp_ifindex;
        uint32_t                dp_upcall_pid;
        uint64_t                dp_stats[OVS_DP_STAT_MAX+1];
};

#define DP_ATTR_NAME            (1 <<  0)
#define DP_ATTR_IFINDEX         (1 <<  1)
#define DP_ATTR_UPCALL_PID      (1 <<  2)
#define DP_ATTR_STATS           (1 <<  3)

static struct nl_cache_ops ovs_dp_cache_ops;
static struct nl_object_ops ovs_dp_obj_ops;
static struct genl_ops ovs_dp_ops;
/** @endcond */

static struct nla_policy ovs_dp_policy[OVS_DP_ATTR_MAX+1] = {
        [OVS_DP_ATTR_NAME]      = { .type = NLA_STRING, },
        [OVS_DP_ATTR_UPCALL_PID]= { .type = NLA_U32 },
        [OVS_DP_ATTR_STATS]     = { .minlen = sizeof(struct ovs_dp_stats) },
};

static int ovs_dp_msg_parser(struct nl_cache_ops *ops, struct genl_cmd *cmd,
                             struct genl_info *info, void *arg)
{
        struct nl_parser_param *pp = arg;
        struct ovs_header *hdr = info->userhdr;
        struct ovs_dp *dp;
        int err;

        if (!(dp = ovs_dp_alloc())) {
                err = -NLE_NOMEM;
                goto errout;
        }

        if (!info->attrs[OVS_DP_ATTR_NAME]) {
                err = -NLE_MISSING_ATTR;
                goto errout;
        }

        dp->ce_msgtype = info->nlh->nlmsg_type;

        ovs_dp_set_name(dp, nla_get_string(info->attrs[OVS_DP_ATTR_NAME]));
        ovs_dp_set_ifindex(dp, hdr->dp_ifindex);

        if (info->attrs[OVS_DP_ATTR_UPCALL_PID]) {
                uint32_t upcall = nla_get_u32(info->attrs[OVS_DP_ATTR_UPCALL_PID]);
                ovs_dp_set_upcall_pid(dp, upcall);
        }

        if (info->attrs[OVS_DP_ATTR_STATS]) {
                struct ovs_dp_stats st;

                nla_memcpy(&st, info->attrs[OVS_DP_ATTR_STATS], sizeof(st));

                dp->dp_stats[OVS_DP_STAT_HIT] = st.n_hit;
                dp->dp_stats[OVS_DP_STAT_MISSED] = st.n_missed;
                dp->dp_stats[OVS_DP_STAT_LOST] = st.n_lost;
                dp->dp_stats[OVS_DP_STAT_FLOWS] = st.n_flows;
                dp->ce_mask |= DP_ATTR_STATS;
        }

        err = pp->pp_cb(OBJ_CAST(dp), pp);
errout:
        /* pp->pp_cb() takes care of reference handling */
        ovs_dp_put(dp);

        return err;
}

/** @cond SKIP */
struct request_hdr {
        struct genlmsghdr genl_hdr;
        struct ovs_header ovs_hdr;
};
/** @endcond */

static int ovs_dp_request_update(struct nl_cache *cache, struct nl_sock *sk)
{
        struct request_hdr hdr = { };
        int err;

        if ((err = genl_resolve_id(&ovs_dp_ops)) < 0)
                return err;

        hdr.genl_hdr.cmd = OVS_DP_CMD_GET;
        hdr.genl_hdr.version = OVS_DATAPATH_VERSION;

        return nl_send_simple(sk, ovs_dp_ops.o_id, NLM_F_DUMP, &hdr, sizeof(hdr));
}

static void ovs_dp_dump_line(struct nl_object *obj, struct nl_dump_params *p)
{
        struct ovs_dp *dp = (struct ovs_dp *) obj;

        nl_dump_line(p, "%s ", dp->dp_name);

        if (dp->ce_mask & DP_ATTR_IFINDEX)
                nl_dump(p, "ifindex %u ", dp->dp_ifindex);

        if (dp->ce_mask & DP_ATTR_UPCALL_PID)
                nl_dump(p, "upcall-pid %u ", dp->dp_upcall_pid);

        nl_dump(p, "\n");
}

static void ovs_dp_dump_stats(struct nl_object *obj, struct nl_dump_params *p)
{
        struct ovs_dp *dp = (struct ovs_dp *) obj;
        
        ovs_dp_dump_line(obj, p);

        nl_dump_line(p, "    Stats:    hit     missed       lost      flows\n");
        nl_dump_line(p, "       %10" PRIu64 " %10" PRIu64 " %10" PRIu64 " %10" PRIu64 "\n",
                dp->dp_stats[OVS_DP_STAT_HIT],
                dp->dp_stats[OVS_DP_STAT_MISSED],
                dp->dp_stats[OVS_DP_STAT_LOST],
                dp->dp_stats[OVS_DP_STAT_FLOWS]);
}

static int ovs_dp_compare(struct nl_object *_a, struct nl_object *_b,
                          uint32_t attrs, int flags)
{
        struct ovs_dp *a = (struct ovs_dp *) _a;
        struct ovs_dp *b = (struct ovs_dp *) _b;
        int diff = 0;

#define DP_DIFF(ATTR, EXPR) ATTR_DIFF(attrs, DP_ATTR_##ATTR, a, b, EXPR)

        diff |= DP_DIFF(NAME,           strcmp(a->dp_name, b->dp_name));
        diff |= DP_DIFF(IFINDEX,        a->dp_ifindex != b->dp_ifindex);
        diff |= DP_DIFF(UPCALL_PID,     a->dp_upcall_pid != b->dp_upcall_pid);

#undef DP_DIFF

        return diff;
}

/**
 * @name Retrieving and Lookup
 * @{
 */

/**
 * Allocate cache and fill it with all configured datapaths
 * @arg sk              Netlink socket.
 * @arg result          Pointer to store resulting cache.
 *
 * Allocates and initializes a new datpath cache. A netlink message is sent
 * to the kernel requesting a full dump of all configured datpaths. The
 * returned messages are parsed and filled into the cache.
 *
 * @see ovs_dp_lookup()
 *
 * @return 0 on success or a negative error code.
 */
int ovs_dp_alloc_cache(struct nl_sock *sk, struct nl_cache **result)
{
        struct nl_cache *cache;
        int err;
        
        if (!(cache = nl_cache_alloc(&ovs_dp_cache_ops)))
                return -NLE_NOMEM;

        if (sk && (err = nl_cache_refill(sk, cache)) < 0) {
                nl_cache_free(cache);
                return err;
        }

        *result = cache;
        return 0;
}

/**
 * Lookup datpath by name
 * @arg cache           Dapath cache
 * @arg name            Name of datapath
 *
 * Find a datapath in the cache matching the provided named.
 *
 * @attention The reference counter of the returned datpath object will
 *            be incremented. Use ovs_dp_put() to release the reference.
 *
 * @see ovs_dp_alloc_cache(0
 * @see ovs_dp_put()
 *
 * @return Datpath object or NULL if no match was found.
 */
struct ovs_dp *ovs_dp_lookup(struct nl_cache *cache, const char *name)
{
        struct ovs_dp *dp;

        if (cache->c_ops != &ovs_dp_cache_ops)
                return NULL;

        nl_list_for_each_entry(dp, &cache->c_items, ce_list) {
                if (!strcmp(name, dp->dp_name)) {
                        nl_object_get((struct nl_object *) dp);
                        return dp;
                }
        }

        return NULL;
}

#if 0
/**
 * Get a link object directly from kernel
 * @arg sk              Netlink socket
 * @arg ifindex         Interface index
 * @arg name            Name of link
 * @arg result          Pointer to store resulting link object
 *
 * This function builds a \c RTM_GETLINK netlink message to request
 * a specific link directly from the kernel. The returned answer is
 * parsed into a struct rtnl_link object and returned via the result
 * pointer or -NLE_OBJ_NOTFOUND is returned if no matching link was
 * found.
 *
 * @route_doc{link_direct_lookup, Lookup Single Link (Direct Lookup)}
 * @return 0 on success or a negative error code.
 */
int ovs_dp_get_kernel(struct nl_sock *sk, int ifindex, const char *name,
                         struct rtnl_link **result)
{
        struct nl_msg *msg = NULL;
        struct nl_object *obj;
        int err;

        if ((err = ovs_dp_build_get_request(ifindex, name, &msg)) < 0)
                return err;

        err = nl_send_auto(sk, msg);
        nlmsg_free(msg);
        if (err < 0)
                return err;

        if ((err = nl_pickup(sk, link_msg_parser, &obj)) < 0)
                return err;

        /* We have used link_msg_parser(), object is definitely a link */
        *result = (struct ovs_dp *) obj;

        /* If an object has been returned, we also need to wait for the ACK */
         if (err == 0 && obj)
                 wait_for_ack(sk);

        return 0;
}
#endif

/** @} */

static int build_ovs_dp_msg(int cmd, const struct ovs_dp *dp, int flags,
                            struct nl_msg **result)
{
        struct nl_msg *msg;
        struct ovs_header *hdr;
        int err;

        switch (cmd) {
        case OVS_DP_CMD_NEW:
                if (!(dp->ce_mask & (DP_ATTR_NAME | DP_ATTR_UPCALL_PID))) {
                        APPBUG("name or upcall-PID must be provided");
                        return -NLE_MISSING_ATTR;
                }
                break;

        case OVS_DP_CMD_DEL:
                if (!(dp->ce_mask & (DP_ATTR_NAME | DP_ATTR_IFINDEX))) {
                        APPBUG("name or interface index must be provided");
                        return -NLE_MISSING_ATTR;
                }
                break;
        }

        if ((err = genl_resolve_id(&ovs_dp_ops)) < 0)
                return err;

        if (!(msg = nlmsg_alloc()))
                return -NLE_NOMEM;

        hdr = genlmsg_put(msg, NL_AUTO_PORT, NL_AUTO_SEQ, ovs_dp_ops.o_id,
                          sizeof(*hdr), flags, cmd, OVS_DATAPATH_VERSION);
        if (!hdr)
                goto errout;

        hdr->dp_ifindex = ovs_dp_get_ifindex(dp);

        if (dp->ce_mask & DP_ATTR_NAME &&
            nla_put_string(msg, OVS_DP_ATTR_NAME, dp->dp_name) < 0)
                goto errout;

        if (cmd == OVS_DP_CMD_NEW) {
                if (dp->ce_mask & DP_ATTR_UPCALL_PID &&
                    nla_put_u32(msg, OVS_DP_ATTR_UPCALL_PID, dp->dp_upcall_pid) < 0)
                        goto errout;
        }

        *result = msg;
        return 0;

errout:
        nlmsg_free(msg);
        return -NLE_MSGSIZE;
}

/**
 * @name Addition / Deletion
 * @{
 */

/**
 * Build Generic Netlink message requesting addition of OVS datapath
 * @arg dp              Datapath object
 * @arg flags           Additional netlink message flags (unused)
 * @arg result          Pointer to store resulting Netlink message
 *
 * Identical to ovs_dp_add() but returns message instead of sending
 * it to the kernel.
 *
 * @see ovs_dp_add()
 *
 * @return 0 on success or a negative error code.
 */
int ovs_dp_build_add_request(const struct ovs_dp *dp, int flags,
                             struct nl_msg **result)
{
        return build_ovs_dp_msg(OVS_DP_CMD_NEW, dp, flags, result);
}

/**
 * Add OVS datapath
 * @arg sk              Netlink socket.
 * @arg dp              Datapath object
 * @arg flags           Additional netlink message flags (unused)
 *
 * Builds a Generic Netlink message with command \c OVS_DP_CMD_NEW requesting
 * the addition of a new Open vSwitch datapath and sends the message to the
 * kernel.
 *
 * After sending, the function will wait for the ACK or an eventual error
 * message and thus blocks until the operation has been completed.
 *
 * @see ovs_dp_build_add_request()
 *
 * @copydoc auto_ack_warning
 *
 * @return 0 on success or a negative error code.
 */
int ovs_dp_add(struct nl_sock *sk, const struct ovs_dp *dp, int flags)
{
        struct nl_msg *msg;
        int err;
        
        err = ovs_dp_build_add_request(dp, flags, &msg);
        if (err < 0)
                return err;

        return nl_send_sync(sk, msg);
}

/**
 * Build Generic Netlink message requesting deletion of OVS datapath
 * @arg dp              Datapath object to delete
 * @arg flags           Additional netlink message flags (unused)
 * @arg result          Pointer to store resulting Netlink message
 *
 * Identical to ovs_dp_delete() but returns message instead of sending
 * it to the kernel.
 *
 * @see ovs_dp_delete()
 *
 * @return 0 on success or a negative error code.
 */
int ovs_dp_build_delete_request(const struct ovs_dp *dp, int flags,
                                struct nl_msg **result)
{
        return build_ovs_dp_msg(OVS_DP_CMD_DEL, dp, flags, result);
}

/**
 * Delete OVS datapath
 * @arg sk              Netlink socket.
 * @arg dp              Datapath object
 * @arg flags           Additional netlink message flags (unused)
 *
 * Builds a Generic Netlink message with command \c OVS_DP_CMD_DEL requesting
 * the deletion of a new Open vSwitch datapath and sends the message to the
 * kernel.
 *
 * After sending, the function will wait for the ACK or an eventual error
 * message and thus blocks until the operation has been completed.
 *
 * @see ovs_dp_build_add_request()
 *
 * @copydoc auto_ack_warning
 *
 * @return 0 on success or a negative error code.
 */
int ovs_dp_delete(struct nl_sock *sk, const struct ovs_dp *dp, int flags)
{
        struct nl_msg *msg;
        int err;
        
        if ((err = ovs_dp_build_delete_request(dp, 0, &msg)) < 0)
                return err;

        return nl_send_sync(sk, msg);
}

/** @} */

/**
 * @name Accessing Datapath Attributes
 * @{
 */

/**
 * Allocate Open vSwitch Datapath
 *
 * @see ovs_dp_put()
 * @return New datapath object or NULL if allocation failed
 */
struct ovs_dp *ovs_dp_alloc(void)
{
        return (struct ovs_dp *) nl_object_alloc(&ovs_dp_obj_ops);
}

/**
 * Give up reference to a datpath object
 * @arg dp              Datapath object
 */
void ovs_dp_put(struct ovs_dp *dp)
{
        nl_object_put(OBJ_CAST(dp));
}

/**
 * Set datpath name
 * @arg dp              Datapath object
 * @arg name            New name
 *
 * @copydoc read_only_attribute
 * @see ovs_dp_get_name()
 */
void ovs_dp_set_name(struct ovs_dp *dp, const char *name)
{
        strncpy(dp->dp_name, name, sizeof(dp->dp_name) - 1);
        dp->ce_mask |= DP_ATTR_NAME;
}

/**
 * Return datpath name
 * @arg dp              Datapath object
 *
 * @see ovs_dp_set_name()
 * @return Datapath name or NULL if name is not specified
 */
const char *ovs_dp_get_name(const struct ovs_dp *dp)
{
        return dp->ce_mask & DP_ATTR_NAME ? dp->dp_name : NULL;
}

/**
 * Set interface index of datapath port
 * @arg dp              Datapath object
 * @arg ifindex         Interface index
 *
 * @see ovs_dp_get_ifindex()
 */
void ovs_dp_set_ifindex(struct ovs_dp *dp, int ifindex)
{
        dp->dp_ifindex = ifindex;
        dp->ce_mask |= DP_ATTR_IFINDEX;
}

/**
 * Return interface index of datapath port
 * @arg dp              Datapath object
 *
 * @see ovs_dp_set_ifindex()
 *
 * @return Interface index or 0 if not set.
 */
int ovs_dp_get_ifindex(const struct ovs_dp *dp)
{
        return dp->dp_ifindex;
}

/**
 * Set upcall PID
 * @arg dp              Datapath object
 * @arg pid             Upcall PID
 *
 * @see ovs_dp_get_upcall_pid()
 */
void ovs_dp_set_upcall_pid(struct ovs_dp *dp, int pid)
{
        dp->dp_upcall_pid = pid;
        dp->ce_mask |= DP_ATTR_UPCALL_PID;
}

/**
 * Return upcall PID
 * @arg dp              Datapath object
 *
 * @see ovs_dp_set_upcall_pid()
 *
 * @return Upcall PID or 0 if not set.
 */
int ovs_dp_get_upcall_pid(const struct ovs_dp *dp)
{
        return dp->dp_upcall_pid;
}

/** @} */

/**
 * @name Statistics
 * @{
 */

/**
 * Return value of datapath statistics counter
 * @arg dp              Datapath object
 * @arg id              Identifier of statistical counter
 *
 * @return Value of counter or 0 if not specified.
 */
uint64_t ovs_dp_get_stat(const struct ovs_dp *dp, ovs_dp_stat_id_t id)
{
        if (id > OVS_DP_STAT_MAX)
                return 0;

        return dp->dp_stats[id];
}

/**
 * Set value of datpath statistics counter
 * @arg dp              Datpath object
 * @arg id              Identifier of statistical counter
 * @arg value           New value
 *
 * \note Changing the value of a statistical counter will not change the
 *       value in the kernel.
 *
 * @return 0 on success or a negative error code
 */
int ovs_dp_set_stat(struct ovs_dp *dp, ovs_dp_stat_id_t id,
                    const uint64_t value)
{
        if (id > OVS_DP_STAT_MAX)
                return -NLE_INVAL;

        dp->dp_stats[id] = value;

        return 0;
}


static const struct trans_tbl dp_stats[] = {
        __ADD(OVS_DP_STAT_HIT, hit)
        __ADD(OVS_DP_STAT_MISSED, missed)
        __ADD(OVS_DP_STAT_LOST, lost)
        __ADD(OVS_DP_STAT_FLOWS, flows)
};

/**
 * Translate datapath statistic ID to name
 * @arg st              Datapath statistic identifier
 * @arg buf             Buffer to store name
 * @arg len             Length of buffer
 *
 * @return Pointer to buffer
 */
const char *ovs_dp_stat2str(ovs_dp_stat_id_t st, char *buf, size_t len)
{
        return __type2str(st, buf, len, dp_stats, ARRAY_SIZE(dp_stats));
}

/**
 * Translate datapath statistic name to identifier
 * @arg name            Name of datapath statistic identifier
 *
 * @return Numeric identifier if found or NULL
 */
int ovs_dp_str2stat(const char *name)
{
        return __str2type(name, dp_stats, ARRAY_SIZE(dp_stats));
}

/** @} */

static struct nl_object_ops ovs_dp_obj_ops = {
        .oo_name                = "openvswitch/datapath",
        .oo_size                = sizeof(struct ovs_dp),
        .oo_dump = {
            [NL_DUMP_LINE]      = ovs_dp_dump_line,
            [NL_DUMP_STATS]     = ovs_dp_dump_stats,
        },
        .oo_compare             = ovs_dp_compare,
        .oo_id_attrs            = DP_ATTR_NAME,
};

static struct genl_cmd ovs_dp_cmds[] = {
        {
                .c_id           = OVS_DP_CMD_NEW,
                .c_name         = "NEW_DATAPATH" ,
                .c_maxattr      = OVS_DP_ATTR_MAX,
                .c_attr_policy  = ovs_dp_policy,
                .c_msg_parser   = ovs_dp_msg_parser,
        },
        {
                .c_id           = OVS_DP_CMD_DEL,
                .c_name         = "DEL_DATAPATH" ,
        },
        {
                .c_id           = OVS_DP_CMD_GET,
                .c_name         = "GET_DATAPATH" ,
                .c_maxattr      = OVS_DP_ATTR_MAX,
                .c_attr_policy  = ovs_dp_policy,
                .c_msg_parser   = ovs_dp_msg_parser,
        },
        {
                .c_id           = OVS_DP_CMD_SET,
                .c_name         = "SET_DATAPATH" ,
        },
};

static struct genl_ops ovs_dp_ops = {
        .o_cmds                 = ovs_dp_cmds,
        .o_ncmds                = ARRAY_SIZE(ovs_dp_cmds),
};

static struct nl_cache_ops ovs_dp_cache_ops = {
        .co_name                = "openvswitch/datapath",
        .co_hdrsize             = GENL_HDRSIZE(sizeof(struct ovs_header)),
        .co_msgtypes            = GENL_FAMILY(GENL_ID_GENERATE, "ovs_datapath"),
        .co_genl                = &ovs_dp_ops,
        .co_protocol            = NETLINK_GENERIC,
        .co_request_update      = ovs_dp_request_update,
        .co_obj_ops             = &ovs_dp_obj_ops,
};

static void __init ovs_datapath_init(void)
{
        if (genl_register(&ovs_dp_cache_ops) < 0)
                BUG();
}

static void __exit ovs_datapath_exit(void)
{
        genl_unregister(&ovs_dp_cache_ops);
}

/** @} */
