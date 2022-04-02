"""Components of textstreams."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._textposition import TextPosition

from ._textstream_core   import ITextstream, BaseTextstream, TextstreamType
from ._textstream_disk   import TextstreamDisk
from ._textstream_memory import TextstreamMemory

from ._textio import (
    DEFAULT_BUFFER_SIZE,
    ITextIO,
    TextIO
)
