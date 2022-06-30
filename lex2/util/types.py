"""Variable types (for type hinting)."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import typing as t
    T = t.TypeVar('T')

# ***************************************************************************************

PtrType = Nullable = __.t.Optional
"""Typedef to simulate pointer type."""

VoidptrType = __.t.Any
"""Typedef to simulate void pointer type (`void*`)."""
