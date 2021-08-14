"""<library> lex2

"lex2" is a library to perform lexical analysis (often called tokenization), using
regular expressions (regex).
"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

__version__ = "0.9.3"

# ***************************************************************************************

from . import (
    excs,
    misc,
    opts,
    textio,
)

from ._token import *
from ._rule  import *
from . import predefs

from ._intf_lexer   import *
from ._intf_matcher import *

from . import lexer
from ._make_lexer import *
