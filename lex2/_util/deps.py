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
    module = __.importlib.util.find_spec(module_name)
    return module is not None
