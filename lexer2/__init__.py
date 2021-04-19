"""<library> lexer2

lexer2 is a library for lexical analysis (often called tokenization). lexer2 is rule-based
in conjunction with regular expressions (regex) and allows for context-based tokenization
through the (optional) use of a ruleset stack.
"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

__version__ = "0.9.2"

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
