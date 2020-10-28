"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import typing as _t

from ._interface import ITextstream  as _ITextstream
from ._interface import TextPosition as _TextPosition

# ***************************************************************************************

class Textstream (_ITextstream):

  # --- FIELDS --- #

    _textPos  : _TextPosition
    _newlines : _t.List[_TextPosition]

    _encoding   : str
    _convertEol : bool

    _strBuffer : str
    _strBufferLength : int
    # _strBufferPosition : int


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self) -> None:
        self._strBuffer = ""
        self._textPos = _TextPosition()
        return


    def __del__(self):
        self.Close()
        return


  # --- INTERFACE METHODS --- #

    def Open(self, fp: str, encoding: str="UTF-8", convertLineEndings: bool=True) -> None:

        self._encoding   = encoding
        self._convertEol = convertLineEndings

        # Read file in given encoding
        self.Close()
        with open(fp, "rb") as f:
            data = f.read()
            self._strBuffer = data.decode(self._encoding, "ignore")

        self._PrepareVariables()

        return


    def Load(self, strData: str,  convertLineEndings: bool=True) -> None:

        self._convertEol = convertLineEndings

        self.Close()
        self._strBuffer = strData

        self._PrepareVariables()

        return


    def Close(self) -> None:

        if (self._strBuffer):
            del self._strBuffer
        self._strBuffer = ""
        _TextPosition.Reset(self._textPos)

        return


    # In characters, not in byte mode
    def Seek(self, offset: int, whence: int=0) -> None:

        new_pos : int
        # 0 Absolute
        # 1 Relative
        # 2 Absolute (reversed)
        if   (whence == 0): new_pos = offset
        elif (whence == 1): new_pos = self._textPos.pos + offset
        elif (whence == 2): new_pos = (self._strBufferLength-1) - offset
        else:
            raise Exception()

        if (new_pos < 0  or  new_pos > self._strBufferLength):
            raise IndexError()

        self._textPos.pos = new_pos

        # If seeking past last character
        if (not new_pos < self._strBufferLength):
            last_nl = self._newlines[-1]
            self._textPos.ln  = last_nl.ln+1
            self._textPos.col = new_pos - last_nl.pos + 1
            # NOTE: self._pos.pos already set
            return

        # Track line- and column number for chosen new position
        # TODO: Maybe add a check/seek block when the new_pos is too far away (from the start/end)

        self._CalculateTextPosition(new_pos)

        return


    def Tell(self) -> _TextPosition:
        return self._textPos


    def IsEOF(self) -> bool:
        return not (self._textPos.pos < self._strBufferLength)


    def GetBuffer(self) -> str:
        return self._strBuffer


    def GetBufferLength(self) -> int:
        return self._strBufferLength


    def GetBufferPosition(self) -> int:
        return self._textPos.pos
        # return self._strBufferPosition


  # --- PRIVATE METHODS --- #

    def _PrepareVariables(self) -> None:

        # Prepare string buffer variables
        if (self._convertEol):  # Convert all line-endings to POSIX format ('\n')
            self._strBuffer = self._strBuffer.replace("\r\n", "\n")
        self._strBufferLength = self._strBuffer.__len__()

        # Find all NEWLINE locations (speeds up seeking)
        self._newlines = [
            _TextPosition()  # Dummy NEWLINE for line 0
        ]
        ln,col,pos = 0,0,0
        for pos, char in enumerate(self._strBuffer):
            # Save position of NEWLINE when encountered
            if (char == '\n'):
                ln += 1
                self._newlines.append(_TextPosition(pos, col, ln))
                col=0
                continue
            col+=1
        # Dummy final NEWLINE for overflow search
        self._newlines.append(_TextPosition(
            ln =ln +1,
            col=col+1,
            pos=pos+1
        ))

        return


    def _CalculateTextPosition(self, newPos: int) -> None:

        # Start from the begin of current line
        ln = self._textPos.ln
        line = self._newlines[ln]

        # Decrease lines to go backwards
        if (newPos < line.pos):
            while(1):
                ln -= 1
                line = self._newlines[ln]
                # Seek behind NEWLINE
                if (newPos > line.pos):
                    self._textPos.col = newPos - line.pos - 1
                    break
                # Seek at the NEWLINE itself
                elif (newPos == line.pos):
                    self._textPos.col = line.col
                    if (ln != 0): ln -= 1
                    break
            self._textPos.ln = ln

        # Increase lines to go forwards (or stay on same line)
        else:
            while(1):
                ln += 1
                line = self._newlines[ln]
                # Seek in front of NEWLINE
                if (newPos < line.pos):
                    self._textPos.col = line.col - (line.pos - newPos) - 1
                    break
                # Seek at the NEWLINE itself
                elif (newPos == line.pos):
                    self._textPos.col = line.col
                    break
            if (ln != 0): ln = ln-1
            self._textPos.ln = ln

        return
