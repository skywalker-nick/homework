def nb_lock(func):
    def wrapped(*argv, **kwargs):
        print 'func start...'
        print argv
        print kwargs
        result = func(*argv, **kwargs)
        print 'func end...'
        return result
    return wrapped


class ABC(object):

    def __init__(self):
        pass

    @nb_lock
    def abc(self, context, id):
        pass


a = ABC()
a.abc('aaa', 'bbb')
