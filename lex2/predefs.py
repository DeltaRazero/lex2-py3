"""Predefined rule objects and -template classes."""

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

    from lex2 import (
        Rule,
        RuleGroup,
    )

# ***************************************************************************************

class Comments (__.RuleGroup):

    def __init__(self):
        super().__init__(
            default_id="COMMENT",
            default_returns=False
        )
        return


    def add_singleline_comment(self, start_regex: str) -> 'Comments':
        self._add_pattern_group(rf'{start_regex}.*')
        return self


    def add_multiline_comment(self, start_regex: str, end_regex: str) -> 'Comments':
        self._add_pattern_group(rf'{start_regex}[\s\S]*?{end_regex}')
        return self


# comments = Comments().add_comment_singleline("a") \
#                      .add_comment_multiline("b", "a") \
#                      .to_rule()

r'''

class BaseComment (__.Rule, metaclass=__.abc.ABCMeta):
    """Base class for a rule filtering comments.
    """

  # --- CONSTANTS --- #

    RULE_ID = "COMMENT"


  # --- READONLY PROPERTIES --- #

    endRule : __.Rule


  # --- CONSTRUCTOR --- #

    @__.abc.abstractmethod
    def __init__(self, regexPatternStart: str, regexPatternEnd: str):
        """
        """
        __.Rule.__init__(self, self.RULE_ID, regexPatternStart, returns=False)
        self.endRule = __.Rule(self.RULE_ID, regexPatternEnd)
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
        super().__init__(
            regexPatternStart=identifyingRegex,
            regexPatternEnd  =r".*"
        )

        return


class MultilineComment (BaseComment):
    """Rule template for filtering singleline comments.
    """

  # --- CONSTRUCTOR --- #

    def __init__(self, identifyingStartRegex: str, identifyingEndRegex: str):
        r"""SinglelineComment object instance initializer.

        Parameters
        ----------
        identifyingStartRegex : str
            This regex pattern denotes the start of a multiline comment. For example:
            r"\/\*" (/*).
        identifyingEndRegex : str
            This regex pattern denotes the start of a multiline comment. For example:
            r"\*\/" (*/).
        """
        super().__init__(
            regexPatternStart=identifyingStartRegex,
            regexPatternEnd  =rf'[\s\S]*?{identifyingEndRegex}|[\s\S]*'
            # regexPatternEnd  =r"([\s\S]*?)\*\/|([\s\S]*)"
        )

        return
'''

# ***************************************************************************************

def __MakeDummyRule(id: str) -> __.Rule: return __.Rule(id, r"a^")
# __MakeDummyRule: _t.Callable[[str], _Rule] = lambda id: _Rule(id, r"a^")

# These rule object instances are not meant to be actually used in rulesets as they won't
# match anything.
# Instead, they are used to label and identify tokens by using the the rule ID property.
space        = __MakeDummyRule("SPACE")
tab          = __MakeDummyRule("TAB")
newline      = __MakeDummyRule("NEWLINE")
