import os
if not os.getenv('TRAVIS') and not os.getenv('HEROKU'):
    from django_envie.workroom import convertfiletovars
    convertfiletovars()
    try:
        from development import *
    except ImportError:
        from base import *
        print "Using default database configuration"

if os.getenv('HEROKU') is not None:
    from production import *
