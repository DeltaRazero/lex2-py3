"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# TODO: The profiler is currently pretty bland and limited. I would like to expand it
# some more in the future.

# ***************************************************************************************

class __:
    '<imports>'

    import abc
    import typing  as t
    import pathlib as pl
    import operator

    from ._generic_lexer import GenericLexer

    from lex2 import (
        textio,
    )
    from lex2 import (
        ruleset_t,
        ILexer,
        Token,
        LexerOptions,
    )

# ***************************************************************************************

class _RuleValueProfile:
    """Keeps track of the most common values of a rule.
    """

    # :: FIELDS :: #

    _value_occurrences : __.t.Dict[str, int]


    # :: CONSTRUCTOR :: #

    def __init__(self) -> None:

        self._value_occurrences = {}

        return


    # :: PUBLIC METHODS :: #

    def add_token(self, token: __.Token) -> None:

        if (token.data in self._value_occurrences):
            self._value_occurrences[token.data] += 1
        else:
            self._value_occurrences[token.data] = 1

        return


    def top_occurrences(self, threshold: int=10) -> __.t.Dict[str, int]:

        # First sort by map values
        self._value_occurrences = dict(
            sorted(
                self._value_occurrences.items(),
                key=__.operator.itemgetter(1),
                reverse=True
            )
        )

        to_return: __.t.Dict[str, int] = {}
        for key, value in self._value_occurrences.items():
            if (value >= threshold): to_return[key] = self._value_occurrences[key]

        return to_return

# ***************************************************************************************

class ProfilerLexer(__.GenericLexer):
    """A wrapper around a lexer implementation to provide profiling functionality.
    """

    # :: PRIVATE PROPERTIES :: #

    _rule_occurrences : __.t.Dict[str, int]
    _rule_profiles    : __.t.Dict[str, _RuleValueProfile]


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    @__.abc.abstractmethod
    def __init__(self):
        super().__init__()
        self._rule_profiles = {}

        return


    # :: INTERFACE METHODS (ILexer) :: #

    def get_next_token(self) -> __.Token:

        token = super().get_next_token()

        if (not (token.id in self._rule_occurrences)):
            self._rule_occurrences[token.id] = 0
            self._rule_profiles   [token.id] = _RuleValueProfile()

        self._rule_occurrences[token.id] += 1
        self._rule_profiles   [token.id].add_token(token)

        return token


    # :: PUBLIC METHODS :: #

    def show_report(self, value_occurrance_threshold: int=10) -> None:
        """Prints a report of which rules (identifiers) occur the most.

        Parameters
        ----------
        valueOccurranceThreshold : int, optional
            Threshold to display the top most occurring values of a rule. A value lower
            than 1 disables the display of values entirely.
            By default 10
        """

        # First sort by the rule occurrences map by values
        self._rule_occurrences = dict(
            sorted(
                self._rule_occurrences.items(),
                key=__.operator.itemgetter(1),
                reverse=True
            )
        )

        # Print description
        msg = "Most occuring rules"
        if (value_occurrance_threshold > 0):
            msg += f" + most occuring values respectively (limited to {value_occurrance_threshold})"

        print("\n" + msg)
        print('=' * len(msg))

        # Show most occurring values
        for key, value in self._rule_occurrences.items():

            # Rule identifier and amount of occurrences
            msg = f"{key}: {value}"
            print("\n" + msg)

            # If showing the top value occurrences, show them in order
            if (value_occurrance_threshold > 0):

                print('-' * len(msg))

                top_occurrences = self._rule_profiles[key].top_occurrences(threshold=value_occurrance_threshold)
                for key in top_occurrences:
                    print(f"    {key} : {top_occurrences[key]}")

        # Print newline
        print()

        return



'''

class ProfilerLexer (__.ILexer):
    """A wrapper around a lexer implementation to provide profiling functionality.
    """

    # :: FIELDS :: #

    _lexer : __.ILexer

    _rule_occurrences : __.t.Dict[str, int]
    _rule_profiles    : __.t.Dict[str, _RuleValueProfile]


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    def __init__(self, lexer: __.ILexer) -> None:
        """ProfilerLexer object instance initializer.

        Parameters
        ----------
        lexer : ILexer
            Instance of an ILexer implementation.
        """

        self._lexer = lexer

        self._rule = {}
        self._rule_profiles    = {}

        return


    def __del__(self):
        del self._lexer
        return


    # :: INTERFACE METHODS (ILexer) :: #

    def push_ruleset(self, ruleset: __.ruleset_t) -> None:
        self._lexer.push_ruleset(ruleset)
        return


    def pop_ruleset(self) -> None:
        self._lexer.pop_ruleset()
        return


    def clear_rulesets(self) -> None:
        self._lexer.clear_rulesets()
        return


    def get_options(self) -> __.LexerOptions:
        return self._lexer.get_options()


    def set_options(self, options: __.LexerOptions) -> None:
        return self._lexer.set_options(options)


    def get_next_token(self) -> __.Token:

        token = self._lexer.get_next_token()

        if (not (token.id in self._rule_occurrences)):
            self._rule_occurrences[token.id] = 0
            self._rule_profiles   [token.id] = _RuleValueProfile()

        self._rule_occurrences[token.id] += 1
        self._rule_profiles   [token.id].add_token(token)

        return token


    # :: INTERFACE METHODS (ITextIO) :: #

    def open(self,
             fp: __.t.Union[str, __.pl.Path],
             buffer_size: int=__.textio.DEFAULT_BUFFER_SIZE,
             encoding: str="UTF-8",
             convert_line_endings: bool=True,
    ) -> None:

        self._lexer.open(
            fp=fp,
            buffer_size=buffer_size,
            encoding=encoding,
            convert_line_endings=convert_line_endings
        )

        return


    def load(self,
             str_data: str,
             convert_line_endings: bool=False
    ) -> None:

        self._lexer.load(
            str_data=str_data,
            convert_line_endings=convert_line_endings,
        )

        return


    def close(self) -> None:

        self._lexer.close()

        return


    # :: PUBLIC METHODS :: #

    def show_report(self, value_occurrance_threshold: int=10) -> None:
        """Prints a report of which rules (identifiers) occur the most.

        Parameters
        ----------
        valueOccurranceThreshold : int, optional
            Threshold to display the top most occurring values of a rule. A value lower
            than 1 disables the display of values entirely.
            By default 10
        """

        # First sort by the rule occurrences map by values
        self._rule_occurrences = dict(
            sorted(
                self._rule_occurrences.items(),
                key=__.operator.itemgetter(1),
                reverse=True
            )
        )

        # Print description
        msg = "Most occuring rules"
        if (value_occurrance_threshold > 0):
            msg += f" + most occuring values respectively (limited to {value_occurrance_threshold})"

        print("\n" + msg)
        print('=' * len(msg))

        # Show most occurring values
        for key, value in self._rule_occurrences.items():

            # Rule identifier and amount of occurrences
            msg = f"{key}: {value}"
            print("\n" + msg)

            # If showing the top value occurrences, show them in order
            if (value_occurrance_threshold > 0):

                print('-' * len(msg))

                top_occurrences = self._rule_profiles[key].top_occurrences(threshold=value_occurrance_threshold)
                for key in top_occurrences:
                    print(f"    {key} : {top_occurrences[key]}")

        # Print newline
        print()

        return

'''
