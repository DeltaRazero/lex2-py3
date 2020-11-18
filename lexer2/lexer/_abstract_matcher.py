"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc as _abc

from .. import misc as _misc
from .. import IMatcher as _IMatcher

# ***************************************************************************************

class AbstractMatcher (_IMatcher, metaclass=_abc.ABCMeta):
    """Abstract base class of an IMatcher implementation.
    """

  # --- PROTECTED FIELDS --- #

    # Regex pattern used by a lexer to identify tokens during lexical analysis.
    _regexPattern : str


  # --- PRIVATE FIELDS --- #

    # Lexer implementation identifier string (a.k.a. 'vendor ID').
    _vendorId : str


  # --- CONSTRUCTOR --- #

    @_abc.abstractmethod
    def __init__(self, vendorId: str, regexPattern: str) -> None:
        """AbstractMatcher object instance initializer.

        Parameters
        ----------
        vendorId : str
            Lexer implementation identifier string (a.k.a. 'vendor ID').
        regexPattern : str
            Regex pattern used by a lexer to identify tokens during lexical analysis.
        """
        self._vendorId = vendorId
        self._regexPattern = regexPattern

        self._CompilePattern()

        return


  # --- PROTECTED METHODS --- #

    @_abc.abstractmethod
    def _CompilePattern(self) -> None:
        """Compiles regex pattern to implementation-specific regex matcher object.
        """
        pass


  # --- GETTERS --- #

    def GetVendorId(self) -> str:
        return self._vendorId

    @_abc.abstractmethod
    def GetPatternMatcher(self) -> _misc.voidptr_t:
        pass
