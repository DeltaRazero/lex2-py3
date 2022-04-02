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


# comments = Comments().add_singleline_comment("a") \
#                      .add_multiline_comment("b", "a") \
#                      .to_rule()

# ***************************************************************************************

def __make_dummy_rule(id: str) -> __.Rule: return __.Rule(id, r"a^")
# __MakeDummyRule: _t.Callable[[str], _Rule] = lambda id: _Rule(id, r"a^")

# These rule object instances are not meant to be actually used in rulesets as they won't
# match anything.
# Instead, they are used to label and identify tokens by using the the rule ID property.
space   = __make_dummy_rule("SPACE")
tab     = __make_dummy_rule("TAB")
newline = __make_dummy_rule("NEWLINE")
