"""Miscellanous components."""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    import typing as t
    T = t.TypeVar('T')

# ***************************************************************************************

# Typedef to simulate pointer type
ptr_t = _.t.Union[_.T, None]

# Typedef to simulate void*
# voidptr_t = _t.Any
voidptr_t = _.t.Any
