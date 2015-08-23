
from os.path import dirname, abspath, join

SOURCE_DIR = dirname(dirname(dirname(abspath(__file__))))
STATIC_DIR = join(SOURCE_DIR, 'static')
SETTINGS_DIR = join(SOURCE_DIR, 'settings')
TEMPLATES_DIR = join(SOURCE_DIR, 'templates')
