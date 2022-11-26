"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import typing as t

    from ._rule import (
        Rule,
    )

    from lex2 import (
        excs,
        textio,
    )

# ***************************************************************************************

class Token:
    """Represents a token that is output during lexical analysis."""

    __slots__ = ('id', 'data', 'pos', 'groups')

    # :: ATTRIBUTES :: #

    id : str
    """The identifier of a token's type (e.g. "NUMBER", "WORD")."""

    data : str
    """Result of regex match."""

    groups : __.t.Sequence[str]
    """Result of regex match, split by encapsulated groups."""

    pos : __.textio.TextPosition
    """Position in the textstream where a token occurs."""


    # :: CONSTRUCTOR :: #

    def __init__(self, id: str="", data: str="", pos: __.textio.TextPosition=__.textio.TextPosition(), groups: __.t.Sequence[str]=()):
        """Token object instance initializer.

        Parameters
        ----------
        id : str, optional
            The identifying string of the resulting token's type (e.g. "NUMBER", "WORD").
            By default ``""``
        data : str, optional
            String data of the identified token.
            By default ``""``
        position : TextPosition, optional
            Position in the textstream where the token occurs.
            By default ``TextPosition()``
        groups : Iterable[str], optional
            Result of regex match, split by encapsulated groups.
            By default ``()``
        """
        self.id     = id
        self.data   = data
        self.pos    = pos
        self.groups = groups
        return


    # :: PUBLIC METHODS :: #

    def is_rule(self, expected_rule: __.Rule) -> bool:
        """Evaluates if the token's identifier matches that of a given rule.

        Parameters
        ----------
        expected_rule : Rule
            Rule object instance.

        Returns
        -------
        bool
        """
        return self.id == expected_rule.id


    def is_rule_oneof(self, expected_rules: __.t.List[__.Rule]) -> bool:
        """Evaluates if the token's identifier matches that one of a given list of rules.

        Parameters
        ----------
        expected_rules : List[Rule]
            List of Rule object instances.

        Returns
        -------
        bool
        """
        for expected_rule in expected_rules:
            if (self.id == expected_rule.id):
                return True
        return False


    def validate_rule(self, expected_rule: __.Rule) -> None:
        """Validates that the token's identifier matches that of a given rule.

        Parameters
        ----------
        expected_rule : Rule
            Rule object instance.

        Raises
        ------
        UnknownTokenError
            When the token's identifier does not match that of a given rule.
        """
        if (not self.is_rule(expected_rule)):
            raise __.excs.UnexpectedTokenError(self.pos, self.data, self.id, [expected_rule.id])
        return


    def validate_rule_oneof(self, expected_rules: __.t.List[__.Rule]) -> None:
        """Validates that the token's identifier matches that one of a given list of rules.

        Parameters
        ----------
        expected_rules : List[Rule]
            List of Rule object instances.

        Raises
        ------
        UnknownTokenError
            When the token's identifier does not match that of a given rule.
        """
        if (not self.validate_rule_oneof(expected_rules)):
            raise __.excs.UnexpectedTokenError(self.pos, self.data, self.id, [er.id for er in expected_rules])
        return
