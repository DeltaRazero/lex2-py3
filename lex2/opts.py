"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    import typing as t

# ***************************************************************************************

#struct
class SeperatorOptions:
    """Struct that defines processing options of a seperator token.

    Properties
    ----------
    ignore : bool
        Flag to specify whether processing of tokens of this seperator should be ignored.
        Defaults to False
    returnTokens : bool
        Flag to specify whether tokens of this seperator should be returned.
        Defaults to False
    """

    ignores : bool
    returns : bool


  # --- CONSTRUCTOR --- #

    def __init__(self):
        self.ignores = False
        self.returns = False
        return

# ***************************************************************************************

# Struct
class LexerOptions:
    """Struct to define processing options of a lexer.

    Properties
    ----------
    space : SeperatorOptions
        Options to specify how a SPACE seperator should be handled.
    tab : SeperatorOptions
        Options to specify how a TAB seperator should be handled.
    newline : SeperatorOptions
        Options to specify how a NEWLINE seperator should be handled.
    idReturns : Dict[str, bool]
        Map with <str, bool> keypairs to specify whether to return tokens from a rule
        which its identifier matches the key given as input.
    """

  # --- PROPERTIES --- #

    space   : SeperatorOptions
    tab     : SeperatorOptions
    newline : SeperatorOptions

    # Key should be the identifier string value of a Rule object. To check whether a
    # token should be returned or ignored, the map gets checked for existence of the
    # token's identifier string as key value.
    idReturns : _.t.Dict[str, bool]


  # --- CONSTRUCTOR --- #

    def __init__(self):

        self.space   = SeperatorOptions()
        self.tab     = SeperatorOptions()
        self.newline = SeperatorOptions()

        self.idReturns = {}

        return
