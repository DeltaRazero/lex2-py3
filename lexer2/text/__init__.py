"""Components of textfile- and position reading."""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._textposition import TextPosition

from ._intf_textstream     import ITextstream
from ._textstream          import Textstream
from ._textstream_buffered import BufferedTextstream

from ._make_textstream import MakeTextstream
