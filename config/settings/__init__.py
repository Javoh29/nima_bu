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
    BOT_TOKEN = "7886990962:AAGDjdnyvCVrmW_Y6k4TFz1Lp_K4hvjr0RU"
    from .dev import *
else:
    BOT_TOKEN = env('BOT_TOKEN')
    from .prod import *

