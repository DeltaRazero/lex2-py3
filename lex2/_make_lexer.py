"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import typing as t

    from lex2 import (
        lexer,
        matcher,
    )

    from lex2 import (
        ILexer,
        IMatcher,
        Rule,
        ruleset_t,
        LexerOptions,
    )

# ***************************************************************************************

DEFAULT_MATCHER = __.matcher.Re_Matcher
DEFAULT_LEXER   = __.lexer.GenericLexer

# TEMPLATE
def MakeLexer(MATCHER_T: __.t.Type[__.matcher.BaseMatcher]=DEFAULT_MATCHER,
              LEXER_T  : __.t.Type[  __.lexer.BaseLexer  ]=DEFAULT_LEXER,
):
    """Factory function for creating a lexer instance.

    If no values are provided for the template parameters, the implementations used for
    the matcher and lexer will default to the library constants `DEFAULT_MATCHER` and
    `DEFAULT_LEXER` respectively.

    Template Parameters
    -------------------
    MATCHER_T : Type[BaseMatcher], optional
        ...

    LEXER_T : Type[BaseLexer], optional
        ...
        Template class type implementing the ILexer interface. By default DEFAULT_LEXER_IMPLEMENTATION

    Parameters
    ----------
    ruleset : ruleset_t, optional
        Initial ruleset. By default []
    options : LexerOptions, optional
        Struct specifying processing options of the lexer. By default LexerOptions()

    Returns
    -------
    ILexer
    """

    class Matcher (MATCHER_T):
        def __init__(self, implementationId: str) -> None:
            self._implementationId = implementationId
            return

    class Lexer (LEXER_T):
        def __init__(self):
            """Re_Lexer object instance initializer."""
            super().__init__()
            self._implementationId = MATCHER_T.__name__
            return
      # --- PROTECTED METHODS --- #
        def _CompileRule(self, rule: __.Rule) -> __.IMatcher:
            matcher = Matcher(self._implementationId)
            matcher.CompilePattern(rule.regexPattern)
            return matcher

    # NOTE: This would be the actual function body in C++
    def _MakeLexer(ruleset: __.ruleset_t=[],
                   options: __.LexerOptions=__.LexerOptions(),
        ) -> __.ILexer:
        """Factory function for creating a lexer instance (templated).

        Parameters
        ----------
        ruleset : ruleset_t, optional
            Initial ruleset. By default []
        options : LexerOptions, optional
            Struct specifying processing options of the lexer. By default LexerOptions()

        Returns
        -------
        ILexer
        """
        lexer = Lexer()
        lexer.SetOptions(options)
        lexer.PushRuleset(ruleset)
        return lexer

    return _MakeLexer
