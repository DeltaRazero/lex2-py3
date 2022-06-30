"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import abc
    import pathlib as pl
    import typing  as t

    from ._textstream_core import (
        ITextstream,
    )

    from ._textstream_disk   import TextstreamDisk
    from ._textstream_memory import TextstreamMemory

# ***************************************************************************************

DEFAULT_BUFFER_SIZE = 512

# ***************************************************************************************

class ITextIO (__.abc.ABC):
    """Interface to a class implementing TextIO functionality.
    """

    # :: INTERFACE METHODS :: #

    @__.abc.abstractmethod
    def open(self,
             fp: __.t.Union[str, __.pl.Path],
             buffer_size: int=DEFAULT_BUFFER_SIZE,
             encoding: str="UTF-8",
             convert_line_endings: bool=True
    ) -> None:
        """Opens a textfile.

        Parameters
        ----------
        fp : str | Path
            String or Path object of a text file to open.
        buffer_size : int, optional
            Size of the buffer in kilobytes (kB). A size of zero (0) allocates the whole
            file into memory. In order to completely capture a token, its length must be
            smaller or equal to half the buffer size value.
            Note that the buffer size will be floored to the nearest even number.
        encoding : str, optional
            Encoding of the text file.
        convert_line_endings : bool, optional
            Convert line-endings from Windows style to UNIX style.
        """
        ...


    @__.abc.abstractmethod
    def load(self, str_data: str, convert_line_endings: bool=False) -> None:
        """Load string data directly.

        Parameters
        ----------
        str_data : str
            String data to directly load. Note that encoding depends on the system-wide
            encoding.
        convert_line_endings : bool, optional
            Convert line-endings from Windows style to UNIX style.
        """
        ...


    @__.abc.abstractmethod
    def close(self) -> None:
        """Closes and deletes textstream resources.
        """
        ...

# ***************************************************************************************

class TextIO (ITextIO, __.abc.ABC):
    """Abstract base class implementing ITextIO, providing TextIO functionality.
    """

    __slots__ = ('_ts')

    # :: PROTECTED ATTRIBUTES :: #

    _ts : __.ITextstream


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    @__.abc.abstractmethod
    def __init__(self) -> None:
        """TextIO object instance initializer.
        """
        self._ts = None
        return


    def __del__(self) -> None:
        self.close()
        return


    # :: INTERFACE METHODS :: #

    def open(self,
             fp: __.t.Union[str, __.pl.Path],
             buffer_size: int=DEFAULT_BUFFER_SIZE,
             encoding: str="UTF-8",
             convert_line_endings: bool=True,
    ) -> None:

        # Re-call method in case of string filepath
        if (isinstance(fp, str)):
            self.open(
                fp=__.pl.Path(fp),
                buffer_size=buffer_size,
                encoding=encoding,
                convert_line_endings=convert_line_endings,
            )
            return

        self.close()

        # Check if path exists and is file
        if (not fp.is_file()):
            raise FileNotFoundError(f'Not an existing file or is a directory: "{str(fp)}"')

        # Buffersize is in units of kilobytes (kB)
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
             convert_line_endings: bool=False
    ) -> None:

        self.close()
        self._ts = __.TextstreamMemory(
            str_data=str_data,
            convert_line_endings=convert_line_endings,
        )

        return


    def close(self) -> None:

        # Only close/cleanup if a textream is already instanced
        if (self._ts):
            self._ts.close()
            del self._ts
            self._ts = None

        return
