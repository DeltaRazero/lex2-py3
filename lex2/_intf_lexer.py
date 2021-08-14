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

    from . import textio

    from .opts   import LexerOptions
    from ._token import Token
    from ._rule  import ruleset_t

# ***************************************************************************************

class ILexer (_.textio.ITextIO, metaclass=_.abc.ABCMeta):
    """Common interface to a lexer object instance.
    """

  # --- INTERFACE METHODS --- #

    @_.abc.abstractmethod
    def PushRuleset(self, ruleset: _.ruleset_t) -> None:
        """Pushes a ruleset to the lexer's ruleset-stack.

        Parameters
        ----------
        ruleset : ruleset_t
        """
        pass

    @_.abc.abstractmethod
    def PopRuleset(self) -> None:
        """Pops a ruleset from the lexer's ruleset-stack.
        """
        pass

    @_.abc.abstractmethod
    def ClearRulesets(self) -> None:
        """Clears all rulesets from the lexer's ruleset-stack.
        """
        pass


    @_.abc.abstractmethod
    def GetNextToken(self) -> _.Token:
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

    @_.abc.abstractmethod
    def GetOptions(self) -> _.LexerOptions:
        """Gets the LexerOptions object instance to define processing options of the lexer.

        Returns
        -------
        LexerOptions
        """
        pass
