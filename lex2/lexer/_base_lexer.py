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
    )
    from lex2 import (
        Rule,
        RulesetType,
        ILexer,
        IMatcher,
        LexerOptions,
    )

# ***************************************************************************************

class BaseLexer (__.textio.TextIO, __.ILexer, __.abc.ABC):
    """Abstract base class partially implementing ILexer.
    """

    __slots__ = (
        '_rulesets', '_active_ruleset',
        '_options',
        '_uid'
    )

    # :: PROTECTED ATTRIBUTES :: #

    # A string value for uniquely identifying a matcher implementation. For pretty much
    # all cases, passing the class name is fine

    # Uses the UID from a matcher. It shouldn't be set manually, as that is done in the
    # make_lexer() factory function
    _uid : str

    _rulesets : __.t.List[__.RulesetType]
    _active_ruleset : __.RulesetType

    _options : __.LexerOptions


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    @__.abc.abstractmethod
    def __init__(self):
        """AbstractLexer object instance initializer.
        """
        super().__init__()

        self._uid = ""

        self._rulesets = []
        self._options  = __.LexerOptions()

        return


    def __del__(self):
        super().__del__()
        return


    # :: PUBLIC METHODS :: #

    def push_ruleset(self, ruleset: __.RulesetType) -> None:
        # Before pushing the ruleset, check if the rules' matcher objects are compiled for use in
        # the current lexer instance by checking the UID.
        self._compile_ruleset(ruleset)
        self._rulesets.append(ruleset)
        self._active_ruleset = self._rulesets[-1]
        return


    def pop_ruleset(self) -> None:
        self._rulesets.pop()
        self._active_ruleset = self._rulesets[-1]
        return


    def clear_rulesets(self) -> None:
        self._rulesets.clear()
        return


    # :: GETTERS & SETTERS :: #

    def get_options(self) -> __.LexerOptions:
        return self._options


    def set_options(self, options: __.LexerOptions) -> None:
        self._options = options
        return


    # :: PROTECTED METHODS :: #

    @__.abc.abstractmethod
    def _compile_rule(self, rule: __.Rule) -> __.IMatcher:
        """Compiles and sets a rule's matcher object.

        Parameters
        ----------
        rule : Rule

        Returns
        -------
        IMatcher
        """
        ...


    # :: PRIVATE METHODS :: #

    def _compile_ruleset(self, ruleset: __.RulesetType) -> None:
        """Checks and compiles rules within a newly pushed ruleset.

        Whenever a ruleset is pushed, this method will check if all rules have their
        corresponding IMatcher-compatible object set to the supported matcher type used
        by the current lexer instance, and compiles if necessary.
        """
        for rule in ruleset:
            if (not isinstance(rule, __.Rule)): # type: ignore
                raise TypeError(f'Object {rule} is not a (sub)class of {__.Rule.__name__}')

            if (self._needs_compilation(rule)):
                rule.set_matcher(self._compile_rule(rule))
        return


    def _needs_compilation(self, rule: __.Rule) -> bool:
        """Check if a rule's matcher object needs to be compiled.
        """
        needs_compilation = False
        matcher = rule.get_matcher()
        # If a matcher object is already compiled and stored, check the ID of the matcher
        if (matcher):
            needs_compilation = matcher.get_uid() != self._uid
        # If no object matcher object stored at all
        else:
            needs_compilation = True

        return needs_compilation
