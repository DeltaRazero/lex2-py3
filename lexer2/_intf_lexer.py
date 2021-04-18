"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc as _abc

from . import textio as _textio
from .opts   import LexerOptions as _LexerOptions
from ._token import Token        as _Token
from ._rule  import ruleset_t    as _ruleset_t

# ***************************************************************************************

class ILexer (_textio.ITextIO, metaclass=_abc.ABCMeta):
    """Common interface to a lexer object instance.
    """

  # --- INTERFACE METHODS --- #

    @_abc.abstractmethod
    def PushRuleset(self, ruleset: _ruleset_t) -> None:
        """Pushes a ruleset to the lexer's ruleset-stack.

        Parameters
        ----------
        ruleset : ruleset_t
        """
        pass

    @_abc.abstractmethod
    def PopRuleset(self) -> None:
        """Pops a ruleset from the lexer's ruleset-stack.
        """
        pass

    @_abc.abstractmethod
    def ClearRulesets(self) -> None:
        """Clears all rulesets from the lexer's ruleset-stack.
        """
        pass


    @_abc.abstractmethod
    def GetNextToken(self) -> _Token:
        """Finds the next token in the textstream, by using the currently active ruleset.

        Returns
        -------
        Token

        Raises
        ------
        UnidentifiedTokenError
            If an unexpected token type has been encountered.
        EndOfData
            If the lexer has reached the end of input data.
        """
        pass


  # --- INTERFACE GETTERS --- #

    @_abc.abstractmethod
    def GetOptions(self) -> _LexerOptions:
        """Gets the LexerOptions object instance to define processing options of the lexer.

        Returns
        -------
        LexerOptions
        """
        pass
