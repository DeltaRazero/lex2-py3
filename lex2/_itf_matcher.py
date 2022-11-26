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

    from ._token import Token

    from lex2 import (
        textio,
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
    def match(self, ts: __.textio.ITextstream, token: __.Token) -> bool:
        """Looks for a pattern match and sets it in the provided token object.

        Parameters
        ----------
        ts : ITextstream
            Textstream object managed by the lexer object.
        token : Token
            Used to set the match data in the token.

        Returns
        -------
        bool
            True in case of a match.
        """
        ...
