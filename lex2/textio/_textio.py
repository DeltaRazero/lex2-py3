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
  import pathlib as pl

  from ._textstream_core import (
    TextstreamInterface,
  )

  from ._textstream_disk   import TextstreamDisk
  from ._textstream_memory import TextstreamMemory

# ******************************************************************************

DEFAULT_BUFFER_SIZE = 512

# ******************************************************************************

class TextIOInterface (__.abc.ABC):
  """Interface to a class implementing TextIO functionality.
  """

  # :: INTERFACE METHODS :: #

  @__.abc.abstractmethod
  def open(self,
    fp: str | __.pl.Path,
    buffer_size: int=DEFAULT_BUFFER_SIZE,
    encoding: str="UTF-8",
    convert_line_endings: bool=True
  ) -> None:
    """Opens a textfile.

    Parameters
    ----------
    fp : str | Path
      Path to a file. Opens in string mode.
    buffer_size : int, optional
      Size of the buffer in thousand characters. A value of zero (0) allocates
      the whole file into memory.
      In order to capture a token, its length must be smaller or equal to half
      the buffer size.
      Buffer size will be floored to the nearest even number.
    encoding : str, optional
      Text encoding of the file.
    convert_line_endings : bool, optional
      Convert line endings from Windows style to UNIX style.
    """
    ...

  @__.abc.abstractmethod
  def load(self, str_data: str, convert_line_endings: bool=False) -> None:
    """Loads string data directly.

    Parameters
    ----------
    str_data : str
      String data to directly load.
    convert_line_endings : bool, optional
      Convert line endings from Windows style to UNIX style.
    """
    ...

  @__.abc.abstractmethod
  def close(self) -> None:
    """Closes and cleans up textstream resources.
    """
    ...

# ******************************************************************************

class TextIO (TextIOInterface, __.abc.ABC):
  """Abstract base class providing TextIO functionality.
  """

  __slots__ = ('_ts')

  # :: PROTECTED ATTRIBUTES :: #

  _ts : __.TextstreamInterface | None

  # :: CONSTRUCTOR & DESTRUCTOR :: #

  @__.abc.abstractmethod
  def __init__(self) -> None:
    self._ts = None
    return

  def __del__(self) -> None:
    self.close()
    return

  # :: INTERFACE METHODS :: #

  def open(self,
    fp: str | __.pl.Path,
    buffer_size: int=DEFAULT_BUFFER_SIZE,
    encoding: str="UTF-8",
    convert_line_endings: bool=True,
  ) -> None:

    # Recall method in case a string filepath was passed.
    if (isinstance(fp, str)):
      return self.open(
        fp=__.pl.Path(fp),
        buffer_size=buffer_size,
        encoding="UTF-8",
        convert_line_endings=convert_line_endings,
      )

    self.close()

    if (not fp.is_file()):
      raise FileNotFoundError(f'Not an existing file or is a directory: "{str(fp)}"')

    # Buffer size in characters, usually mapping to single characters and thus
    # kilobytes (kB).
    buffer_size *= 1000

    if (buffer_size < 0):
      raise ValueError("buffer size cannot be a negative value")

    if (buffer_size == 0):
      with open(fp, "r", encoding=encoding) as f:
        self._ts = __.TextstreamMemory(
        str_data=f.read(),
          convert_line_endings=convert_line_endings,
        )
    else:
      self._ts = __.TextstreamDisk(
        fp=fp,
        buffer_size=buffer_size,
        encoding=encoding,
        convert_line_endings=convert_line_endings,
      )

    return

  def load(self,
    str_data: str,
    convert_line_endings: bool=False,
  ) -> None:

    self.close()
    self._ts = __.TextstreamMemory(
      str_data=str_data,
      convert_line_endings=convert_line_endings,
    )

    return

  def close(self) -> None:
    # Only close when a textstream instance is present.
    if (not self._ts):
      return

    self._ts.close()
    del self._ts
    self._ts = None

    return
