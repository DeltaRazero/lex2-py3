"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc as _abc

from .misc import voidptr_t as _voidptr_t

# ***************************************************************************************

class IMatcher (metaclass=_abc.ABCMeta):
    """Common interface to a rule matcher object instance.
    """

  # --- INTERFACE GETTERS --- #

    @_abc.abstractmethod
    def GetVendorId(self) -> str:
        """Gets the lexer implementation identifier string (a.k.a. 'vendor ID').

        Returns
        -------
        str
        """
        pass


    @_abc.abstractmethod
    def GetPatternMatcher(self) -> _voidptr_t:
        """Gets the compiled regex pattern matcher object reference.

        Returns
        -------
        voidptr_t
            Reference to an implemented regex pattern matcher object. The return type is
            void* (t.Any) by design, as in a statically typed environment the developer
            of a lexer implementation should cast the object to the appropriate type.
        """
        pass
