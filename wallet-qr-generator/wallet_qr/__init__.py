"""
Crypto Wallet QR Generator
Professional CLI tool for creating beautiful wallet QR codes.
"""

__version__ = "1.0.0"
__author__ = "CryptoQR Team"
__email__ = "support@cryptoqr.dev"
__license__ = "MIT"
__url__ = "https://github.com/username/wallet-qr-generator"

from .generator import QRGenerator
from .styles import QRConfig, ColorScheme, Layout
from .exceptions import WalletQRException, InvalidAddressError, GenerationError
from .utils import validate_wallet_address, create_output_dir

__all__ = [
    'QRGenerator',
    'QRConfig',
    'ColorScheme',
    'Layout',
    'WalletQRException',
    'InvalidAddressError',
    'GenerationError',
    'validate_wallet_address',
    'create_output_dir',
]