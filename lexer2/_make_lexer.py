"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from . import lexer  as _lexer

from ._intf_lexer import ILexer as _ILexer

from .opts  import LexerOptions as _LexerOptions
from ._rule import ruleset_t    as _ruleset_t

# ***************************************************************************************

def MakeLexer(ruleset: _ruleset_t=[],
              options: _LexerOptions=_LexerOptions(),
) -> _ILexer:
    """Creates an instance of the library's default lexer implementation.

    Parameters
    ----------
    ruleset : ruleset_t, optional
        Initial ruleset.
        By default []
    options : LexerOptions, optional
        Struct specifying processing options of the lexer.
        By default LexerOptions()

    Returns
    -------
    ILexer
    """
    DEFAULT_IMPLEMENTATION_CLASS = _lexer.re_python.Re_Lexer

    lexer: _ILexer = DEFAULT_IMPLEMENTATION_CLASS(
        ruleset=ruleset,
        options=options,
    )
    return lexer
