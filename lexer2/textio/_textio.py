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

from ._textposition    import TextPosition as _TextPosition
from ._intf_textstream import ITextstream  as _ITextstream

from ._textstream_disk   import Textstream_Disk   as _Textstream_Disk
from ._textstream_memory import Textstream_Memory as _Textstream_Memory

from .. import misc as _misc

# ***************************************************************************************

# DEFAULT_BUFFER_SIZE = 2**19  # 524288
DEFAULT_BUFFER_SIZE = 0

# ***************************************************************************************

# TODO: ALL docstrings in this sourcefile

class ITextIO (metaclass=_abc.ABCMeta):
    """Common interface to a TextStream object instance.
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
        fp : Union[str, Path]
            String or Path object of a filepath.
        encoding : str, optional
            Encoding of textfile. By default "UTF-8".
        """
        pass


    @_abc.abstractmethod
    def Load(self, strData: str) -> None:
        """Directly loads string data into the textstream object.

        Parameters
        ----------
        strData : str
            String data. Note that encoding depends on the system-wide encoding.
        convertLineEndings : bool, optional
            Convert line-endings from Windows style to UNIX style. By default 'True'.
        """
        pass


    @_abc.abstractmethod
    def Close(self) -> None:
        """Closes and deletes the textstream.
        """
        pass

# ***************************************************************************************

class TextIO (ITextIO):
    """TODO:"""

  # --- PROTECTED FIELDS --- #

    # _ts : _misc.ptr_t[_ITextstream]
    _ts : _ITextstream


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self) -> None:
        """TODO:"""

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

        if (bufferSize < 1):

            data: str
            with open(fp, "r", encoding=encoding) as f:
                data = f.read()

            self._ts = _Textstream_Memory(
                strData=data,
                convertLineEndings=convertLineEndings,
            )

        else:

            # Enforce minimum
            if (bufferSize < 128): bufferSize = 128

            self._ts = _Textstream_Disk(
                fp=fp,
                bufferSize=bufferSize,
                encoding=encoding,
                convertLineEndings=convertLineEndings,
            )

            # raise NotImplementedError("Buffered textstream")

        return


    def Load(self,
             strData: str,
             convertLineEndings: bool=True
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
