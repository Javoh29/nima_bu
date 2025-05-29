import os
import environ
from .base import BASE_DIR

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')
BOT_TOKEN = env('BOT_TOKEN')

if DEBUG:
    from .dev import *
else:
    from .prod import *

