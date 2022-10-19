"""Models for about panel."""
from dataclasses import dataclass

@dataclass
class Hardware:
    """Hardware class"""
    processor: str
    cores: int
    memory: float
    disk: float
    product_name: str
    vendor: str
    graphics: str

@dataclass
class Software:
    """Software class"""
    os_name: str
    os_type: str
    kernel: str
