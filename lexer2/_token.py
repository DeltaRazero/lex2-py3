"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from . import excs as _excs
from . import file as _file

from ._rule import Rule as _Rule

# ***************************************************************************************

class Token:
    """Represents a token that is output during lexical analysis.
    """

  # --- RUNTIME/READONLY CONSTANTS --- #

    # Identifying string of the token's type (e.g. "NUMBER", "WORD") -- rule ID
    id_ : str

    # Position in the textstream where the token occurs
    position_ : _file.TextPosition


  # --- PROPERTIES --- #

    # String data of the identified token type
    data : str


  # --- CONSTRUCTOR --- #

    def __init__(self, id: str, data: str, position: _file.TextPosition):
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
        self.id_  = id
        self.data = data
        self.position_ = position

        return


  # --- PUBLIC METHODS --- #

    def IsRule(self, expectedRule: _Rule) -> bool:
        """Evaluates whether the token's identifier matches that of a given rule.

        Parameters
        ----------
        expectedRule : Rule
            Rule object instance.

        Returns
        -------
        bool
        """
        return self.id_ == expectedRule.id_


    def ValidateRule(self, expectedRule: _Rule) -> None:
        """Validates whether the token's identifier matches that of a given rule.

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
            raise _excs.UnknownTokenError(self.position_, self.data)
        return
