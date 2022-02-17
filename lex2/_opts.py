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

  # --- NESTED CLASSES --- #

    #struct
    class SeperatorOptions:
        """Struct that defines processing options of a seperator token.

        Properties
        ----------
        ignored : bool
            Flag to specify whether processing of tokens of this seperator should be ignored.
            Defaults to False
        returns : bool
            Flag to specify whether tokens of this seperator should be returned.
            Defaults to False
        """

        ignored : bool
        returns : bool


      # --- CONSTRUCTOR --- #

        def __init__(self):
            self.ignores = False
            self.returns = False
            return


  # --- PROPERTIES --- #

    space   : SeperatorOptions
    tab     : SeperatorOptions
    newline : SeperatorOptions

    # Key should be the identifier string value of a Rule object. To check whether a
    # token should be returned or ignored, the map gets checked for existence of the
    # token's identifier string as key value.
    idReturns : __.t.Dict[str, bool]


  # --- CONSTRUCTOR --- #

    def __init__(self):

        self.space   = LexerOptions.SeperatorOptions()
        self.tab     = LexerOptions.SeperatorOptions()
        self.newline = LexerOptions.SeperatorOptions()

        self.idReturns = {}

        return
