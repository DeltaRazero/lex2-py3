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

    from lex2.util.types import (
        PtrType,
        Nullable,
    )

# ***************************************************************************************

class Rule:
    """Class representing a rule, used as filter during lexical analysis."""

    __slots__ = ('_matcher', 'id', 'regex', 'returns')

    # :: PRIVATE ATTRIBUTES :: #

    _matcher : __.PtrType[__.IMatcher]


    # :: READONLY ATTRIBUTES :: #

    id : str
    """<readonly> Rule identifier string."""

    regex : str
    """<readonly> The regular expression used by a matcher to perform regex matching."""


    # :: PUBLIC ATTRIBUTES :: #

    returns : bool
    """Whether tokens matched by this rule should be returned when scanning for tokens."""


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    def __init__(self, id: str, regex: str, returns: bool=True):
        """Rule object instance initializer.

        Parameters
        ----------
        id : str
            The identifying name of a resulting token (e.g. "NUMBER", "WORD").
        regex: str
            The regular expression used by a matcher to perform regex matching.
        returns : bool, optional
            Specify whether tokens matched by this rule should be returned when scanning
            for tokens.
            By default ``True``

        Raises
        ------
        ValueError
            If the given regular expression is empty.
        """
        self.id = id
        self.returns = returns

        self._matcher = None

        if (not regex):
            raise ValueError("The given regular expression must be non-empty")
        self.regex = regex

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

    def get_matcher(self) -> __.PtrType[__.IMatcher]:
        """Gets the IMatcher-compatible object instance.

        The rule matcher object is used by a lexer object to identify tokens during
        lexical analysis.

        Returns
        -------
        PtrType[IMatcher]
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

class RuleGroup (__.abc.ABC):
    """Abstract base class for making a creator class to dynamically build up a group of rules.

    To condense down the rule group into a single ``Rule`` object, use the inherited
    ``.rule()`` method.
    """

    # :: PRIVATE ATTRIBUTES :: #

    _id : str
    _returns : bool

    _regex_prefix : str
    _regex_groups : __.t.List[str]
    _regex_suffix : str


    # :: CONSTRUCTOR :: #

    @__.abc.abstractmethod
    def __init__(self,
                 id: str,
                 returns: bool=True,
                 regex_prefix: str="",
                 regex_suffix: str=""
    ):
        """Rule object instance initializer.

        Parameters
        ----------
        id : str
            The identifying name of a resulting token (e.g. "NUMBER", "WORD").
        returns : bool, optional
            Specify whether tokens matched by this rule group should be returned when scanning
            for tokens by default.
            By default ``True``
        regex_prefix : str, optional
            Regular expression that is prefixed for every added regex pattern group.
            By default ``""``
        regex_suffix : str, optional
            Regular expression that is suffixed for every added regex pattern group.
            By default ``""``
        """
        self._id = id
        self._returns = returns

        self._regex_prefix = regex_prefix
        self._regex_groups = []
        self._regex_suffix = regex_suffix

        return


    # :: PUBLIC METHODS :: #

    def rule(self, id: __.Nullable[str]=None, returns: __.Nullable[bool]=None) -> Rule:
        """Compiles the rule group to a rule object.

        Parameters
        ----------
        id : str, optional
            Overwrites the predefined identifying name of a resulting token.
            By default the id set by the parent class.
        returns : bool, optional
            Overwrites whether tokens matched by this rule group should be returned when scanning
            for tokens by default.
            By default the returns set by the parent class.

        Returns
        -------
        Rule

        Raises
        ------
        ValueError
            If the given regular expression is empty.
        """
        if (not id): id = self._id
        if (not returns): returns = self._returns

        if (not self._regex_groups):
            raise ValueError("The given regular expression must be non-empty")

        rule = Rule(
            id,
            f"{self._regex_prefix}({'|'.join(self._regex_groups)}){self._regex_suffix}",
            returns
        )
        return rule


    # :: PROTECTED METHODS :: #

    def _add_regex_group(self, regex: str) -> None:
        regex= f'({regex})'
        self._regex_groups.append(regex)
        return

# ***************************************************************************************

# SEE: https://github.com/python/mypy/issues/2984#issuecomment-285716826
# RulesetType = _t.List[Rule]
RulesetType = __.t.Sequence[Rule]
