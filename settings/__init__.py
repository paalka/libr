from .base import *

try:
        from .local import *
except ImportError:
        raise ImportError("Couldn't load local settings")
