import os
from functools import wraps

import sh

mkdir = sh.mkdir.bake('-p')
cd = sh.cd
git = sh.git

P = os.path.join

# DECORATORS
def destructive(fn):
    """functions decorated with `@destructive` are prevented from running
    in safe mode."""
    @wraps(fn)
    def _destructive(*args, **kwargs):
        self = args[0]
        if self.safe_mode:
            raise AttributeError('Cannot run destructive function %s in safe mode.' % fn.__name__)
        else:
            return fn(*args, **kwargs)
    return _destructive

def useworkdir(fn):
    """Decorator for functions that need to write to a working directory.
    Ensures before the function is run that the workdir exists."""
    @wraps(fn)
    def _useworkdir(*args, **kwargs):
        self = args[0]
        # TODO: check object has workdir attribute.
        if os.path.isdir(self.workdir):
            pass
            #self.log.warning('Working directory for exp %r already exists' % self.name)
        else:
            self.log.debug('Making directory %r' % self.workdir)
            mkdir(self.workdir)
        return fn(*args, **kwargs)
    return _useworkdir

def url_to_folder(url):
        """Convert a url to a valid folder name."""
        for sym in ('/:@'):
            url = url.replace(sym, '-')
        return url
