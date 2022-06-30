"""Predefined rule objects and -template classes."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    from lex2 import (
        Rule,
        RuleGroup,
    )

# ***************************************************************************************

class Comments (__.RuleGroup):
    """Rule group for defining sourcecode-style comments."""

    def __init__(self):
        """"""
        super().__init__(
            id="COMMENT",
            returns=False
        )
        return


    def add_singleline_comment(self, start_regex: str) -> 'Comments':
        """Adds a definition for a singleline comment.

        Parameters
        ----------
        start_regex : str
            Regex denoting the start of a singleline comment.

        Returns
        -------
        Comments
        """
        self._add_regex_group(rf'{start_regex}.*')
        return self


    def add_multiline_comment(self, start_regex: str, end_regex: str) -> 'Comments':
        """Adds a definition for a multline comment.

        Parameters
        ----------
        start_regex : str
            Regex denoting the start of a singleline comment.
        end_regex : str
            Regex denoting the end of a singleline comment.

        Returns
        -------
        Comments
        """
        self._add_regex_group(rf'{start_regex}[\s\S]*?{end_regex}')
        return self


# comments = Comments().add_singleline_comment("a") \
#                      .add_multiline_comment("b", "a") \
#                      .to_rule()

# ***************************************************************************************

space = __.Rule("SPACE", r" ")
"""Rule defining a space character."""

tab = __.Rule("TAB", r"\t")
"""Rule defining a tab character."""

newline = __.Rule("NEWLINE", r"\n")
"""Rule defining a newline character."""
