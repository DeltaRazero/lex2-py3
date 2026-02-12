"""<internal>"""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ******************************************************************************

# Struct.
class TextPosition:
  """Struct describing the position in a textstream."""

  __slots__ = ('pos', 'col', 'ln')

  # :: PUBLIC ATTRIBUTES :: #

  pos : int
  """
  Absolute position in a textstream. Counting starts from 0.
  Multi-byte characters are counted as one position.
  """
  col : int
  """Column of the textstream position. Counting starts from 0."""
  ln  : int
  """Line of the textstream position. Counting starts from 0."""

  # :: CONSTRUCTOR :: #

  def __init__(self, pos: int=0, col: int=0, ln: int=0) -> None:
    """
    Parameters
    ----------
    pos : int, optional
      Absolute position in a textstream. Counting starts from 0.
      Multi-byte characters are counted as one position.
    col : int, optional
      Column of the textstream position. Counting starts from 0.
    ln : int, optional
      Line of the textstream position. Counting starts from 0.
    """
    self.pos = pos
    self.col = col
    self.ln  = ln
    return
