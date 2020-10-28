"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import typing as _t
_T = _t.TypeVar('T')  #type: ignore

# ***************************************************************************************

# Typedef to simulate void*
VoidPtr_t = _t.Any

# Typedef to simulate pointer type
Ptr_t = _t.Union[_T, None]
