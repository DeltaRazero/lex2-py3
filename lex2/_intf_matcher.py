"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    import abc

    from .misc import voidptr_t

# ***************************************************************************************

class IMatcher (metaclass=_.abc.ABCMeta):
    """Common interface to a rule matcher object instance.
    """

  # --- INTERFACE GETTERS --- #

    @_.abc.abstractmethod
    def GetVendorId(self) -> str:
        """Gets the lexer implementation identifier string (a.k.a. 'vendor ID').

        Returns
        -------
        str
        """
        pass


    @_.abc.abstractmethod
    def GetPatternMatcher(self) -> _.voidptr_t:
        """Gets the compiled regex pattern matcher object reference.

        Returns
        -------
        voidptr_t
            Reference to an implemented regex pattern matcher object. The return type is
            void* (t.Any) by design, as in a statically typed environment the developer
            of a lexer implementation should cast the object to the appropriate type.
        """
        pass
