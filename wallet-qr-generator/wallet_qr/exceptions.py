"""
Custom exceptions for Wallet QR Generator
"""

class WalletQRException(Exception):
    """Base exception for all Wallet QR errors"""
    pass

class InvalidAddressError(WalletQRException):
    """Raised when wallet address is invalid"""
    def __init__(self, address):
        super().__init__(f"Invalid wallet address: {address}")

class GenerationError(WalletQRException):
    """Raised when QR generation fails"""
    pass

class ConfigError(WalletQRException):
    """Raised when configuration is invalid"""
    pass

class FileError(WalletQRException):
    """Raised when file operations fail"""
    pass