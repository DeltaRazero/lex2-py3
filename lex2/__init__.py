"""<library> lex2

"lex2" is a library to perform lexical analysis (often called tokenization), using
regular expressions (regex).
"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

__version__ = "0.9.3-beta"

# ***************************************************************************************

from . import excs
from . import misc
from . import opts
from . import textio

from ._token import Token
from ._rule  import Rule, ruleset_t
from . import predefs

from ._intf_matcher import IMatcher
from ._intf_lexer   import ILexer

from . import lexer
from ._make_lexer import MakeLexer
