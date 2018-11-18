import os
import gettext

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

lang = gettext.translation('base', localedir=os.path.join(ROOT_DIR, 'locales'))
lang.install()
_ = lang.gettext
