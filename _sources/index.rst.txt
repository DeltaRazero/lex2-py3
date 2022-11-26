
=====================
|project| (|release|)
=====================

.. _wiki_url_lexical_analysis: https://en.wikipedia.org/wiki/Lexical_analysis
.. _wiki_url_regex: https://en.wikipedia.org/wiki/Regular_expression

lex2 is a library intended for `lexical analysis <_wiki_url_lexical_analysis>`__ (also called `tokenization <_wiki_url_lexical_analysis>`__). String analysis is performed using `regular expressions (regex) <wiki_url_regex_>`__ in user-defined rules. Some additional functions, such as dynamic ruleset stack, provide flexibility to some degree at runtime.

The library is written in platform independent pure Python3, and is portable (no usage of language-specific features) making it straightforward to port to other programming languages. Furthermore, the library is designed to enable the end-user to easily integrate any external regex engine of their choice through a simple to use unified interface.

----------

.. .. toctree:
..     :maxdepth: 2

..     Home <self>

.. toctree::
    :maxdepth: 2
    :caption: Library Guide

    docs/01_installing
    docs/02_defining_rulesets
    docs/03_lexer_usage
    docs/04_customizing_regex_engine
    docs/05_miscellaneous

.. toctree::
    :maxdepth: 2
    :caption: API Reference

    lex2 <_autosummary/lex2>
