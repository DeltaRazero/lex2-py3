"""Components of textstreams."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._textposition import TextPosition

from ._textstream_core   import ITextstream, AbstractTextstream
from ._textstream_disk   import Textstream_Disk
from ._textstream_memory import Textstream_Memory

from ._textio import (
    DEFAULT_BUFFER_SIZE,
    ITextIO,
    TextIO
)
