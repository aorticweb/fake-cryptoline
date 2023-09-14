from abc import ABC, abstractmethod
from typing import List

from bot.models.price import PairPrice


class BaseClient(ABC):
    """Base client for decentralized apis client"""

    @abstractmethod
    def markets(self) -> List[PairPrice]:
        pass
