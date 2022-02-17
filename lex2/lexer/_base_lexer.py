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

    from lex2 import (
        textio,
        predefs,
    )
    from lex2 import (
        ruleset_t,
        Rule,
        ILexer,
        IMatcher,
        LexerOptions,
    )

# ***************************************************************************************

class BaseLexer (__.textio.TextIO, __.ILexer, metaclass=__.abc.ABCMeta):
    """Abstract base class of an ILexer implementation.
    """

  # --- PROTECTED FIELDS --- #

    # A string value for uniquely identifying a matcher implementation. For pretty much
    # all cases, passing the class name works.
    _implementationId : str

    _rulesets : __.t.List[__.ruleset_t]
    _active_ruleset : __.ruleset_t

    _options : __.LexerOptions


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    @__.abc.abstractmethod
    def __init__(self):
        """AbstractLexer object instance initializer.
        """
        super().__init__()

        self._implementationId = ""

        self._rulesets = []
        self._options  = __.LexerOptions()

        return


    def __del__(self):
        super().__del__()
        return


  # --- PUBLIC METHODS --- #

    def PushRuleset(self, ruleset: __.ruleset_t) -> None:
        # Before pushing the ruleset, we check if the pattern matchers (saved in the rule
        # objects) are compiled for the specific lexer implementation this function is called from.
        self._CompileRuleset(ruleset)
        self._rulesets.append(ruleset)
        self._active_ruleset = self._rulesets[-1]
        return


    def PopRuleset(self) -> None:
        self._rulesets.pop()
        self._active_ruleset = self._rulesets[-1]
        return


    def ClearRulesets(self) -> None:
        self._rulesets.clear()
        return


  # --- GETTERS & SETTERS --- #

    def GetOptions(self) -> __.LexerOptions:
        return self._options


    def SetOptions(self, options: __.LexerOptions) -> None:
        self._options = options
        return


  # --- PROTECTED METHODS --- #

    @__.abc.abstractmethod
    def _CompileRule(self, rule: __.Rule) -> __.IMatcher:
        """Requests implemented lexer to compile a regex matcher object.

        Parameters
        ----------
        rule : Rule

        Returns
        -------
        IMatcher
        """
        ...


  # --- PRIVATE METHODS --- #

    def _CompileRuleset(self, ruleset: __.ruleset_t) -> None:
        """Checks and compiles rules within a newly pushed ruleset.

        Whenever a ruleset is pushed, this method will check if all rules have their
        corresponding IMatcher-compatible object set to the matcher type, used by
        a specific lexer/matcher implementation, and compiles if necessary.
        """
        for rule in ruleset:

            # TODO: Throw TypeError exception if rule is not of (sub)type Rule, so the error message is clearer for the user. This is dynamic language specific

            # Call the specific lexer implementation's CompileRule() method for regex
            # pattern matcher compilation
            if (self._NeedsCompilation(rule)):
                rule.SetMatcher(self._CompileRule(rule))

            # Comment rules have an addition rule to be compiled # TODO: REMOVE
            # if (rule.id == __.predefs.comment.id):
            #     # rule = static_cast<BaseComment*>(rule)->endRule
            #     rule: __.Rule = __.t.cast(__.predefs.BaseComment, rule).endRule
            #     if (self._NeedsCompilation(rule)):
            #         rule.SetMatcher(self._CompileRule(rule))

        return


    def _NeedsCompilation(self, rule: __.Rule) -> bool:
        """Check if the regex pattern matcher in a rule object needs to be compiled.
        """
        needs_compilation = False
        matcher = rule.GetMatcher()
        # If a Matcher object already compiled and stored, check the ID of the matcher
        # implementation
        if (matcher):
            needs_compilation = matcher.GetImplementationId() != self._implementationId
        # If no object Matcher object stored at all
        else:
            needs_compilation = True

        return needs_compilation
