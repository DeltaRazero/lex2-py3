"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc as _abc

from . import textio as _textio
from ._token import Token     as _Token
from ._rule  import ruleset_t as _ruleset_t
from ._flags import HFlags    as _HFlags

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
        UnknownTokenError
            If a token with an unknown rule pattern is encountered AND the HandlerFlag
            value for 'unknownToken' has been set to HANDLE_AND_RETURN.
        EndOfTextstream
            If the lexer reaches the end of the textstream data.
        """
        pass


  # --- INTERFACE GETTERS --- #

    @_abc.abstractmethod
    def GetHFlags(self) -> _HFlags:
        """Gets the HFlags (HandlerFlags) object instance.

        Returns
        -------
        HFlags
        """
        pass
