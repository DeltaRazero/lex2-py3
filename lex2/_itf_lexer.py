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

    from lex2 import (
        Token,
        ruleset_t,
        LexerOptions,
    )

# ***************************************************************************************

class ILexer (__.textio.ITextIO, metaclass=__.abc.ABCMeta):
    """Common interface to a lexer object instance.
    """

  # --- INTERFACE METHODS --- #

    @__.abc.abstractmethod
    def PushRuleset(self, ruleset: __.ruleset_t) -> None:
        """Pushes a ruleset to the lexer's ruleset-stack.

        Parameters
        ----------
        ruleset : ruleset_t
        """
        ...

    @__.abc.abstractmethod
    def PopRuleset(self) -> None:
        """Pops a ruleset from the lexer's ruleset-stack.
        """
        ...

    @__.abc.abstractmethod
    def ClearRulesets(self) -> None:
        """Clears all rulesets from the lexer's ruleset-stack.
        """
        ...


    @__.abc.abstractmethod
    def GetNextToken(self) -> __.Token:
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
        ...


  # --- INTERFACE GETTERS & SETTERS --- #

    @__.abc.abstractmethod
    def GetOptions(self) -> __.LexerOptions:
        """Gets the LexerOptions object instance to define processing options of the lexer.

        Returns
        -------
        LexerOptions
        """
        ...

    @__.abc.abstractmethod
    def SetOptions(self, options: __.LexerOptions) -> None:
        """Sets the LexerOptions object instance to define processing options of the lexer.

        Parameters
        ----------
        options : LexerOptions
        """
        ...
