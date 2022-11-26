"""<library> lex2

lex2 is a library intended for lexical analysis (also called tokenization). String
analysis is performed using regular expressions (regex), as specified in user-defined
rules. Mechanisms, such as a dynamic ruleset-stack, provide flexibility to some degree
at runtime.
"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

__version__ = "1.1.0"

# ***************************************************************************************

from . import (
    excs,
    textio,
    util,
)

from ._rule  import Rule, RuleGroup, RulesetType
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
    make_lexer,
)
