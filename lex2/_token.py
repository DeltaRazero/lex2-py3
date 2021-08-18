"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    from . import (
        excs,
        textio,
    )

    from ._rule import Rule

# ***************************************************************************************

class Token:
    """Represents a token that is output during lexical analysis.

    Readonly Properties
    -------------------
    id : str
        The rule ID is the identifying string value of a token's type (e.g. "NUMBER",
        "WORD").
    position : TextPosition
        Position in the textstream where a token occurs.
    data : str
        String data of an identified token type.
    """

  # --- READONLY PROPERTIES --- #

    # Identifying string of the token's type (e.g. "NUMBER", "WORD") -- rule ID
    id : str

    # Position in the textstream where the token occurs
    position : _.textio.TextPosition

    # String data of the identified token type
    data : str


  # --- CONSTRUCTOR --- #

    def __init__(self, id: str, data: str, position: _.textio.TextPosition):
        """Token object instance initializer.

        Parameters
        ----------
        id : str
            The identifying string of the resulting token's type (e.g. "NUMBER", "WORD").
        data : str
            String data of the identified token.
        position : TextPosition
            Position in the textstream where the token occurs.
        """
        self.id  = id
        self.data = data
        self.position = position

        return


  # --- PUBLIC METHODS --- #

    def IsRule(self, expectedRule: _.Rule) -> bool:
        """Evaluates if the token's identifier matches that of a given rule.

        Parameters
        ----------
        expectedRule : Rule
            Rule object instance.

        Returns
        -------
        bool
        """
        return self.id == expectedRule.id


    def ValidateRule(self, expectedRule: _.Rule) -> None:
        """Validates that the token's identifier matches that of a given rule.

        Parameters
        ----------
        expectedRule : Rule
            Rule object instance.

        Raises
        ------
        UnknownTokenError
            When the token's identifier does not match that of a given rule.
        """
        if (not self.IsRule(expectedRule)):
            raise _.excs.UnexpectedTokenError(self.position, self.data, self.id)
        return
