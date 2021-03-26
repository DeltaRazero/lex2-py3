"""Components of textfile- and position reading."""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._textposition import TextPosition

from ._intf_textstream import ITextstream
from ._textio          import ITextIO, TextIO, DEFAULT_BUFFER_SIZE
