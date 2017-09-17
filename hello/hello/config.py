import os

class ContainerConfig(object):
    def __init__(self):
        """ build a flask config object out of environment variables """

        bind_object = {}
        bools = {'True': True, 'False': False}

        for k, v in os.environ.iteritems():
            if k.startswith('HELLO_'):
                if k == 'HELLO_BINDS_MASTER':
                    bind_object['master'] = v
                elif k == 'HELLO_BINDS_SLAVE':
                    bind_object['slave'] = v
                else:
                    var_name = k.split('HELLO_')[1]
                    if v in bools.keys():
                        setattr(self, var_name, bools[v])
                    else:
                        setattr(self, var_name, v)

        if len(bind_object) != 2:
            if not hasattr(self, 'TESTING'):
                raise Exception('MySQL replica configuration not found, aborting!')
        else:
            self.SQLALCHEMY_BINDS = bind_object
