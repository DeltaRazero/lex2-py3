
.. py:currentmodule:: lex2

Lexer Usage
===========

Instantiation
-------------

A lexer object instance is created by using the library's :func:`make_lexer() <_.lex2.make_lexer>` factory function. It mimics the behaviour of *function templates* as found in languages (such as C++, C#, or Rust) and therefore needs two consecutive function calls for the following data:

#. Template parameters for setting a custom matcher and lexer implementation.
   |br|
   |i| These can generally be ignored, and should only be used if the default implementations are not adequate. See also: :ref:`Customizing Regex Engine`. |/i|
#. Generic initialization parameters supported by each lexer.

.. code-block:: python3
    :caption: Using the make_lexer() factory function

    ruleset: lex2.RulesetType = [
        #        Identifier     Regex pattern
        lex2.Rule("WORD",        r"[a-zA-Z]+"),
        lex2.Rule("NUMBER",      r"[0-9]+"),
        lex2.Rule("PUNCTUATION", r"[.,:;!?\\-]")
    ]

    options = lex2.LexerOptions()
    options.space.returns = True

    #                                   Both optional, but best
    #                                   practice to set ruleset
    #                                     ┌───────┴────────┐
    lexer: lex2.ILexer = lex2.make_lexer()(ruleset, options)

.. py:currentmodule:: _
.. py:function:: lex2.make_lexer(MATCHER_T, LEXER_T)(ruleset=None, options=<lex2.LexerOptions object>)

    .. autofunction_docstring:: lex2.make_lexer
.. py:currentmodule:: lex2


Textstream I/O
--------------

When a lexer is instantiated, it must first be given a stream of text data that it must process. For all lexers, this functionality is handled by the :py:mod:`textio` sub-package: the ``Textstream`` set of components handle the lower-level file/memory I/O management (i.e. reading contents into memory buffers exposed to the lexer), while the :class:`TextIO <lex2.textio.TextIO>` class and its corresponding interface :class:`ITextIO <lex2.textio.ITextIO>` are exposed to the user for top-level I/O management (i.e. opening/loading/closing streams).

*The UML class diagram below visualizes and summarizes the relationships between classes and interfaces just discussed.*

.. figure:: /diagrams/png/textio_structure.png
    :align: center
    :scale: 25%

    UML class diagram visualizing TextIO and Textstream inheritance

As discussed, the :class:`ITextIO <lex2.textio.ITextIO>` interface is what is exposed to the user, which is part of each lexer because of the inherited interface. Through the interface, already instanced string objects can be passed directly using the :meth:`load() <lex2.textio.ITextIO.load>` method; files can be read either in chunks or one large buffer with the :meth:`open() <lex2.textio.ITextIO.open>` method; streams are closed manually using the :meth:`close() <lex2.textio.ITextIO.close>` method.

.. code-block:: python3
    :caption: Using the ITextIO interface to manage opening/loading/closing streams

    lexer: lex2.ILexer = lex2.make_lexer()()

    lexer.open("/path/to/some/file.txt")
    # Note that opening a new stream automatically closes the previous stream
    lexer.load("Text data passed directly.")
    lexer.close()

.. autoclass:: lex2.textio.ITextIO


Iteration and Tokenization
--------------------------

Once a lexer is instantiated and prepared, the lexer's :meth:`get_next_token() <ILexer.get_next_token>` method is to be used to tokenize the input data. Whenever the method is called, the lexer will iterate through the textstream and return the next identifiable token it can find back to the caller. Once the end of data (EOD) is reached, the lexer will raise the :exc:`EOD <lex2.exc.EOD>` signal exception to let the caller know to break out of a main lexing loop.

Tokens are in the form of :py:class:`Token` class instances, and contain information about the token type, tokenized data, and position in the textstream (in the form of a :class:`TextPosition <lex2.textio.TextPosition>` class instance).

.. code-block:: python3
    :caption: Main lexing loop example

    ruleset: lex2.RulesetType = [
        lex2.Rule("WORD",        r"[a-zA-Z]+"),
        lex2.Rule("PUNCTUATION", r"[.,:;!?\\-]")
    ]

    lexer: lex2.ILexer = lex2.make_lexer()(ruleset)
    lexer.load("Some input data.")

    # Main loop
    token: lex2.Token
    while (1):

    #  Tries to find the next token in the textstream.
    #  A try/catch block is required at the same or
    #  higher level to catch the 'EOD' exception signal
    #  whenever the textstream is exhausted of data.
    #   ┌────────────────┴────────────────┐
        try: token = lexer.get_next_token()
        except lex2.excs.EOD:
            break

        info = [
             f"ln: {token.pos.ln +1}",
            f"col: {token.pos.col+1}",
            token.id,
            token.data,
        ]
        print("{: <8} {: <12} {: <15} {: <10}".format(*info))

    lexer.close()

.. code-block:: console

    >>> ln: 1    col: 1       WORD            Some
    >>> ln: 1    col: 6       WORD            input
    >>> ln: 1    col: 12      WORD            data
    >>> ln: 1    col: 16      PUNCTUATION     .

.. autoclass:: lex2.Token
.. autoclass:: lex2.textio.TextPosition


Token Validation
----------------

For the use-case of making a parser and creating abstract trees (AST), the token class includes the :meth:`is_rule() <lex2.Token.is_rule>` / :meth:`is_rule_oneof() <lex2.Token.is_rule_oneof>` and :meth:`validate_rule_oneof() <lex2.Token.validate_rule>` / :meth:`validate_rule() <lex2.Token.validate_oneof>` methods for checking and validating if a token matches an expected rule, by means of passing :py:class:`Rule` object instances.

.. code-block:: python3
    :caption: Token validation example

    class rules:
    word = lex2.Rule("WORD",        r"[a-zA-Z]+")
    punc = lex2.Rule("PUNCTUATION", r"[.,:;!?\\-]")
    ruleset = [word, punc]

    lexer: lex2.ILexer = lex2.make_lexer()(rules.ruleset)
    lexer.load("word")

    token: lex2.Token = lexer.get_next_token()
    token.validate_rule(rules.word)
    token.validate_rule(rules.punc)

.. code-block:: console

    >>> lex2.excs.UnexpectedTokenError: Unexpected token type "WORD" @ ln:1|col:1
    >>> Expected the following type(s): "PUNCTUATION", for the following data:
    >>>     "word"


Changing Lexer Behaviour
------------------------



.. autoclass:: lex2.ILexer




if wanting to use your own regex engine see: blah blah, or want to create your own lexer implementation (blah blah)






