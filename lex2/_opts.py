"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import typing as t

# ***************************************************************************************

# Struct
class LexerOptions:
    """Struct to define processing options of a lexer."""

    # :: NESTED CLASSES :: #

    #struct
    class SeparatorOptions:
        """Struct that defines processing options of a separator token."""

        __slots__ = ('ignored', 'returns')

        ignored : bool
        """Flag to specify whether processing of tokens of this separator should be ignored.
           Defaults to ``False``
        """

        returns : bool
        """Flag to specify whether tokens of this separator should be returned.
           Defaults to ``False``
        """

        # :: CONSTRUCTOR :: #

        def __init__(self):
            self.ignored = False
            self.returns = False
            return

    __slots__ = ('space', 'tab', 'newline', 'id_returns')

    # :: PUBLIC ATTRIBUTES :: #

    space   : SeparatorOptions
    """Options to specify how a SPACE separator should be handled."""
    tab     : SeparatorOptions
    """Options to specify how a TAB separator should be handled."""
    newline : SeparatorOptions
    """Options to specify how a NEWLINE separator should be handled."""

    # Key should be the identifier string value of a Rule object. To check whether a
    # token should be returned or ignored, the map gets checked for existence of the
    # token's identifier string as key value.
    id_returns : __.t.Dict[str, bool]
    """Map with <str, bool> key-pairs to specify whether to return tokens from a rule
       which its identifier matches the key given as input.
    """


    # :: CONSTRUCTOR :: #

    def __init__(self):

        self.space   = self.SeparatorOptions()
        self.tab     = self.SeparatorOptions()
        self.newline = self.SeparatorOptions()

        self.id_returns = {}

        return
