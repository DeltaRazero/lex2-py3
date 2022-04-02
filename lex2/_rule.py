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
    import typing as t

    from lex2._itf_matcher import (
        IMatcher,  # NOTE: Direct import to prevent class not being defined yet
    )

    from lex2._util.types import (
        ptr_t,
        nullable
    )

# ***************************************************************************************

class Rule:
    """Class representing a rule, used as filter during lexical analysis.

    Readonly Properties
    -------------------
    id : str
        The rule ID is the identifying string value of a token's type (e.g. "NUMBER",
        "WORD").
    regex_pattern : str
        The regex pattern string is used by a matcher to perform regex matching.

    Properties
    ----------
    returns: bool
        Whether tokens matched by this rule should be returned when scanning for tokens.
    """

    # :: READONLY PROPERTIES :: #

    # Rule identifier string
    id : str

    # The regex pattern string is used by a matcher to perform regex matching.
    regex_pattern : str


    # :: PROPERTIES :: #

    # Whether tokens matched by this rule should be returned when scanning for tokens.
    returns : bool


    # :: FIELDS :: #

    _matcher : __.ptr_t[__.IMatcher]


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    def __init__(self, id: str, regex_pattern: str, returns: bool=True):
        """Rule object instance initializer.

        Parameters
        ----------
        id : str
            The identifying string of a resulting token's type (e.g. "NUMBER", "WORD").
        regex_pattern : str
            Regex pattern used by a lexer to identify tokens during lexical analysis.
        returns : bool, optional
            Specify whether tokens matched by this rule should be returned when scanning
            for tokens.
            By default True
        """
        self.id = id
        self.regex_pattern = regex_pattern

        self.returns = returns

        self._matcher = None

        return


    def __del__(self):
        self._destruct_matcher()
        return


    # :: PRIVATE METHODS :: #

    def _destruct_matcher(self) -> None:
        if (self._matcher):
            del self._matcher
        self._matcher = None
        return


    # :: GETTERS :: #

    def get_matcher(self) -> __.ptr_t[__.IMatcher]:
        """Gets the IMatcher-compatible object instance.

        The rule matcher object is used by a lexer object to identify tokens during
        lexical analysis.

        Returns
        -------
        ptr_t[IMatcher]
        """
        return self._matcher


    # :: SETTERS :: #

    def set_matcher(self, matcher: __.IMatcher) -> None:
        """Sets the rule matcher object reference.

        Parameters
        ----------
        matcher : IMatcher
        """
        self._destruct_matcher()
        self._matcher = matcher
        return

# ***************************************************************************************

class RuleGroup (metaclass=__.abc.ABCMeta):

    # :: PRIVATE PROPERTIES :: #

    _default_id : str
    _default_returns : bool

    _regex_patterns : __.t.List[str]


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    def __init__(self, default_id: str, default_returns: bool=True):
        """Rule object instance initializer.

        Parameters
        ----------
        id : str
            The identifying string of a resulting token's type (e.g. "NUMBER", "WORD"). # TODO: Change description to identifier string
        regex_pattern : str
            Regex pattern used by a lexer to identify tokens during lexical analysis.
        returns : bool, optional
            Specify whether tokens matched by this rule group should be returned when scanning  # TODO: Add 'whether ... by default' in other files
            for tokens by default.
            By default True
        """
        self._default_id = default_id
        self._default_returns = default_returns

        self._regex_patterns = []

        return


    # :: PUBLIC METHODS :: #

    def to_rule(self, id: __.nullable[str]=None, returns: __.nullable[bool]=None) -> Rule:
        """Compiles the rule group to a rule object.

        Parameters
        ----------
        id : str, optional
            Identifier string.
            By default the default id from the child class
        returns : bool, optional
            Specify whether tokens matched by this rule group should be returned when scanning
            for tokens  by default.
            By default the default returns from the child class

        Returns
        -------
        Rule
        """
        if (not id): id = self._default_id
        if (not returns): returns = self._default_returns

        rule = Rule(
            id,
            '|'.join(self._regex_patterns),
            returns
        )
        return rule


    # :: PROTECTED METHODS :: #

    def _add_pattern_group(self, regex_pattern: str) -> None:
        regex_pattern = f'({regex_pattern})'
        self._regex_patterns.append(regex_pattern)
        return

# ***************************************************************************************

# SEE: https://github.com/python/mypy/issues/2984#issuecomment-285716826
# ruleset_t = _t.List[Rule]
ruleset_t = __.t.Sequence[Rule]
