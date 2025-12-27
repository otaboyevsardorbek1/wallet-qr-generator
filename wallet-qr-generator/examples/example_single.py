#!/usr/bin/env python3
"""
Example 1: Generate single QR code
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wallet_qr.generator import QRGenerator
from wallet_qr.styles import QRConfig

def main():
    print("🚀 Example 1: Single QR Code Generation")
    print("=" * 60)
    
    # Your wallet address
    wallet_address = "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X"
    
    print(f"Wallet Address: {wallet_address}")
    print(f"Address Type: Base64-like format")
    print("-" * 60)
    
    # Option 1: Professional style
    print("\n1. Professional Style QR")
    print("-" * 40)
    
    config = QRConfig.from_preset("professional")
    config.title = "MY CRYPTO WALLET"
    config.subtitle = "Secure Digital Assets"
    
    generator = QRGenerator(config)
    result = generator.generate(wallet_address, "wallet_professional.png")
    
    print(f"✅ Generated: {result['filepath']}")
    print(f"   Size: {result['size_formatted']}")
    print(f"   Dimensions: {result['dimensions'][0]}x{result['dimensions'][1]}")
    
    # Option 2: Dark mode
    print("\n2. Dark Mode QR")
    print("-" * 40)
    
    config = QRConfig.from_preset("dark")
    config.title = "DARK WALLET"
    config.fill_color = "#9B59B6"  # Purple
    
    generator = QRGenerator(config)
    result = generator.generate(wallet_address, "wallet_dark.png")
    
    print(f"✅ Generated: {result['filepath']}")
    
    # Option 3: Custom design
    print("\n3. Custom Design QR")
    print("-" * 40)
    
    config = QRConfig(
        version=6,
        error_correction="H",
        box_size=15,
        border=4,
        fill_color="#E74C3C",  # Red
        back_color="#FDEDEC",  # Light red background
        title="RED WALLET",
        subtitle="Hot Wallet for Trading",
        show_address=True,
        show_qr_border=True,
        add_logo=False,
        watermark="SECURE"
    )
    
    generator = QRGenerator(config)
    result = generator.generate(wallet_address, "wallet_custom.png")
    
    print(f"✅ Generated: {result['filepath']}")
    
    print("\n" + "=" * 60)
    print("🎉 All examples completed!")
    print("Check the current directory for generated QR codes.")
    print("\nNext steps:")
    print("  1. Scan QR codes with your wallet app")
    print("  2. Test with different addresses")
    print("  3. Customize colors and styles")

if __name__ == "__main__":
    main()