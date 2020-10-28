"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import enum   as _enum
import typing as _t

from . import _rule

# ***************************************************************************************

# Enum
class HFlag (_enum.Enum):
    """Enum flag values to specify handling of a token.

    Values
    ------
    HANDLE_AND_RETURN
        A lexer will handle the token type and return it to the user.
        If this flag value is set the the 'unknownToken' type, a lexer will throw a
        `UnknownTokenException` in which information about the unknown token type can be
        retrieved from its object properties. The token data will be the every character
        until a SPACE, TAB or NEWLINE character is encountered.
    HANDLE_AND_IGNORE
        A lexer will handle the token type internally but does NOT return it to the user.
        Instead, the lexer will return the next token type that has its HFlag value set
        to `HANDLE_AND_RETURN`.
        If this flag value is set the the 'unknownToken' type, a lexer will NOT throw an
        `UnknownTokenException` and continue finding a new token after it encounters a
        SPACE, TAB or NEWLINE character.
    """

    # Internally processes the token:
    #  * Returns the token when known
    #  * Throws an exception when unknown token
    HANDLE_AND_RETURN = _enum.auto()

    # Internally processes the token, but does not return it
    HANDLE_AND_IGNORE = _enum.auto()

# ***************************************************************************************

# Struct
class HFlags:
    """Struct to define how token types are handled by setting their HFlag value.

    Properties
    ----------
    space : HFlag
        HFlag to define how SPACE characters are handled.
        Defaults to HFlag.HANDLE_AND_IGNORE
    tab : HFlag
        HFlag to define how TAB characters are handled.
        Defaults to HFlag.HANDLE_AND_IGNORE
    newline : HFlag
        HFlag to define how NEWLINE characters are handled.
        Defaults to HFlag.HANDLE_AND_IGNORE
    comment : HFlag
        HFlag to define how comment tokens are handled.
        Defaults to HFlag.HANDLE_AND_IGNORE
    unknownToken : HFlag
        HFlag to define how tokens with unknown type are handled.
        Defaults to HFlag.HANDLE_AND_RETURN
    userFlags : t.Dict[Rule, HFlag]
        Map of <Rule, HFlag> keypair to define how user-defined tokens are handled.
    """

  # --- PROPERTIES --- #

    space   : HFlag
    tab     : HFlag
    newline : HFlag

    comment : HFlag

    unknownToken : HFlag

    # Key is a Rule object instance. A lexer will request its rule id when comparing to
    # a token instance.
    userFlags : _t.Dict[_rule.Rule, HFlag] = {}


  # --- CONSTRUCTOR --- #

    def __init__(self):

        self.space   = HFlag.HANDLE_AND_IGNORE
        self.tab     = HFlag.HANDLE_AND_IGNORE
        self.newline = HFlag.HANDLE_AND_IGNORE

        self.comment = HFlag.HANDLE_AND_IGNORE

        self.unknownToken = HFlag.HANDLE_AND_RETURN

        self.userFlags = {}

        return
