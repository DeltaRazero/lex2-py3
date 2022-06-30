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
        RulesetType,
        LexerOptions,
    )

# ***************************************************************************************

DEFAULT_MATCHER = __.matcher.ReMatcher
DEFAULT_LEXER   = __.lexer.GenericLexer

# ***************************************************************************************

# template
def make_lexer(MATCHER_T: __.t.Type[__.matcher.BaseMatcher]=DEFAULT_MATCHER,
               LEXER_T  : __.t.Type[  __.lexer.BaseLexer  ]=DEFAULT_LEXER,
):
    """Factory function for creating a lexer instance.

    If no values are provided for the template parameters, the implementations used for
    the matcher and lexer will default to the library constants ``DEFAULT_MATCHER`` and
    ``DEFAULT_LEXER`` respectively.

    Template Parameters
    -------------------
    MATCHER_T : Type[BaseMatcher], optional
        Template class type that implements the ``BaseMatcher`` base class.
        By default ``DEFAULT_MATCHER``
    LEXER_T : Type[BaseLexer], optional
        Template class type that implements the ``BaseLexer`` base class.
        By default ``DEFAULT_LEXER``

    Parameters
    ----------
    ruleset : RulesetType, optional
        Initial ruleset.
        By default ``[]``
    options : LexerOptions, optional
        Struct specifying processing options of the lexer.
        By default ``LexerOptions()``

    Returns
    -------
    ILexer
    """

    # This would be the actual function body in C++/C#/Rust/etc.
    def _templated_make_lexer(ruleset: __.RulesetType=None,
                              options: __.LexerOptions=__.LexerOptions(),
        ) -> __.ILexer:
        """Factory function for creating a lexer instance (templated).

        Parameters
        ----------
        ruleset : RulesetType, optional
            Initial ruleset. By default []
        options : LexerOptions, optional
            Struct specifying processing options of the lexer. By default LexerOptions()

        Returns
        -------
        ILexer
        """

        UID: str = MATCHER_T.__name__

        class Matcher (MATCHER_T):
            def __init__(self, uid: str) -> None:
                super().__init__()
                self._uid = uid
                return

        class Lexer (LEXER_T):
            def __init__(self):
                super().__init__()
                self._uid = UID
                return

            # :: PROTECTED METHODS :: #

            def _compile_rule(self, rule: __.Rule) -> __.IMatcher:
                matcher = Matcher(self._uid)
                matcher.compile_pattern(rule.regex)
                return matcher

        # Default value is empty array
        ruleset = ruleset or []

        lexer = Lexer()
        lexer.set_options(options)
        lexer.push_ruleset(ruleset)

        return lexer

    # Workaround for using autodoc with nested functions
    # see: https://stackoverflow.com/a/12039980
    make_lexer.templated_make_lexer = _templated_make_lexer

    return _templated_make_lexer
