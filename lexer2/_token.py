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

  # --- FIELDS --- #

    _id   : str
    _data : str

    _position : _file.TextPosition


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
        self._id   = id
        self._data = data
        self._position = position

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
        return self._id == expectedRule.ID


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
            raise _excs.UnknownTokenError(self._position, self._data)
        return


  # --- GETTERS --- #

    def GetId(self) -> str:
        """Gets the identifying string of the token's type (e.g. "NUMBER", "WORD").

        Returns
        -------
        str
        """
        return self._id


    def GetData(self) -> str:
        """Gets the string data of the identified token type.

        Returns
        -------
        str
        """
        return self._data


    def GetPosition(self) -> _file.TextPosition:
        """Gets the position in the textstream where the token occurs.

        Returns
        -------
        TextPosition
        """
        return self._position
