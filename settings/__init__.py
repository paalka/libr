from base import *

try:
        from local import *
except ImportError, e:
        raise ImportError("Couldn't load local settings")
