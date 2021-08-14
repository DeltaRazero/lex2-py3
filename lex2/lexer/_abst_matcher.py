"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    import abc

    from .. import misc
    from .. import IMatcher

# ***************************************************************************************

class AbstractMatcher (_.IMatcher, metaclass=_.abc.ABCMeta):
    """Abstract base class of an IMatcher implementation.
    """

  # --- PROTECTED FIELDS --- #

    # Regex pattern used by a lexer to identify tokens during lexical analysis.
    _regexPattern : str


  # --- PRIVATE FIELDS --- #

    # Lexer implementation identifier string (a.k.a. 'vendor ID').
    _vendorId : str


  # --- CONSTRUCTOR --- #

    @_.abc.abstractmethod
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

    @_.abc.abstractmethod
    def _CompilePattern(self) -> None:
        """Compiles regex pattern to implementation-specific regex matcher object.
        """
        pass


  # --- GETTERS --- #

    def GetVendorId(self) -> str:
        return self._vendorId

    @_.abc.abstractmethod
    def GetPatternMatcher(self) -> _.misc.voidptr_t:
        pass
