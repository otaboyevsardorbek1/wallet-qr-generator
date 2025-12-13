#!/usr/bin/env python3
"""
Example 2: Batch QR code generation
"""

import os
import sys
import tempfile
import shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wallet_qr.generator import QRGenerator
from wallet_qr.styles import QRConfig
from wallet_qr.utils import ProgressBar

def main():
    print("🚀 Example 2: Batch QR Code Generation")
    print("=" * 60)
    
    # Create temporary directory for output
    temp_dir = tempfile.mkdtemp(prefix="wallet_qr_example_")
    print(f"Output directory: {temp_dir}")
    
    # Sample wallet addresses (different formats)
    wallet_addresses = [
        # Base64-like
        "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X",
        # Ethereum-like
        "0x742d35Cc6634C0532925a3b844Bc9e90a3b9e0a1",
        # Bitcoin-like
        "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq",
        # Litecoin-like
        "Lc7g9hUJ8GJgUPUg7nz9JN6bgh8J7hK9t8",
        # Solana-like
        "CiDwVBFgWV9E5MvXWoLgnEgn2hK7rJikbvfWavzAQz3",
        # Custom
        "TQz9qL2c8X6jF4mKp7nR3sV5wY8xZ2bG4dH6jK8"
    ]
    
    print(f"\n📊 Processing {len(wallet_addresses)} wallet addresses")
    print("-" * 60)
    
    # Configuration for batch generation
    config = QRConfig.from_preset("professional")
    config.title = "MULTI-WALLET QR"
    config.subtitle = "Batch Generated"
    
    # Create generator
    generator = QRGenerator(config)
    
    # Setup progress bar
    progress = ProgressBar(len(wallet_addresses), prefix='Generating:', suffix='Complete', length=40)
    
    def update_progress(current, total, address=None):
        progress.update()
        if address:
            print(f"   {current}/{total}: {address[:30]}...")
    
    print("\n🚀 Starting batch generation...")
    print("-" * 60)
    
    # Generate batch
    results = generator.generate_batch(
        wallet_addresses,
        temp_dir,
        progress_callback=update_progress
    )
    
    print("\n" + "=" * 60)
    print("✅ BATCH GENERATION COMPLETE!")
    print("=" * 60)
    
    # Print summary
    total_size = sum(r['size_bytes'] for r in results)
    avg_size = total_size / len(results) if results else 0
    
    print(f"\n📊 Summary:")
    print(f"   • Generated: {len(results)} QR codes")
    print(f"   • Total size: {total_size:,} bytes")
    print(f"   • Average size: {avg_size:,.0f} bytes")
    print(f"   • Output directory: {temp_dir}")
    
    # Show file list
    print(f"\n📁 Generated files:")
    for i, result in enumerate(results, 1):
        filename = os.path.basename(result['filepath'])
        size_kb = result['size_bytes'] / 1024
        print(f"   {i:2d}. {filename:30} ({size_kb:.1f} KB)")
    
    print("\n🔧 Next steps:")
    print("   1. Check the output directory")
    print("   2. Test QR codes with wallet apps")
    print("   3. Distribute to users/clients")
    
    # Ask if user wants to keep files
    keep = input("\nKeep generated files? (y/n): ").strip().lower()
    if keep != 'y':
        shutil.rmtree(temp_dir)
        print("🗑️  Temporary files cleaned up.")
    else:
        print(f"💾 Files kept in: {temp_dir}")

if __name__ == "__main__":
    main()