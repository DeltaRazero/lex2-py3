
.. py:currentmodule:: lex2

Customizing Regex Engine
========================

In the event that the regex engine used by default (from Python's builtin ``re`` module) is inadequate, it is possible to substitute it for a regex engine of the user's own choice.


Underlying Architecture
-----------------------

While not essential, it may be beneficial to understand the way how the library utilizes a regex engine to match tokens. Each Rule stores a matcher-like object that implements the :class:`BaseMatcher <lex2.matcher.BaseMatcher>` abstract class (and thus the :class:`IMatcher <lex2.IMatcher>` interface). A matcher is responsible for carrying out the matching behaviour to try and identify text according to the regex pattern stored in the rule.

When a ruleset is assigned to a lexer, it will immediately check if each rule's matcher attribute is set accordingly, and will otherwise instantiate an appropriate matcher implementation. Also, if a matcher has not yet compiled the corresponding regex pattern, the lexer will automatically call the :meth:`compile_pattern() <lex2.IMatcher.compile_pattern>` method to do so.

When the lexer iterates over rules, it will access each rule's matcher and call the :meth:`match() <lex2.IMatcher.match>` method. This will a boolean to indicate whether a match was found. A lexer passes down its textstream to :meth:`match() <lex2.IMatcher.match>` to be used as input data for the compiled regex pattern, and passes down an instance of :class:`Token <lex2.Token>` for the matcher to store the match data in.

*The UML class diagram below visualizes and summarizes the relationships between classes and interfaces just discussed.*

.. figure:: /diagrams/png/matcher_structure.png
    :align: center
    :scale: 25%

    UML class diagram visualizing the textstream-lexer-rule-matcher relationships


Practical Example
-----------------

To explain how to define and use a custom matcher, it's best illustrated using a practical example. For this example, the regex engine from the library `'regex' by Matthew Barnett <https://pypi.org/project/regex/>`_ is used.

There's a few components:

* All matcher classes must inherit from the :class:`BaseMatcher <lex2.matcher.BaseMatcher>` abstract base class.
* The base class constructor must be called.
* Implementation of the :meth:`compile_pattern() <lex2.IMatcher.compile_pattern>` method.

    * A regex pattern string is given as input for generating a compiled regex pattern.
    * The compiled regex pattern needs to be stored as a class instance attribute, or via a reference to another object.

* Implementation of the :meth:`match() <lex2.IMatcher.match>` method.

    * The lexer's textstream is passed down to use as input for the compiled regex pattern. It is an instance of :class:`ITextstream <lex2.textio.ITextstream>`.
      |br|
      |i| Also see :ref:`Improving match() Performance on Python`. |/i|

    * A token is passed down to store the match data. It is an instance of :class:`Token <lex2.Token>`.

    * If a match is found, store the the string value of the match in ``token.data`` and the encapsulated groups in ``token.groups``, and return ``True``. If no match is found, return ``False``.

.. code-block:: python3
    :caption: Example of implementing a custom matcher

    import lex2
    import regex as rgx

    class CustomMatcher (lex2.matcher.BaseMatcher):

        _pattern : rgx.Pattern

        def __init__(self) -> None:
            super().__init__()

        def compile_pattern(self, regex: str) -> None:
            self._pattern = rgx.compile(regex)

        def match(self, ts: lex2.textio.ITextstream, token: lex2.Token) -> bool:
            regex_match = self._pattern.match(
                ts.get_string_buffer(),      # Data
                ts.get_string_buffer_pos(),  # Data position start
                ts.get_string_buffer_size(), # Data position end
            )
            if (regex_match):
                token.data   = regex_match.group()
                token.groups = regex_match.groups()
                return True
            return False

To use your custom defined matcher, you need to pass it as a template argument to the :func:`make_lexer() <_.lex2.make_lexer>` function as follows:

.. code-block:: python3

    lexer: lex2.ILexer = lex2.make_lexer(MATCHER_T=CustomMatcher)(ruleset, options)


Improving match() Performance on Python
---------------------------------------

Because Python has to constantly do dictionary lookups, accessing the string buffer variables through the interface methods may cause noticeable slowdown on larger lexing operations. Hence you can skip the methods and reference the private variables directly, as shown below.

.. code-block:: python3
    :caption: Accessing string buffer variables directly

    def match(self, ts: lex2.textio.ITextstream, token: lex2.Token) -> bool:
        regex_match = self._pattern.match(
            ts._string_buffer,      # Data
            ts._string_buffer_pos,  # Data position start
            ts._string_buffer_size, # Data position end
        )
        ...
