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

# Typedef to simulate pointer type
ptr_t = nullable = __.t.Optional

# Typedef to simulate void*
voidptr_t = __.t.Any
