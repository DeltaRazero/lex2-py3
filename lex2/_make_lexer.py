"""<internal>"""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ******************************************************************************

class __:
  '<imports>'

  import typing as t

  from lex2 import (
    lexer,
    matcher,
  )

  from lex2 import (
    LexerInterface,
    MatcherInterface,
    Rule,
    Ruleset,
    LexerOptions,
  )

# ******************************************************************************

DEFAULT_MATCHER = __.matcher.ReMatcher
DEFAULT_LEXER   = __.lexer.StdLexer

# ******************************************************************************

def Lexer(
  MATCHER_T: __.t.Type[__.matcher.MatcherBase],
  LEXER_T  : __.t.Type[__.lexer.LexerBase],
):
  class LexerTemplated (LEXER_T):
    def __init__(self):
      super().__init__()
      self._uid = MATCHER_T.uid()
      return

    # :: PROTECTED METHODS :: #

    def _compile_rule(self, rule: __.Rule) -> __.MatcherInterface:
      matcher = MATCHER_T()
      matcher.compile_pattern(rule.regex)
      return matcher

  return LexerTemplated

# ******************************************************************************

# Template function.
def make_lexer(
  MATCHER_T: __.t.Type[__.matcher.MatcherBase]=DEFAULT_MATCHER,
  LEXER_T  : __.t.Type[__.lexer.LexerBase]=DEFAULT_LEXER,
):
  """Factory function for creating a lexer instance.

  If no values are provided for the template parameters, the implementations
  used for the matcher and lexer will default to the library constants
  ``DEFAULT_MATCHER`` and ``DEFAULT_LEXER`` respectively.

  Template Parameters
  -------------------
  MATCHER_T : Type[MatcherBase], optional
    Template class type that implements the ``MatcherBase`` base class.
    By default ``DEFAULT_MATCHER``
  LEXER_T : Type[LexerBase], optional
    Template class type that implements the ``LexerBase`` base class.
    By default ``DEFAULT_LEXER``

  Parameters
  ----------
  ruleset : Ruleset, optional
    Initial ruleset.
    By default ``[]``
  options : LexerOptions, optional
    Struct specifying processing options of the lexer.
    By default ``LexerOptions()``

  Returns
  -------
  LexerInterface
  """

  # The actual function in C++/Java/etc.
  def _templated_make_lexer(
    ruleset: __.t.Optional[__.Ruleset]=None,
    options: __.LexerOptions=__.LexerOptions(),
  ) -> __.LexerInterface:
    """Factory function for creating a lexer instance (templated).

    Parameters
    ----------
    ruleset : Ruleset, optional
      Initial ruleset. By default []
    options : LexerOptions, optional
      Struct specifying processing options of the lexer. By default LexerOptions()

    Returns
    -------
    LexerInterface
    """

    lexer = Lexer(MATCHER_T, LEXER_T)()
    lexer.set_options(options)
    lexer.push_ruleset(ruleset or [])

    return lexer

  # Workaround for using autodoc with nested functions
  # see: https://stackoverflow.com/a/12039980
  make_lexer.templated_make_lexer = _templated_make_lexer

  return _templated_make_lexer
