"""Components of a lexer implementation with Python's builtin `re` module."""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ******************************************************************************

class __:
  '<imports>'

  import typing as t
  import re

  from . import (
    MatcherBase,
  )

  from lex2 import (
    textio,
    Token,
  )

# ******************************************************************************

class ReMatcher (__.MatcherBase):
  """Implementation of IMatcher using Python's builtin `re` module.
  """

  __slots__ = ('_pattern')

  # :: PRIVATE ATTRIBUTES :: #

  # t.Pattern is an instance of a compiled regex pattern of Python's builtin 're' module
  _pattern : __.t.Pattern[str]

  # :: CONSTRUCTOR :: #

  def __init__(self) -> None:
    return

  # :: PUBLIC METHODS :: #

  @staticmethod
  def uid() -> str:
    return ReMatcher.__name__

  def compile_pattern(self, regex: str) -> None:
    self._pattern = __.re.compile(regex)
    return

  def match(self, ts: __.textio.TextstreamInterface, token: __.Token) -> bool:
    regex_match = self._pattern.match(
      # ts.get_buffer(),          # Data input
      # ts.get_buffer_position(), # Read STARTING AT position
      # ts.get_buffer_size(),     # Read UNTIL position
      # NOTE: Direct access is done to improve performance. Using the interface
      # methods is encouraged in a compiled language.
      ts._buffer,      # Data input
      ts._buffer_pos,  # Read STARTING AT position
      ts._buffer_size, # Read UNTIL position
    )

    if (not regex_match):
      return False

    token.data = regex_match.group()
    token.groups = regex_match.groups()
    return True
