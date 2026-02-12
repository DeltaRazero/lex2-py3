"""<internal>"""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ******************************************************************************

class __:
  '<imports>'

  import abc

  from lex2 import (
    MatcherInterface,
  )

# ******************************************************************************

class MatcherBase (__.MatcherInterface, __.abc.ABC):
  """Abstract base class partially implementing MatcherInterface.
  """

  # :: CONSTRUCTOR :: #

  @__.abc.abstractmethod
  def __init__(self) -> None:
    return

  # :: GETTERS :: #

  @staticmethod
  @__.abc.abstractmethod
  def uid() -> str:
    """Gets the unique identifier of the matcher implementation.

    Returns
    -------
    str
    """
    ...

  def get_uid(self) -> str:
    return self.uid()
