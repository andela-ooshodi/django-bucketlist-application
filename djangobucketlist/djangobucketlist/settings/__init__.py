import os
if not os.getenv('TRAVIS'):
    from development import *
