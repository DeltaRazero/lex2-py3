"""Predefined rule objects and -template classes."""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._rule import Rule as _Rule

# ***************************************************************************************

space = _Rule(
    "SPACE",
    r" "
)

tab = _Rule(
    "TAB",
    r"\t"
)

newline = _Rule(
    "NEWLINE",
    r"\n"
)

unknownToken = _Rule(
    "UNKNOWN_TOKEN",
    r"[^ \t\n]*"
)

# ***************************************************************************************

class BaseComment (_Rule):
    """Base class for a rule filtering comments.
    """

    def __init__(self, regexPattern: str, name: str="COMMENT"):
        _Rule.__init__(self, name, regexPattern)

        return

# This rule object instance is not meant to be used by the user, as it doesn't actually
# match anything. Instead, it's used by lexers as common object to identify tokens as
# "COMMENT" (rules that inherit BaseComment, SinglinelineComment or MultilineComment)
_comment_ = BaseComment(r"a^")


class SinglelineComment (BaseComment):
    """Rule template for filtering single-line comments.
    """

  # --- CONSTRUCTOR --- #

    def __init__(self, identifyingChars: str):
        """SinglelineComment object instance initializer.

        Parameters
        ----------
        identifyingChars : str
            Combination of characters that identify the start of a single-line comment
            (e.g. "//" or "#").
        """
        BaseComment.__init__(self, self._GenerateRegex(identifyingChars))

        return


  # --- PRIVATE METHODS --- #

    @staticmethod
    def _GenerateRegex(identifyingChars: str) -> str:
        return "[{0}].*".format(identifyingChars)


class MultilineComment (BaseComment):
    """Rule template for filtering multi-line comments.
    """

  # --- CONSTRUCTOR --- #

    def __init__(self, identifyingStartChars: str, identifyingEndChars: str):
        """SinglelineComment object instance initializer.

        Parameters
        ----------
        identifyingStartChars : str
            Combination of characters that identify the start of a multi-line comment
            (e.g. "/*").
        identifyingEndChars : str
            Combination of characters that identify the end of a multi-line comment
            (e.g. "*/").
        """
        BaseComment.__init__(self, self._GenerateRegex(identifyingStartChars, identifyingEndChars))

        return


  # --- PRIVATE METHODS --- #

    @staticmethod
    def _GenerateRegex(identifyingStartChars: str, identifyingEndChars: str) -> str:
        regex_start = ""
        for char in identifyingStartChars:
            regex_start += "\\{0}".format(char)

        regex_end = ""
        for char in identifyingEndChars:
            regex_end += "\\{0}".format(char)

        return "({0})(.|\\n)+?({1})".format(regex_start, regex_end)
