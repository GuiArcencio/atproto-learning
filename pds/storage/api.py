from abc import ABC, abstractmethod
from typing import Optional

from multiformats import CID

class BlockStorage(ABC):

    @abstractmethod
    def read(self, cid: CID) -> Optional[bytes]:
        pass

    @abstractmethod
    def write(self, content: bytes):
        pass