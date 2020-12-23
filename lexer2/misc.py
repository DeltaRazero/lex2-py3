"""Miscellanous components."""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import typing as _t
T = _t.TypeVar('T')

# ***************************************************************************************

# Typedef to simulate pointer type
ptr_t = _t.Union[T, None]

# Typedef to simulate void*
# voidptr_t = _t.Any
voidptr_t = ptr_t[_t.Any]
