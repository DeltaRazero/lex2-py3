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
    """Abstract base class partially implementing IMatcher.
    """

    # :: PROTECTED PROPERTIES :: #

    # Unique identifier (UID) of the matcher implementation
    _uid : str


    # :: CONSTRUCTOR :: #

    @__.abc.abstractmethod
    def __init__(self) -> None:
        self._uid = ""
        return


    # :: GETTERS :: #

    def get_uid(self) -> str:
        return self._uid
