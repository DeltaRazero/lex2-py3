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
    import typing  as t
    import operator
    import os

    from ._generic_lexer import GenericLexer

    from lex2 import (
        Token,
    )

# ***************************************************************************************

class _RuleValueProfile:
    """Keeps track of the most common values of a rule."""

    # :: PRIVATE ATTRIBUTES :: #

    # <str: token value> , <int: amount of times that value occurred>
    _value_occurrences : __.t.Dict[str, int]


    # :: CONSTRUCTOR :: #

    def __init__(self) -> None:
        self._value_occurrences = {}
        return


    # :: PUBLIC METHODS :: #

    def add_token(self, token: __.Token) -> None:
        """Adds a token's value to the """
        if (token.data in self._value_occurrences):
            self._value_occurrences[token.data] += 1
        else:
            self._value_occurrences[token.data] = 1
        return


    def top_occurrences(self, threshold: int) -> __.t.Dict[str, int]:
        """Returns an ordered map of values sorted by occurrence (with a threshold)."""
        # First make a sorted map by value
        self._value_occurrences = dict(
            sorted(
                self._value_occurrences.items(),
                key=__.operator.itemgetter(1),
                reverse=True
            )
        )

        # Apply threshold
        processed_map: __.t.Dict[str, int] = {}
        for value, occurrences in self._value_occurrences.items():
            if (occurrences >= threshold): processed_map[value] = self._value_occurrences[value]

        return processed_map


class _RuleProfile:
    occurrence    : int
    value_profile : _RuleValueProfile

    def __init__(self) -> None:
        self.occurrence    = 0
        self.value_profile = _RuleValueProfile()
        return

# ***************************************************************************************

class ProfilerLexer(__.GenericLexer):
    """A wrapper around a lexer implementation to provide profiling functionality.
    """

    # :: PRIVATE ATTRIBUTES :: #

    _profiles : __.t.Dict[str, _RuleProfile]


    # :: CONSTRUCTOR :: #

    @__.abc.abstractmethod
    def __init__(self):
        self._profiles = {}

        super().__init__()
        return


    # :: INTERFACE METHODS (ILexer) :: #

    def get_next_token(self) -> __.Token:

        token = super().get_next_token()

        if (not (token.id in self._profiles)):
            self._profiles[token.id] = _RuleProfile()

        profile = self._profiles[token.id]
        profile.occurrence += 1
        profile.value_profile.add_token(token)

        return token


    def close(self) -> None:

        if (self._profiles):
            self.show_report()

        return super().close()


    # :: PUBLIC METHODS :: #

    def show_report(self, value_occurrence_threshold: int=10) -> None:
        """Prints a report of which rules (identifiers) occur the most.

        This method is automatically called when it hasn't been called manually yet and
        the textstream is closed (also done when the lexer is destroyed by the garbage
        collector).

        After the report is printed, the profile will be cleared.

        Parameters
        ----------
        value_occurrence_threshold : int, optional
            Threshold to display the top most occurring values of a rule. A value lower
            than 1 disables the display of values entirely.
            By default ``10``
        """
        TAB = '  '

        # First sort by the rule occurrences map by values
        self._profiles = dict(
            sorted(
                self._profiles.items(),
                key=lambda item: item[1].occurrence,
                reverse=True
            )
        )

        self._heading(
            "Lexer profiler report",
            underline_char='=',
            double_line=True,
            full_width=True,
        )

        # Print description
        self._heading(
            "Most occurring rules",
            double_line=True,
            full_width=True,
        )

        print(f'Occurrence value threshold is set to {value_occurrence_threshold}')

        for rule_id, profile in self._profiles.items():

            msg = f"{rule_id} : {profile.occurrence}"
            if (value_occurrence_threshold <= 0):
                print(msg)
            else:
                self._heading(msg)
                padding = len(str(profile.occurrence)) - 1

                top_occurrences = profile.value_profile.top_occurrences(threshold=value_occurrence_threshold)
                for key in top_occurrences:
                    print(f'{TAB}{top_occurrences[key]: <{padding}} : {key}' )

        # Print a final newline
        print()

        # Clear profile
        self._profiles = {}

        return


    # :: HELPER METHODS :: #

    @staticmethod
    def _heading( msg: str, underline_char: str='-', double_line: bool=False, full_width: bool=False) -> None:

        length = __.os.get_terminal_size().columns-1 if full_width else len(msg)
        line = underline_char * length

        NEWLINE = '\n' # Because Python doesn't like conditional newline in format-strings...
        print(f'{line if double_line else ""}\n{msg}\n{line}{NEWLINE if full_width else ""}')

        return
