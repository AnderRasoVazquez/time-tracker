import sys
import pandas  # TODO without this here I get the following error:
               # from pandas.util._move import ( ValueError: module functions cannot set METH_CLASS or METH_STATIC
from application import Application

import os
import gettext
from definitions import ROOT_DIR

gettext.install('base', localedir=os.path.join(ROOT_DIR, 'locales'))

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
