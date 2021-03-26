"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from . import lexer  as _lexer
from . import textio as _textio

from ._intf_lexer import ILexer as _ILexer

from ._rule  import ruleset_t as _ruleset_t
from ._flags import HFlags    as _HFlags

# ***************************************************************************************

def MakeLexer(ruleset: _ruleset_t=[],
              handleFlags: _HFlags=_HFlags(),
) -> _ILexer:
    """Creates an instance of the library's current default lexer implementation.

    Parameters
    ----------
    ruleset : ruleset_t, optional
        Initial ruleset.
        By default ``[]``
    handleFlags : HFlags, optional
        Initial handleFlags struct.
        By default ``HFlags()``
    textstream : ITextstream, optional
        Specify a specific ITextstream implementation.
        By default ``Textstream()``

    Returns
    -------
    ILexer
    """
    DEFAULT_IMPLEMENTATION_CLASS = _lexer.re_python.Re_Lexer

    lexer: _ILexer = DEFAULT_IMPLEMENTATION_CLASS(
        ruleset=ruleset,
        handleFlags=handleFlags,
    )
    return lexer
