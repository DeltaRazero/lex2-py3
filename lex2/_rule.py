"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import typing as _t

from .misc import ptr_t as _ptr_t
from ._intf_matcher import IMatcher as _IMatcher

# ***************************************************************************************

class Rule:
    """Class representing a rule, used as filter during lexical analysis.

    Readonly Properties
    -------------------
    id : str
        The rule ID is the identifying string value of a token's type (e.g. "NUMBER",
        "WORD").
    regexPattern : str
        The regex pattern string is used by a matcher to perform regex matching.

    Properties
    ----------
    returns: bool
        Whether tokens matched by this rule should be returned when scanning for tokens.
    """

  # --- READONLY PROPERTIES --- #

    # Rule identifier string
    id : str

    # The regex pattern string is used by a matcher to perform regex matching.
    regexPattern : str


  # --- PROPERTIES --- #

    # Whether tokens matched by this rule should be returned when scanning for tokens.
    returns : bool


  # --- FIELDS --- #

    _matcher : _ptr_t[_IMatcher]


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self, id: str, regexPattern: str, returns: bool=True):
        """Rule object instance initializer.

        Parameters
        ----------
        id : str
            The identifying string of a resulting token's type (e.g. "NUMBER", "WORD").
        regexPattern : str
            Regex pattern used by a lexer to identify tokens during lexical analysis.
        returns : bool, optional
            Specify whether tokens matched by this rule should be returned when scanning
            for tokens.
            By default True
        """
        self.id = id
        self.regexPattern = regexPattern

        self.returns = returns

        self._matcher = None

        return


    def __del__(self):
        self._DestructMatcher()
        return


  # --- PRIVATE METHODS --- #

    def _DestructMatcher(self) -> None:
        if (self._matcher):
            del self._matcher
        self._matcher = None
        return


  # --- GETTERS --- #

    def GetMatcher(self) -> _ptr_t[_IMatcher]:
        """Gets the IMatcher-compatible object instance.

        The rule matcher object is used by a lexer object to identify tokens during
        lexical analysis.

        Returns
        -------
        ptr_t[IMatcher]
        """
        return self._matcher


  # --- SETTERS --- #

    def SetMatcher(self, matcher: _IMatcher) -> None:
        """Sets the rule matcher object reference.

        Parameters
        ----------
        matcher : IMatcher
        """
        self._DestructMatcher()
        self._matcher = matcher
        return

# *****************************************************************************

# SEE: https://github.com/python/mypy/issues/2984#issuecomment-285716826
# ruleset_t = _t.List[Rule]
ruleset_t = _t.Sequence[Rule]
