"""Predefined rule objects and -template classes."""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc    as _abc
import typing as _t

from ._rule import Rule as _Rule

# ***************************************************************************************

class BaseComment (_Rule, metaclass=_abc.ABCMeta):
    """Base class for a rule filtering comments.
    """

  # --- CONSTANTS --- #

    RULE_ID = "COMMENT"


  # --- READONLY PROPERTIES --- #

    ruleEnd : _Rule


  # --- CONSTRUCTOR --- #

    @_abc.abstractmethod
    def __init__(self, regexPatternStart: str, regexPatternEnd: str):
        """
        """
        _Rule.__init__(self, self.RULE_ID, regexPatternStart)
        self.ruleEnd = _Rule(self.RULE_ID, regexPatternEnd)
        return


class SinglelineComment (BaseComment):
    """Rule template for filtering singleline comments.
    """

  # --- CONSTRUCTOR --- #

    def __init__(self, identifyingRegex: str):
        """SinglelineComment object instance initializer.

        Parameters
        ----------
        identifyingRegex : str
            This regex pattern denotes the start of a singleline comment. For example:
            r"//".
        """
        BaseComment.__init__(
            self,
            regexPatternStart=identifyingRegex,
            regexPatternEnd  =r".*"
        )

        return


class MultilineComment (BaseComment):
    """Rule template for filtering singleline comments.
    """

  # --- CONSTRUCTOR --- #

    def __init__(self, identifyingStartRegex: str, identifyingEndRegex: str):
        """SinglelineComment object instance initializer.

        Parameters
        ----------
        identifyingStartRegex : str
            This regex pattern denotes the start of a multiline comment. For example:
            r"\/\*" (/*).
        identifyingEndRegex : str
            This regex pattern denotes the start of a multiline comment. For example:
            r"\*\/" (*/).
        """
        BaseComment.__init__(
            self,
            regexPatternStart=identifyingStartRegex,
            regexPatternEnd  =r"[\s\S]*?{}|[\s\S]*".format(identifyingEndRegex)
            # regexPatternEnd  =r"([\s\S]*?)\*\/|([\s\S]*)"
        )

        return

# ***************************************************************************************

def __MakeDummyRule(id: str) -> _Rule: return _Rule(id, r"a^")
# __MakeDummyRule: _t.Callable[[str], _Rule] = lambda id: _Rule(id, r"a^")

# These rule object instances are not meant to be actually used in rulesets as they won't
# match anything.
# Instead, they are used to label and identify tokens by using the the rule ID property.
space        = __MakeDummyRule("SPACE")
tab          = __MakeDummyRule("TAB")
newline      = __MakeDummyRule("NEWLINE")

comment      = __MakeDummyRule(BaseComment.RULE_ID)
