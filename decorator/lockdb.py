# Copyright (c) 2015 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import eventlet
eventlet.monkey_patch()

import inspect
import random
import time

import six


# Used to identify each API session
LOCK_SEED = 9876543210

# Used to wait and retry for Galera
DB_INIT_RETRY_INTERVAL = 1
DB_MAX_RETRY_INTERVAL = 10

# Used to wait and retry for distributed lock
LOCK_MAX_RETRIES = 100
LOCK_INIT_RETRY_INTERVAL = 2
LOCK_MAX_RETRY_INTERVAL = 10
LOCK_INC_RETRY_INTERVAL = 1

# global lock id
GLOBAL_LOCK_ID = "ffffffffffffffffffffffffffffffff"


class wrap_db_lock(object):

    def __init__(self):
        super(wrap_db_lock, self).__init__()

    def __call__(self, f):
        @six.wraps(f)
        def wrap_db_lock(*args, **kwargs):

            # magic to prevent from nested lock
            within_wrapper = False
            for frame in inspect.stack()[1:]:
                if frame[3] == 'wrap_db_lock':
                    within_wrapper = True
                    break

            if not within_wrapper:
                print '%s: not with_wrapper' % str(self)
            else:
                print 'with in wrapper'

            try:
                result = f(*args, **kwargs)
            except Exception as e:
                pass
            return result
        return wrap_db_lock

