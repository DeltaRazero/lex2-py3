"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc     as _abc
import pathlib as _pl
import typing  as _t

from ._intf_textstream import ITextstream  as _ITextstream

from ._textstream_disk   import Textstream_Disk   as _Textstream_Disk
from ._textstream_memory import Textstream_Memory as _Textstream_Memory

# ***************************************************************************************

DEFAULT_BUFFER_SIZE = 512

# ***************************************************************************************

class ITextIO (metaclass=_abc.ABCMeta):
    """Interface to a class implementing TextIO functionality.
    """

  # --- INTERFACE METHODS --- #

    @_abc.abstractmethod
    def Open(self,
             fp: _t.Union[str, _pl.Path],
             bufferSize: int=DEFAULT_BUFFER_SIZE,
             encoding: str="UTF-8",
             convertLineEndings: bool=True
    ) -> None:
        """Opens a textfile.

        Parameters
        ----------
        fp : str | Path
            String or Path object of a text file to open.
        bufferSize : int, optional
            Size of the buffer in kilobytes (kB). A size of zero (0) allocates the whole
            file into memory.
            Keep in mind that in order to completely capture a token, it must be smaller
            or equal to the size allocated to the buffer by this argument. Note that the
            buffer size will be floored to the nearest even number.
        encoding : str, optional
            Encoding of the text file.
        convertLineEndings : bool, optional
            Convert line-endings from Windows style to UNIX style.
        """
        pass


    @_abc.abstractmethod
    def Load(self, strData: str, convertLineEndings: bool=False) -> None:
        """Load string data directly.

        Parameters
        ----------
        strData : str
            String data to directly load. Note that encoding depends on the system-wide
            encoding.
        convertLineEndings : bool, optional
            Convert line-endings from Windows style to UNIX style.
        """
        pass


    @_abc.abstractmethod
    def Close(self) -> None:
        """Closes and deletes textstream resources.
        """
        pass

# ***************************************************************************************

class TextIO (ITextIO):
    """TODO:"""

  # --- PROTECTED FIELDS --- #

    _ts : _ITextstream


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self) -> None:
        self._ts = None
        return


    def __del__(self) -> None:
        self.Close()
        return


  # --- INTERFACE METHODS --- #

    def Open(self,
             fp: _t.Union[str, _pl.Path],
             bufferSize: int=DEFAULT_BUFFER_SIZE,
             encoding: str="UTF-8",
             convertLineEndings: bool=True,
    ) -> None:

        self.Close()

        # Cast fp to pathlib.Path if a string
        if (type(fp) is str):
            fp = _pl.Path(fp)

        # Check if path exists and is file
        if (not fp.is_file()):
            raise FileNotFoundError(f'Not an existing file or is a directory: "{str(fp)}"')

        # Buffersize is in units of kilobytes (kB)
        bufferSize *= 1000

        if (bufferSize < 0):
            raise ValueError("buffer size cannot be a negative value")

        elif (bufferSize == 0):

            with open(fp, "r", encoding=encoding) as f:
                self._ts = _Textstream_Memory(
                    strData=f.read(),
                    convertLineEndings=convertLineEndings,
                )

        else:
            self._ts = _Textstream_Disk(
                fp=fp,
                bufferSize=bufferSize,
                encoding=encoding,
                convertLineEndings=convertLineEndings,
            )

        return


    def Load(self,
             strData: str,
             convertLineEndings: bool=False
    ) -> None:

        self.Close()
        self._ts = _Textstream_Memory(
            strData=strData,
            convertLineEndings=convertLineEndings,
        )

        return


    def Close(self) -> None:

        # Only close/cleanup if a textream is already instanced
        if (self._ts):
            self._ts.Close()
            del self._ts
            self._ts = None

        return
