"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from . import lexer as _lexer
from . import file  as _file

from ._interface_lexer import ILexer as _ILexer

from ._rule  import Ruleset_t as _Ruleset_t
from ._flags import HFlags    as _HFlags

DEFAULT_VENDOR = _lexer.re_python.Re_Lexer.VENDOR_ID

# ***************************************************************************************

def MakeLexer(vendorId: str=DEFAULT_VENDOR,
              ruleset: _Ruleset_t=[],
              handleFlags: _HFlags=_HFlags(),
              textstream: _file.ITextstream=_file.Textstream()
) -> _ILexer:
    """Creates an ILexer-compatible lexer implementation, specified by vendor ID.

    Parameters
    ----------
    vendorId : str, optional
        Lexer implementation identifier string (a.k.a. 'vendor ID').
        By default "RE_PYTHON_DEFAULT"
    ruleset : Ruleset_t, optional
        Initial ruleset.
        By default []
    handleFlags : HFlags, optional
        Initial handleFlags struct.
        By default HFlags()
    textstream : ITextstream, optional
        Specify a specific ITextstream implementation.
        By default Textstream()

    Returns
    -------
    ILexer
    """
    lexer: _ILexer
    # Select implementation by vendor ID
    if(vendorId == DEFAULT_VENDOR):
        lexer = _lexer.re_python.Re_Lexer(
            ruleset=ruleset, handleFlags=handleFlags, textstream=textstream
        )
    # In case of an unknown vendor ID, return the default implementation
    else:
        lexer = MakeLexer(
            ruleset=ruleset, handleFlags=handleFlags, textstream=textstream
        )

    return lexer
