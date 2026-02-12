"""<internal>"""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
  '<imports>'

  from ._textstream_core import (
    TextstreamInterface,
    TextstreamBase,
    TextstreamType,
  )

# ***************************************************************************************

class TextstreamMemory (__.TextstreamBase, __.TextstreamInterface):
  """Textstream using memory streaming."""

  # :: CONSTRUCTOR :: #

  def __init__(self,
    str_data: str,
    convert_line_endings: bool,
  ) -> None:
    """
    Parameters
    ----------
    str_data : str
      String data to load directly.
    convert_line_endings : bool
      Convert line-endings from Windows style to UNIX style.
    """
    super().__init__(__.TextstreamType.MEMORY)

    # Convert all line-endings to POSIX style ('\n').
    if (convert_line_endings):
      str_data = str_data.replace("\r\n", "\n")

    self._buffer = str_data
    self._buffer_size = len(str_data)

    return

  def __del__(self):
    self.close()
    return

  # :: INTERFACE METHODS :: #

  def close(self) -> None:
    self._buffer = ""
    self._buffer_pos  = 0
    self._buffer_size = 0
    return

  def update(self, n: int) -> None:
    self._update_position(n)
    # Set EOF if end is reached.
    if (self._buffer_pos >= self._buffer_size):
      self._is_eof = True
    return
