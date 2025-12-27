"""
QR Code style definitions and templates
"""

from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any, List
from enum import Enum
import json

class ColorScheme(Enum):
    """Color scheme presets"""
    BLUE = ("#2E86C1", "#F8F9F9", "#2C3E50", "Professional blue theme")
    GREEN = ("#27AE60", "#F8F9F9", "#145A32", "Fresh green theme")
    RED = ("#E74C3C", "#FDF2F0", "#922B21", "Vibrant red theme")
    PURPLE = ("#8E44AD", "#F9F0FF", "#4A235A", "Royal purple theme")
    DARK = ("#27AE60", "#1C2833", "#BDC3C7", "Dark mode theme")
    GRADIENT = ("#FF6B6B", "#F8F9F9", "#2C3E50", "Gradient color theme")
    GOLD = ("#F39C12", "#FEF9E7", "#7D6608", "Premium gold theme")
    SILVER = ("#7F8C8D", "#F8F9F9", "#2C3E50", "Elegant silver theme")
    
    @property
    def hex_color(self):
        return self.value[0]
    
    @property
    def background(self):
        return self.value[1]
    
    @property
    def text_color(self):
        return self.value[2]
    
    @property
    def description(self):
        return self.value[3]

@dataclass
class QRConfig:
    """QR code configuration"""
    version: int = 5
    error_correction: str = "H"  # L, M, Q, H
    box_size: int = 12
    border: int = 4
    fill_color: str = "#2E86C1"
    back_color: str = "white"
    title: str = "CRYPTO WALLET"
    subtitle: str = ""
    show_address: bool = True
    show_qr_border: bool = True
    add_logo: bool = False
    logo_path: Optional[str] = None
    logo_size: int = 80
    watermark: str = ""
    custom_css: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_preset(cls, preset: str) -> 'QRConfig':
        """Create config from preset"""
        presets = {
            "professional": cls(
                version=5,
                error_correction="H",
                box_size=12,
                border=4,
                fill_color="#2E86C1",
                title="CRYPTO WALLET ADDRESS",
                subtitle="Secure Digital Asset Storage",
                show_address=True,
                show_qr_border=True,
                add_logo=True,
                logo_size=100
            ),
            "minimalist": cls(
                version=4,
                error_correction="Q",
                box_size=15,
                border=3,
                fill_color="black",
                title="",
                show_address=False,
                show_qr_border=False,
                add_logo=False
            ),
            "dark": cls(
                version=5,
                error_correction="H",
                box_size=10,
                border=4,
                fill_color="#27AE60",
                back_color="#1C2833",
                title="CRYPTO WALLET",
                subtitle="Scan to Transfer",
                show_address=True,
                show_qr_border=True,
                add_logo=False
            ),
            "gradient": cls(
                version=4,
                error_correction="H",
                box_size=12,
                border=3,
                fill_color="#FF6B6B",
                title="WALLET ADDRESS",
                subtitle="Digital Currency",
                show_address=True,
                show_qr_border=True,
                add_logo=False,
                custom_css={"gradient": True}
            ),
            "business": cls(
                version=6,
                error_correction="H",
                box_size=10,
                border=4,
                fill_color="#2C3E50",
                title="BUSINESS WALLET",
                subtitle="Official Corporate Address",
                show_address=True,
                show_qr_border=True,
                add_logo=True,
                logo_size=120
            ),
            "premium": cls(
                version=7,
                error_correction="H",
                box_size=14,
                border=6,
                fill_color="#F39C12",
                back_color="#FEF9E7",
                title="PREMIUM WALLET",
                subtitle="Gold Standard Security",
                show_address=True,
                show_qr_border=True,
                add_logo=True,
                logo_size=150,
                watermark="VERIFIED"
            )
        }
        
        if preset.lower() in presets:
            return presets[preset.lower()]
        
        # Default to professional if preset not found
        return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "version": self.version,
            "error_correction": self.error_correction,
            "box_size": self.box_size,
            "border": self.border,
            "fill_color": self.fill_color,
            "back_color": self.back_color,
            "title": self.title,
            "subtitle": self.subtitle,
            "show_address": self.show_address,
            "show_qr_border": self.show_qr_border,
            "add_logo": self.add_logo,
            "logo_path": self.logo_path,
            "logo_size": self.logo_size,
            "watermark": self.watermark,
            "custom_css": self.custom_css
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QRConfig':
        """Create config from dictionary"""
        return cls(**data)

@dataclass
class Layout:
    """Layout configuration"""
    width: int
    height: int
    padding: int = 40
    qr_position: Tuple[int, int] = (0, 0)
    title_position: Tuple[int, int] = (0, 0)
    subtitle_position: Tuple[int, int] = (0, 0)
    address_position: Tuple[int, int] = (0, 0)
    logo_position: Tuple[int, int] = (0, 0)
    watermark_position: Tuple[int, int] = (0, 0)
    
    @classmethod
    def auto(cls, qr_size: Tuple[int, int], config: QRConfig) -> 'Layout':
        """Auto-generate layout based on QR size and config"""
        qr_width, qr_height = qr_size
        
        # Calculate extra height for text elements
        height_extra = 40  # Base padding
        
        if config.title:
            height_extra += 60
        if config.subtitle:
            height_extra += 30
        if config.show_address:
            height_extra += 80
        if config.watermark:
            height_extra += 30
        
        padding = 40
        width = qr_width + padding * 2
        height = qr_height + padding * 2 + height_extra
        
        # Calculate positions
        qr_x = padding
        qr_y = padding + (60 if config.title else 20)
        
        title_y = 30
        subtitle_y = title_y + 40
        
        return cls(
            width=width,
            height=height,
            padding=padding,
            qr_position=(qr_x, qr_y),
            title_position=(padding, title_y),
            subtitle_position=(padding, subtitle_y),
            address_position=(padding, qr_y + qr_height + 20),
            logo_position=(width - padding - 50, 30),
            watermark_position=(width - padding - 100, height - 30)
        )

class StyleManager:
    """Manage and apply styles"""
    
    def __init__(self):
        self.styles = {}
        self._load_default_styles()
    
    def _load_default_styles(self):
        """Load default style presets"""
        self.styles = {
            name: QRConfig.from_preset(name)
            for name in ["professional", "minimalist", "dark", "gradient", "business", "premium"]
        }
    
    def get_style(self, name: str) -> Optional[QRConfig]:
        """Get style by name"""
        return self.styles.get(name.lower())
    
    def add_style(self, name: str, config: QRConfig):
        """Add custom style"""
        self.styles[name.lower()] = config
    
    def list_styles(self) -> List[str]:
        """List available styles"""
        return list(self.styles.keys())
    
    def save_styles(self, filepath: str):
        """Save styles to file"""
        styles_data = {
            name: config.to_dict()
            for name, config in self.styles.items()
        }
        
        with open(filepath, 'w') as f:
            json.dump(styles_data, f, indent=2)
    
    def load_styles(self, filepath: str):
        """Load styles from file"""
        with open(filepath, 'r') as f:
            styles_data = json.load(f)
        
        self.styles.update({
            name: QRConfig.from_dict(config_data)
            for name, config_data in styles_data.items()
        })