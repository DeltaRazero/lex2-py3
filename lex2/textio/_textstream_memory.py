"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    from ._textstream_core import (
        ITextstream,
        BaseTextstream,
        TextstreamType,
    )

# ***************************************************************************************

class TextstreamMemory (__.BaseTextstream, __.ITextstream):

    # :: CONSTRUCTOR & DESTRUCTOR :: #

    def __init__(self,
                 str_data: str,
                 convert_line_endings: bool
    ) -> None:
        """TextPosition object instance initializer.

        Parameters
        ----------
        str_data : str
            String data to directly load. Note that encoding depends on the system-wide
            encoding.
        convert_line_endings : bool
            Convert line-endings from Windows style to UNIX style.
        """
        super().__init__(__.TextstreamType.MEMORY)

        # Convert all line-endings to POSIX format ('\n')
        if (convert_line_endings):
            str_data = str_data.replace("\r\n", "\n")

        self._string_buffer = str_data
        self._string_buffer_size = len(str_data)

        return


    def __del__(self):
        self.close()
        return


    # :: INTERFACE METHODS :: #

    def close(self) -> None:
        self._string_buffer = ""
        self._string_buffer_pos  = 0
        self._string_buffer_size = 0
        return


    def update(self, n: int) -> None:
        self._update_position(n)

        # If current position Signal EOF
        if (self._string_buffer_pos >= self._string_buffer_size):
            self._is_eof = True

        return
