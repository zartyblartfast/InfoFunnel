"""Delivery output modules."""

from abc import ABC, abstractmethod
from typing import Any


class DeliveryBase(ABC):
    """Abstract base for digest delivery."""

    @abstractmethod
    def deliver(self, content: str, topic: str = "digest") -> bool:
        """Send the digest content. Returns True on success."""
        ...


class CLIDelivery(DeliveryBase):
    """Print digest to terminal."""

    def deliver(self, content: str, topic: str = "digest") -> bool:
        print(content)
        return True
