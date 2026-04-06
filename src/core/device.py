# src/core/device.py
"""
Device-Konfiguration für AT32UC3A1512
- Device-Informationen
- Memory-Layout
- Programmier-Parameter
"""

from dataclasses import dataclass
from typing import List, Dict, Any

from ..config.constants import DEVICE, INTERFACE, PROGRAMMER


@dataclass
class MemoryRegion:
    """Beschreibt eine Memory-Region des Devices."""
    name: str
    address: int
    size: int
    description: str


@dataclass
class DeviceConfig:
    """Zentrale Device-Konfiguration."""
    
    # Device-Info
    device_name: str = DEVICE
    interface: str = INTERFACE
    programmer: str = PROGRAMMER
    
    # Memory-Layout
    flash_start: int = 0x80000000
    flash_size: int = 0x180000  # 1,5 MB
    user_page_start: int = 0x80800000
    user_page_size: int = 0x200  # 512 Bytes
    
    # Memory-Regionen
    memory_regions: List[MemoryRegion] = None
    
    def __post_init__(self):
        """Initialisiere Speicher-Regionen nach der Initialisierung."""
        if self.memory_regions is None:
            self.memory_regions = [
                MemoryRegion(
                    name="Flash",
                    address=self.flash_start,
                    size=self.flash_size,
                    description="Main Flash Memory (1.5 MB)"
                ),
                MemoryRegion(
                    name="User Page",
                    address=self.user_page_start,
                    size=self.user_page_size,
                    description="User Page (512 Bytes)"
                ),
            ]
    
    def get_memory_region(self, name: str) -> MemoryRegion:
        """Findet eine Memory-Region nach Name."""
        for region in self.memory_regions:
            if region.name.lower() == name.lower():
                return region
        raise ValueError(f"Memory Region '{name}' not found")
    
    def to_dict(self) -> Dict[str, Any]:
        """Exportiert die Konfiguration als Dictionary."""
        return {
            "device_name": self.device_name,
            "interface": self.interface,
            "programmer": self.programmer,
            "flash_start": hex(self.flash_start),
            "flash_size": hex(self.flash_size),
            "user_page_start": hex(self.user_page_start),
            "user_page_size": hex(self.user_page_size),
        }
    
    def __repr__(self) -> str:
        return (f"DeviceConfig(device={self.device_name}, "
                f"interface={self.interface}, "
                f"programmer={self.programmer})")


# Globale Standard-Konfiguration
DEFAULT_DEVICE = DeviceConfig()