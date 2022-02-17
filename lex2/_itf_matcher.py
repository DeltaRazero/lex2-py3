"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import abc

    from lex2 import (
        textio,
    )

    from lex2._util.types import (
        ptr_t,
    )

# ***************************************************************************************

class IMatcher (metaclass=__.abc.ABCMeta):
    """Common interface to a rule matcher object instance.
    """

  # --- INTERFACE GETTERS --- #

    @__.abc.abstractmethod
    def GetImplementationId(self) -> str:
        """Gets the lexer implementation identifier string.

        Returns
        -------
        str
        """
        ...


    @__.abc.abstractmethod
    def CompilePattern(self, regexPattern: str) -> __.ptr_t[str]:
        """Compiles regex pattern to implementation-specific regex matcher object.

        Parameters
        ----------
        regexPattern
            Regular expression to compile.
        """
        ...


    @__.abc.abstractmethod
    def Match(self, ts: __.textio.ITextstream) -> __.ptr_t[str]:
        """Looks for a pattern match and returns string data in case of a match.

        Parameters
        ----------
        ts : ITextstream
            Textstream object managed by the lexer object.

        Returns
        -------
        ptr_t[str]
            Nullable string object. Contains string data in case of a match, otherwise
            NULL/None.
        """
        ...
