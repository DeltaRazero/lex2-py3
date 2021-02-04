"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._intf_textstream     import ITextstream         as _ITextstream
from ._textstream          import Textstream          as _Textstream
from ._textstream_buffered import BufferedTextstream  as _BufferedTextstream

# ***************************************************************************************

def MakeTextstream(chunkSize: int=512, isBuffered: bool=False) -> _ITextstream:
    """Creates an ITextstream-compatible textstream object.

    Parameters
    ----------
    chunkSize : int, optional
        Size of a single string buffer chunk (in characters). Note that this number
        will be floored to the nearest even number.
        By default 512.
    isBuffered : bool, optional
        Specifies if the textstream should be buffered (only string data from chunks are
        loaded into memory). Use this option only if working with very big files to save
        work memory if needed.
        By default False.

    Returns
    -------
    ITextstream
    """
    textstream: _ITextstream
    # Select implementation
    if (isBuffered):
        textstream = _BufferedTextstream(chunkSize)
    else:
        textstream = _Textstream(chunkSize)

    return textstream
