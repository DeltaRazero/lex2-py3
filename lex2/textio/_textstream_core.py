"""<internal>"""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ******************************************************************************

class __:
  '<imports>'

  import abc
  import enum

  from ._textposition import TextPosition

# ******************************************************************************

class TextstreamType (__.enum.Enum):
  """Textstream type.

  Values
  ------
  MEMORY
    When a textstream has all data in memory.
  DISK
    When a textstream has data partially available in memory at one time, and
    has to dynamically read and swap data in chunks from disk.
  """
  MEMORY = 0
  DISK   = 1

# ******************************************************************************

class TextstreamInterface (__.abc.ABC):
  """Common interface to a Textstream object instance.
  """

  # :: INTERFACE METHODS :: #

  @__.abc.abstractmethod
  def close(self) -> None:
    """Closes and deletes textstream resources.
    """
    ...

  @__.abc.abstractmethod
  def update(self, n: int) -> None:
    """Updates the textstream's buffer.

    Parameters
    ----------
    n : int
      Amount of characters to read and insert. Must be a positive number.
    """
    ...

  @__.abc.abstractmethod
  def is_eof(self) -> bool:
    """Evaluates whether the textstream has reached the end of data.
    """
    ...

  # :: INTERFACE GETTERS :: #

  @__.abc.abstractmethod
  def get_textstream_type(self) -> TextstreamType:
    """Gets textstream type.
    """
    ...

  @__.abc.abstractmethod
  def get_position(self) -> __.TextPosition:
    """Gets the TextPosition object instance.
    """
    ...

  @__.abc.abstractmethod
  def get_buffer(self) -> str:
    """Gets the currently buffered string value.
    """
    ...

  @__.abc.abstractmethod
  def get_buffer_size(self) -> int:
      """Gets the length of the currently buffered string (in characters).
      """
      ...

  @__.abc.abstractmethod
  def get_buffer_position(self) -> int:
    """Gets the index of the current position in the buffered string.
    """
    ...

# ***************************************************************************************

class TextstreamBase (TextstreamInterface, __.abc.ABC): # pylint: disable=abstract-method
  """Abstract base class of an ITextstream implementation.
  """

  __slots__ = (
    '_tp', '_is_eof',
    '_buffer', '_buffer_size', '_buffer_pos',
    '_textstream_type',
  )

  # :: PRIVATE ATTRIBUTES :: #

  _textstream_type : TextstreamType
  _tp : __.TextPosition
  _is_eof : bool

  # The string buffer may be either unicode-aware or pure ASCII, or a multi-byte
  # encoded (e.g. UTF-8).
  _buffer : str
  _buffer_size : int
  _buffer_pos  : int

  # :: CONSTRUCTOR & DESTRUCTOR :: #

  @__.abc.abstractmethod
  def __init__(self, textstream_type: TextstreamType) -> None:

    self._textstream_type = textstream_type

    self._tp = __.TextPosition(
      pos=0,
      ln =0,
      col=0,
    )

    self._is_eof = False

    self._buffer = ""
    self._buffer_size = 0
    self._buffer_pos  = 0

    return

  # :: INTERFACE METHODS :: #

  def is_eof(self) -> bool:
    return self._is_eof


  # :: INTERFACE GETTERS :: #

  def get_textstream_type(self) -> TextstreamType:
    return self._textstream_type

  def get_position(self) -> __.TextPosition:
    return self._tp

  def get_buffer(self) -> str:
    return self._buffer

  def get_buffer_size(self) -> int:
    return self._buffer_size

  def get_buffer_position(self) -> int:
    return self._buffer_pos

  # :: PROTECTED METHODS :: #

  # @profile
  def _update_position(self, n: int) -> None:
    """Updates text position."""

    # Cache variable for faster lookup times in Python.; not necessary for compiled
    # languages.
    _tp = self._tp

    old_pos = self._buffer_pos
    self._buffer_pos += n

    chars = self._buffer[old_pos : self._buffer_pos]
    # Amount of code-points.
    strlen = len(chars)
    # Amount bytes.
    sizeof = strlen

    _tp.pos += strlen

    amount_newlines = chars.count('\n')
    if (amount_newlines):
      _tp.col = 0
      _tp.ln += amount_newlines
      for i in range(sizeof-1, -1, -1):
        if (chars[i] != '\n'):
          continue
        # -- When using multi-byte encodings:
        # chars = chars[i+1:]
        # strlen = sizeof(chars)
        # -- When using Unicode-aware or ASCII-only strings:
        strlen -= i -1
        break

    _tp.col += strlen

    return
