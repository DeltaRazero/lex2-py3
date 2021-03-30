"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import typing as _t

# ***************************************************************************************

# Struct
class LexerOptions:
    """Struct to define processing options of a lexer.

    Properties
    ----------
    returnSpace : bool
        Flag to specify if a SPACE character token should be returned or ignored.
        Defaults to False (ignore)
    returnTab : bool
        Flag to specify if a TAB character token should be returned or ignored.
        Defaults to False (ignore)
    returnNewline : bool
        Flag to specify if a NEWLINE character token should be returned or ignored.
        Defaults to False (ignore)
    returnComment : bool
        Flag to specify if a COMMENT token should be returned or ignored.
        Defaults to False (ignore)
    returnRule : Dict[str, bool]
        Map with <str, str> keypairs to specify which user-defined tokens should be
        returned or ignored.
    """

  # --- PROPERTIES --- #

    returnSpace   : bool
    returnTab     : bool
    returnNewline : bool
    returnComment : bool

    # Key should be the identifier string value of a Rule object. To check whether a
    # token should be returned or ignored, the map gets checked for existence of the
    # token's identifier string as key value.
    returnRule : _t.Dict[str, bool]


  # --- CONSTRUCTOR --- #

    def __init__(self):

        self.returnSpace   = False
        self.returnTab     = False
        self.returnNewline = False
        self.returnComment = False

        self.returnRule = {}

        return
