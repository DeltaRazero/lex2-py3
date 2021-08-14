"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    from . import lexer

    from ._intf_lexer import ILexer
    from ._rule       import ruleset_t
    from .opts        import LexerOptions

# ***************************************************************************************

def MakeLexer(ruleset: _.ruleset_t=[],
              options: _.LexerOptions=_.LexerOptions(),
) -> _.ILexer:
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
    DEFAULT_IMPLEMENTATION_CLASS = _.lexer.re_python.Re_Lexer

    lexer: _.ILexer = DEFAULT_IMPLEMENTATION_CLASS(
        ruleset=ruleset,
        options=options,
    )
    return lexer
