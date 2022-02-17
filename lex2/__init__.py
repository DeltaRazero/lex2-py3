"""<library> lex2

"lex2" is a library to perform lexical analysis (often called tokenization), using
regular expressions (regex).
"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

__version__ = "0.9.4"

# ***************************************************************************************

from . import (
    excs,
    textio,
    _util,
)

from ._rule  import Rule, RuleGroup, ruleset_t
from ._token import Token
from . import predefs

from ._opts import LexerOptions

from ._itf_lexer   import ILexer
from ._itf_matcher import IMatcher

from . import lexer
from . import matcher
from ._make_lexer import (
    DEFAULT_LEXER,
    DEFAULT_MATCHER,
    MakeLexer
)
