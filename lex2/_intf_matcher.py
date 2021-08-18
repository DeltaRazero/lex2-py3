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

    from . import textio
    from .misc import ptr_t

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
    def Match(self, ts: _.textio.ITextstream) -> _.ptr_t[str]:
        """Looks for a pattern match and returns string data in case of a match.

        Returns
        -------
        ptr_t[str]
            Nullable string object. Contains string data in case of a match, otherwise
            NULL/None.
        """
        pass
