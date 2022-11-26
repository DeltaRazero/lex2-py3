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
        RulesetType,
        LexerOptions,
    )

# ***************************************************************************************

class ILexer (__.textio.ITextIO, __.abc.ABC):
    """Common interface to a lexer object instance.
    """

    # :: INTERFACE METHODS :: #

    @__.abc.abstractmethod
    def push_ruleset(self, ruleset: __.RulesetType) -> None:
        """Pushes a ruleset to the ruleset-stack.

        Parameters
        ----------
        ruleset : RulesetType
        """
        ...

    @__.abc.abstractmethod
    def pop_ruleset(self) -> None:
        """Pops a ruleset from the ruleset-stack.
        """
        ...

    @__.abc.abstractmethod
    def clear_rulesets(self) -> None:
        """Clears all rulesets from the ruleset-stack.
        """
        ...


    @__.abc.abstractmethod
    def get_next_token(self) -> __.Token:
        """Finds the next token in the textstream using the currently active ruleset.

        Returns
        -------
        Token

        Raises
        ------
        UnknownTokenError
            If an unknown token type has been encountered.
        EOF
            If the lexer has reached the end of input data from a textstream.
        """
        ...


    # :: INTERFACE GETTERS & SETTERS :: #

    @__.abc.abstractmethod
    def get_options(self) -> __.LexerOptions:
        """Gets the lexer options to define processing options of the lexer.

        Returns
        -------
        LexerOptions
        """
        ...

    @__.abc.abstractmethod
    def set_options(self, options: __.LexerOptions) -> None:
        """Sets the lexer options to define processing options of the lexer.

        Parameters
        ----------
        options : LexerOptions
        """
        ...
