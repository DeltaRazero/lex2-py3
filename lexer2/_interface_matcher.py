"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc as _abc

from . import misc as _misc

# ***************************************************************************************

class IMatcher (metaclass=_abc.ABCMeta):
    """Common interface to a rule matcher object instance.
    """

  # --- INTERFACE METHODS --- #

    @_abc.abstractmethod
    def GetRuleId(self) -> str:
        """Gets the rule identifier string.

        Returns
        -------
        str
        """
        pass


    @_abc.abstractmethod
    def GetVendorId(self) -> str:
        """Gets the lexer implementation identifier string (a.k.a. 'vendor ID').

        Returns
        -------
        str
        """
        pass


    @_abc.abstractmethod
    def GetPatternMatcher(self) -> _misc.VoidPtr_t:
        """Gets the compiled regex pattern matcher object reference.

        Returns
        -------
        VoidPtr_t
            Reference to an implemented regex pattern matcher object. The return type is
            void* (t.Any) by design, as in a statically typed environment the developer
            of a lexer implementation should cast the object to the appropriate type.
        """
        pass
