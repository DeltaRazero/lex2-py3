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

    from lex2 import (
        IMatcher
    )

# ***************************************************************************************

class BaseMatcher (__.IMatcher, metaclass=__.abc.ABCMeta):
    """Abstract base class of an IMatcher implementation.
    """

  # --- PROTECTED FIELDS --- #

    # Lexer implementation identifier string
    _implementationId : str


  # --- CONSTRUCTOR --- #

    @__.abc.abstractmethod
    def __init__(self) -> None:
        self._implementationId = ""
        return


  # --- GETTERS --- #

    def GetImplementationId(self) -> str:
        return self._implementationId
