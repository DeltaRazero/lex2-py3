
.. py:currentmodule:: lex2

Defining Rulesets
=================

.. _url_regex: https://www.regular-expressions.info/quickstart.html

The purpose of a lexer is to break a stream of text characters into a sequence of tokens (strings with an assigned and thus identified meaning). Before tokens can be recognized, of course, it must first be clear which tokens are possible and how they can be recognized as such. This is done by defining a set of rules, each defining a regex pattern on how to recognize a particular token and what identifiable name it should be assigned to it.

.. note::
    If you are not familiar with regular expressions (regex), the `quickstart guide on regular-expressions.info <_url_regex>`__ provides a good starting point.


Rules
-----

Defining rules in lex2 is done through creating :py:class:`Rule` object instances. In addition to an identifiable name and regex pattern, each rule can be configured to be returned to the user by the lexer (on by default) or whether to be processed internally but not returned.

A good example when tokens should not be returned are comments in programming languages. Comments are always ignored and should therefore not be returned to the parser. However, it must be defined on how to recognize a comment in order for them to be skipped by the lexer.

.. code-block:: python3
    :caption: Instantiating a Rule object

    #                      identifier  regex  returns? (optional)
    #                       ┌───┴───┐ ┌──┴──┐  ┌─┴─┐
    number_rule = lex2.Rule("INTEGER", r"\d+", True)

    # You can inspect the identifier and regex pattern of the object, and change
    # the return behaviour property value
    number_rule.id
    >>> 'INTEGER'
    number_rule.regex
    >>> '\\d+'
    number_rule.returns
    >>> True
    number_rule.returns = False
    number_rule.returns
    >>> False

.. autoclass:: lex2.Rule

Rule Groups
-----------

If you find yourself writing boilerplate code to include or format parts of a regular expression, or just would like an abstraction layer altogether, you can opt to use the :py:class:`RuleGroup` base class. An example is given in the code block below.

.. code-block:: python3
    :caption: Creating a regular expression for specific e-mail domain addresses

    class AllowedEmail (lex2.RuleGroup):
        def __init__(self):
            super().__init__(
                "EMAIL",
                regex_prefix=r"(?i)\A[a-z\d_\-.]+"
            )

    #   Define a public method to add a regex group. It has to
    #   call the inherited protected method '_add_regex_group()'
    #   ┌──────────────────────┴────────────────────┐
        def add_provider(self, domain: str, tld: str):
            self._add_regex_group(fr'@{domain}\.{tld}')
            return self

    allowed_email = (AllowedEmail()
                        .add_provider("gmail",   "com")
                        .add_provider("hotmail", "com")
                        .rule())
    #                   └──┬──┘
    #   Compiles your group into a singular Rule object

    allowed_email.id
    >>> 'EMAIL'
    allowed_email.regex
    >>> '(?i)\A[a-z\d_\-.]+((@gmail\.com)|(@hotmail\.com))'

.. warning::
    By convention, your custom public methods should return themselves (``self``) so it's possible to have method chaining.

.. autoclass:: lex2.RuleGroup


Ruleset
-------

Finally, rulesets can be defined as standard lists populated with :py:class:`Rule` object instances. It is recommended to type-hint the list variable (if stored) with the :py:class:`RulesetType` type alias.

.. code-block:: python3
    :caption: Defining a ruleset

    ruleset: lex2.RulesetType = [
        lex2.Rule("WORD",        r"[a-zA-Z]+"),
        lex2.Rule("NUMBER",      r"[0-9]+"),
        lex2.Rule("PUNCTUATION", r"[.,:;!?\\-]")
    ]

.. note::
    If you intend to use multiple rulesets, that reuse earlier defined rules, it is better to store the :py:class:`Rule` instances into separate variables first and reference them in rulesets.
