"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# TODO: The profiler is currently pretty bland and limited. I would like to expand it
# some more in the future.

# ***************************************************************************************

class _:
    '<imports>'

    import typing  as t
    import pathlib as pl
    import operator

    from .. import (
        opts,
        textio,

        ruleset_t,
        ILexer,
        Token,
    )

# ***************************************************************************************

class _RuleValueProfile:
    """Keeps track of the most common values of a rule.
    """

  # --- FIELDS --- #

    _valueOccurrences : _.t.Dict[str, int]


  # --- CONSTRUCTOR --- #

    def __init__(self) -> None:

        self._valueOccurrences = {}

        return


  # --- PUBLIC METHODS --- #

    def AddToken(self, token: _.Token) -> None:

        if (token.data in self._valueOccurrences):
            self._valueOccurrences[token.data] += 1
        else:
            self._valueOccurrences[token.data] = 1

        return


    def TopOccurrences(self, threshold: int=10) -> _.t.Dict[str, int]:

        # First sort by map values
        self._valueOccurrences = dict(
            sorted(
                self._valueOccurrences.items(),
                key=_.operator.itemgetter(1),
                reverse=True
            )
        )

        to_return: _.t.Dict[str, int] = {}
        for key in self._valueOccurrences:
            value = self._valueOccurrences[key]
            if (value >= threshold): to_return[key] = self._valueOccurrences[key]

        return to_return

# ***************************************************************************************

class ProfilerLexer (_.ILexer):
    """A wrapper around a lexer implementation to provide profiling functionality.
    """

  # --- FIELDS --- #

    _lexer : _.ILexer

    _ruleOccurrences : _.t.Dict[str, int]
    _ruleProfiles    : _.t.Dict[str, _RuleValueProfile]


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self, lexer: _.ILexer) -> None:
        """ProfilerLexer object instance initializer.

        Parameters
        ----------
        lexer : ILexer
            Instance of an ILexer implementation.
        """

        self._lexer = lexer

        self._ruleOccurrences = {}
        self._ruleProfiles    = {}

        pass


    def __del__(self):
        del self._lexer
        return


  # --- INTERFACE METHODS (ILexer) --- #

    def PushRuleset(self, ruleset: _.ruleset_t) -> None:
        self._lexer.PushRuleset(ruleset)
        return


    def PopRuleset(self) -> None:
        self._lexer.PopRuleset()
        return


    def ClearRulesets(self) -> None:
        self._lexer.ClearRulesets()
        return


    def GetOptions(self) -> _.opts.LexerOptions:
        return self._lexer.GetOptions()


    def GetNextToken(self) -> _.Token:

        token = self._lexer.GetNextToken()

        if (not (token.id in self._ruleOccurrences)):
            self._ruleOccurrences[token.id] = 0
            self._ruleProfiles   [token.id] = _RuleValueProfile()

        self._ruleOccurrences[token.id] += 1
        self._ruleProfiles   [token.id].AddToken(token)

        return token


  # --- INTERFACE METHODS (ITextIO) --- #

    def Open(self,
             fp: _.t.Union[str, _.pl.Path],
             bufferSize: int=_.textio.DEFAULT_BUFFER_SIZE,
             encoding: str="UTF-8",
             convertLineEndings: bool=True,
    ) -> None:

        self._lexer.Open(
            fp=fp,
            bufferSize=bufferSize,
            encoding=encoding,
            convertLineEndings=convertLineEndings
        )

        return


    def Load(self,
             strData: str,
             convertLineEndings: bool=False
    ) -> None:

        self._lexer.Load(
            strData=strData,
            convertLineEndings=convertLineEndings,
        )

        return


    def Close(self) -> None:

        self._lexer.Close()

        return


  # --- PUBLIC METHODS --- #

    def ShowReport(self, valueOccurranceThreshold: int=10) -> None:
        """Prints a report of which rules (identifiers) occur the most.

        Parameters
        ----------
        valueOccurranceThreshold : int, optional
            Threshold to display the top most occurring values of a rule. A value lower
            than 1 disables the display of values entirely.
            By default 10
        """

        # First sort by the rule occurrences map by values
        self._ruleOccurrences = dict(
            sorted(
                self._ruleOccurrences.items(),
                key=_.operator.itemgetter(1),
                reverse=True
            )
        )

        # Print description
        msg = "Most occuring rules"
        if (valueOccurranceThreshold > 0):
            msg += f" + most occuring values respectively (limited to {valueOccurranceThreshold})"

        print("\n" + msg)
        print('=' * len(msg))

        # Show most occurring values
        for key in self._ruleOccurrences:

            # Rule identifier and amount of occurrences
            msg = f"{key}: {self._ruleOccurrences[key]}"
            print("\n" + msg)

            # If showing the top value occurrences, show them in order
            if (valueOccurranceThreshold > 0):

                print('-' * len(msg))

                top_occurrences = self._ruleProfiles[key].TopOccurrences(threshold=valueOccurranceThreshold)
                for key in top_occurrences:
                    print(f"    {key} : {top_occurrences[key]}")

        # Print newline
        print()

        return
