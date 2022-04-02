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
    import enum

    from ._textposition import TextPosition

# ***************************************************************************************

class TextstreamType (__.enum.Enum):
    """Textstream enum type.

    Values
    ------
    MEMORY
        When a textstream has all data in working memory at its disposal.
    DISK
        When a textstream only has part data available in working memory at one time, and
        has to dynamically read and swap data in chunks from disk.
    """
    MEMORY = 0
    DISK   = 1

# ***************************************************************************************

class ITextstream (metaclass=__.abc.ABCMeta):
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
            Amount of characters to read/update. Must be a positive number.
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
        """Gets textstream enum type.
        """
        ...


    @__.abc.abstractmethod
    def get_text_position(self) -> __.TextPosition:
        """Gets the TextPosition object instance.
        """
        ...


    @__.abc.abstractmethod
    def get_string_buffer(self) -> str:
        """Gets the currently buffered string value.
        """
        ...


    @__.abc.abstractmethod
    def get_string_buffer_size(self) -> int:
        """Gets the length of the currently buffered string (in characters).
        """
        ...


    @__.abc.abstractmethod
    def get_string_buffer_position(self) -> int:
        """Gets the index of the current position in the buffered string.
        """
        ...

# ***************************************************************************************

class BaseTextstream (ITextstream): # pylint: disable=abstract-method
    """Abstract base class of an ITextstream implementation.
    """

    # :: PRIVATE PROPERTIES :: #

    _textstream_type : TextstreamType

    _tp : __.TextPosition

    _is_eof : bool

    # The string buffer may either be unicode-aware/ASCII or a multibyte system-encoding
    # (such as UTF-8)
    _string_buffer : str
    _string_buffer_size : int
    _string_buffer_pos  : int


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    def __init__(self, textstream_type: TextstreamType) -> None:

        self._textstream_type = textstream_type

        self._tp = __.TextPosition(
            pos=0,
            ln =0,
            col=0,
        )

        self._is_eof = False

        self._string_buffer = ""
        self._string_buffer_size = 0
        self._string_buffer_pos  = 0

        return


    # :: INTERFACE METHODS :: #

    def is_eof(self) -> bool:
        return self._is_eof


    # :: INTERFACE GETTERS :: #

    def get_textstream_type(self) -> TextstreamType:
        return self._textstream_type


    def get_text_position(self) -> __.TextPosition:
        return self._tp


    def get_string_buffer(self) -> str:
        return self._string_buffer


    def get_string_buffer_size(self) -> int:
        return self._string_buffer_size


    def get_string_buffer_position(self) -> int:
        return self._string_buffer_pos


    # :: PROTECTED METHODS :: #

    def _update_position(self, n: int) -> None:
        """Updates text position."""

        # Cache variable for faster lookup times in Python. Not necessary for compiled languages
        _tp = self._tp

        old_pos = self._string_buffer_pos
        self._string_buffer_pos += n

        chars = self._string_buffer[ old_pos : self._string_buffer_pos ]
        strlen = len(chars) # Amount codepoints
        sizeof = strlen # Amount bytes

        _tp.pos += strlen

        lns = chars.count('\n')
        if (lns):
            _tp.col = 0
            _tp.ln += lns
            # for (int i=size-1; i>=0; i--)
            for i in range(sizeof-1, -1, -1):
                if (chars[i] == '\n'):
                # IF SYSTEM-ENCODING (UTF-8) STRINGS
                    # chars  = chars[ i+1 : ]
                    # strlen = sizeof(chars)
                    # break
                # IF UNICODE-AWARE OR ASCII-ONLY STRINGS
                    strlen = strlen - i - 1
                    break
                # ENDIF

        _tp.col += strlen

        return

        # Older slower code, not portable without unicode-aware strings
        """
        _tp = self._tp
        for char in self._string_buffer[ old_pos : self._string_buffer_pos ]:

            _tp.pos += 1
            _tp.col += 1

            if (char == '\n'):
                _tp.ln += 1
                _tp.col = 0

        return
        """
