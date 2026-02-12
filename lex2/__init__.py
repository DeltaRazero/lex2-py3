"""<library> lex2

lex2 is a library intended for lexical analysis (also called tokenization). String
analysis is performed using regular expressions (regex), as specified in user-defined
rules. Mechanisms, such as a dynamic ruleset-stack, provide flexibility to some degree
at runtime.
"""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

__version__ = "1.3.0"

# ***************************************************************************************

from . import (
  excs,
  textio,
  util,
)

from ._rule  import Rule, RuleGroup, Ruleset
from ._token import Token
from . import predefs

from ._opts import LexerOptions

from ._lexer_interface   import LexerInterface
from ._matcher_interface import MatcherInterface

from . import lexer
from . import matcher
from ._make_lexer import (
  DEFAULT_LEXER,
  DEFAULT_MATCHER,
  make_lexer,
)
