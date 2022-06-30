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

    from lex2.util.types import (
        PtrType,
    )

# ***************************************************************************************

class IMatcher (__.abc.ABC):
    """Common interface to a rule matcher object instance.
    """

    # :: INTERFACE GETTERS :: #

    @__.abc.abstractmethod
    def get_uid(self) -> str:
        """Gets the unique identifier (UID) of the matcher implementation.

        Returns
        -------
        str
        """
        ...


    @__.abc.abstractmethod
    def compile_pattern(self, regex: str) -> None:
        """Compiles regex pattern to implementation-specific regex matcher object.

        Parameters
        ----------
        regex
            Regular expression to compile.
        """
        ...


    @__.abc.abstractmethod
    def match(self, ts: __.textio.ITextstream) -> __.PtrType[str]:
        """Looks for a pattern match and returns string data in case of a match.

        Parameters
        ----------
        ts : ITextstream
            Textstream object managed by the lexer object.

        Returns
        -------
        PtrType[str]
            Nullable string object. Contains string data in case of a match, otherwise
            NULL/None.
        """
        ...
