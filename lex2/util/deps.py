"""Dependency checking."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import importlib.util

# ***************************************************************************************

def is_module_installed(module_name: str) -> bool:
    """Checks whether a specified module is installed.

    Parameters
    ----------
    module_name : str
        Name of the module.

    Returns
    -------
    bool
    """
    module = __.importlib.util.find_spec(module_name)
    return module is not None
