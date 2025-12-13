#!/usr/bin/env python3
"""
Example 3: Advanced customization
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wallet_qr.generator import QRGenerator
from wallet_qr.styles import QRConfig, ColorScheme
from wallet_qr.utils import print_banner, print_success, print_info

def create_gradient_qr():
    """Create QR code with gradient colors"""
    print("\n🎨 Gradient QR Code")
    print("-" * 40)
    
    wallet_address = "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X"
    
    config = QRConfig.from_preset("gradient")
    config.title = "GRADIENT WALLET"
    config.subtitle = "Colorful & Modern"
    config.custom_css = {"gradient": True, "gradient_name": "ocean"}
    
    generator = QRGenerator(config)
    result = generator.generate(wallet_address, "wallet_gradient_ocean.png")
    
    print_success(f"Generated: {result['filepath']}")
    return result

def create_premium_qr():
    """Create premium-style QR code"""
    print("\n💎 Premium QR Code")
    print("-" * 40)
    
    wallet_address = "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X"
    
    config = QRConfig.from_preset("premium")
    config.title = "GOLD WALLET"
    config.subtitle = "Premium Security"
    config.fill_color = "#D4AF37"  # Gold
    config.back_color = "#FFF8DC"  # Cornsilk
    config.watermark = "VERIFIED"
    
    generator = QRGenerator(config)
    result = generator.generate(wallet_address, "wallet_premium_gold.png")
    
    print_success(f"Generated: {result['filepath']}")
    return result

def create_business_qr():
    """Create business-style QR code with logo"""
    print("\n🏢 Business QR Code")
    print("-" * 40)
    
    wallet_address = "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X"
    
    config = QRConfig.from_preset("business")
    config.title = "CORPORATE WALLET"
    config.subtitle = "Official Business Address"
    config.fill_color = "#2C3E50"  # Dark blue
    config.add_logo = True
    
    # Note: In real usage, specify logo path
    # config.logo_path = "company_logo.png"
    
    generator = QRGenerator(config)
    result = generator.generate(wallet_address, "wallet_business.png")
    
    print_success(f"Generated: {result['filepath']}")
    print_info("Note: Add --logo path/to/logo.png for actual logo")
    return result

def create_minimalist_set():
    """Create minimalist QR codes in different colors"""
    print("\n🎯 Minimalist QR Codes (Color Set)")
    print("-" * 40)
    
    wallet_address = "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X"
    
    colors = [
        ("#E74C3C", "Red"),
        ("#2E86C1", "Blue"),
        ("#27AE60", "Green"),
        ("#8E44AD", "Purple"),
        ("#F39C12", "Orange")
    ]
    
    results = []
    
    for color, name in colors:
        config = QRConfig.from_preset("minimalist")
        config.fill_color = color
        config.box_size = 18  # Larger for minimalist
        
        generator = QRGenerator(config)
        filename = f"wallet_minimalist_{name.lower()}.png"
        
        result = generator.generate(wallet_address, filename)
        results.append(result)
        
        print_info(f"  {name}: {result['filepath']}")
    
    return results

def main():
    print_banner()
    print("\n🚀 Example 3: Advanced Customization Examples")
    print("=" * 60)
    
    print("\nThis example demonstrates advanced customization features.")
    print("Generating 5 different QR code styles...")
    
    # Create different styles
    results = []
    
    results.append(create_gradient_qr())
    results.append(create_premium_qr())
    results.append(create_business_qr())
    minimalist_results = create_minimalist_set()
    results.extend(minimalist_results)
    
    print("\n" + "=" * 60)
    print("🎉 ADVANCED EXAMPLES COMPLETE!")
    print("=" * 60)
    
    # Summary
    total_size = sum(r['size_bytes'] for r in results)
    
    print(f"\n📊 Summary:")
    print(f"   • Total QR codes: {len(results)}")
    print(f"   • Total size: {total_size:,} bytes")
    print(f"   • Styles: Gradient, Premium, Business, Minimalist (5 colors)")
    
    print("\n🎨 Generated styles include:")
    print("   1. Gradient colors with ocean theme")
    print("   2. Premium gold design with watermark")
    print("   3. Business style (add your own logo)")
    print("   4. Minimalist in 5 different colors")
    
    print("\n🔧 Tips for production use:")
    print("   • Use --error-correction H for maximum reliability")
    print("   • Test QR codes with multiple scanner apps")
    print("   • For print, use --size 8 or higher")
    print("   • Add your company logo with --logo option")

if __name__ == "__main__":
    main()