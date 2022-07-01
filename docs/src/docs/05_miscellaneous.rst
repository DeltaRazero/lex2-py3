
.. py:currentmodule:: lex2

Miscellaneous
=============

This section contains some information on miscellaneous functionality of the library.


Profiling Order of Rules (Improving Performance)
------------------------------------------------

.. _url_redirection_operators: https://linuxize.com/post/bash-write-to-file/

Due to the design of the library, the lexer will try to match rules sequentially one at a time. In practice, this would mean a common rule that is put as last in a ruleset will cause slowdown compared to putting such a rule first.

The library includes another lexer built on top of the default lexer to provide some basic profiling on the input data, in order to more easily find an optimal order of rules.

The profiling lexer (:class:`ProfilerLexer <lex2.lexer.ProfilerLexer>`) can be used by simply defining it as class to the :func:`make_lexer() <_.lex2.make_lexer>` factory function. The profile information is shown either by manually calling the :func:`show_report() <lex2.lexer.ProfilerLexer.show_report>` method or by closing the lexer's textstream (also done automatically when the lexer is destroyed by garbage collection).

.. code-block:: python3
    :caption: Using the profiling lexer

    lexer: lex2.ILexer = lex2.make_lexer(LEXER_T=lex2.lexer.ProfilerLexer)(ruleset, options)

    ...

    # Manual call; you can set the occurrence threshold on showing values of a rule
    lexer: lex2.lexer.ProfilerLexer
    lexer.show_report(value_occurrence_threshold=10)

    # Automatically calls .show_report() if it wasn't already called manually
    lexer.close()


.. note::
    If you wish to write the output of :func:`show_report() <lex2.lexer.ProfilerLexer.show_report>` to a file, you can do so using redirection operators. See also `this page on how to redirect output to a file <_url_redirection_operators>`__.
