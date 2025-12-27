"""
Command Line Interface for Wallet QR Generator
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import textwrap

from generator import QRGenerator
from styles import QRConfig, ColorScheme, StyleManager
from utils import (
    validate_wallet_address, 
    create_output_dir, 
    save_config, 
    print_banner,
    print_success, 
    print_error, 
    print_warning,
    print_info,
    ProgressBar,
    clear_screen,
    get_terminal_width
)
from .exceptions import WalletQRException, InvalidAddressError # pyright: ignore[reportMissingImports]

class WalletQRCLI:
    """Professional CLI interface for Wallet QR Generator"""
    
    def __init__(self):
        self.parser = self._create_parser()
        self.style_manager = StyleManager()
        self.terminal_width = get_terminal_width()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create comprehensive argument parser"""
        
        parser = argparse.ArgumentParser(
            prog="walletqr",
            description="""🚀 Professional Crypto Wallet QR Code Generator
Create beautiful, production-ready QR codes for cryptocurrency wallets.""",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent("""
            📚 Examples:
              %(prog)s "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X"
              %(prog)s -a wallets.txt -s professional -c "#27AE60" -o my_qr_codes
              %(prog)s --batch config.json --style dark --size 8
              %(prog)s --interactive
            
            🎨 Available Styles: professional, minimalist, dark, gradient, business, premium
            
            📖 Documentation: https://github.com/username/wallet-qr-generator
            """)
        )
        
        # Input group
        input_group = parser.add_argument_group('📥 Input Options')
        input_mutex = input_group.add_mutually_exclusive_group()
        
        input_mutex.add_argument(
            'address',
            nargs='?',
            help='Single wallet address to encode'
        )
        
        input_mutex.add_argument(
            '-a', '--address-file',
            metavar='FILE',
            help='Text file containing wallet addresses (one per line)'
        )
        
        input_mutex.add_argument(
            '--batch',
            metavar='JSON_FILE',
            help='JSON configuration file for batch generation'
        )
        
        input_mutex.add_argument(
            '-i', '--interactive',
            action='store_true',
            help='Launch interactive mode'
        )
        
        # Output group
        output_group = parser.add_argument_group('📤 Output Options')
        output_group.add_argument(
            '-o', '--output',
            default='output',
            metavar='DIR',
            help='Output directory (default: output)'
        )
        
        output_group.add_argument(
            '--prefix',
            default='wallet',
            help='Filename prefix (default: wallet)'
        )
        
        output_group.add_argument(
            '--format',
            choices=['png', 'jpg', 'webp', 'all'],
            default='png',
            help='Output image format (default: png)'
        )
        
        output_group.add_argument(
            '--quality',
            type=int,
            choices=range(1, 101),
            default=95,
            help='Image quality 1-100 (default: 95)'
        )
        
        # Design group
        design_group = parser.add_argument_group('🎨 Design Options')
        design_group.add_argument(
            '-s', '--style',
            choices=['professional', 'minimalist', 'dark', 'gradient', 'business', 'premium'],
            default='professional',
            help='QR code style preset (default: professional)'
        )
        
        design_group.add_argument(
            '-c', '--color',
            default='#2E86C1',
            help='Primary color in hex format (default: #2E86C1)'
        )
        
        design_group.add_argument(
            '-bg', '--background',
            default='white',
            help='Background color in hex (default: white)'
        )
        
        design_group.add_argument(
            '--size',
            type=int,
            choices=range(1, 11),
            default=5,
            help='QR size level 1-10 (1=small, 10=large) (default: 5)'
        )
        
        design_group.add_argument(
            '--logo',
            help='Path to logo image to add to QR center'
        )
        
        design_group.add_argument(
            '--logo-size',
            type=int,
            default=100,
            help='Logo size in pixels (default: 100)'
        )
        
        design_group.add_argument(
            '--title',
            help='Custom title text'
        )
        
        design_group.add_argument(
            '--subtitle',
            help='Custom subtitle text'
        )
        
        design_group.add_argument(
            '--watermark',
            help='Watermark text to add to background'
        )
        
        # Advanced group
        advanced_group = parser.add_argument_group('⚙️ Advanced Options')
        advanced_group.add_argument(
            '--error-correction',
            choices=['L', 'M', 'Q', 'H'],
            default='H',
            help='Error correction level (default: H)'
        )
        
        advanced_group.add_argument(
            '--border',
            type=int,
            default=4,
            help='Border size in modules (default: 4)'
        )
        
        advanced_group.add_argument(
            '--no-address',
            action='store_true',
            help='Hide wallet address from QR image'
        )
        
        advanced_group.add_argument(
            '--no-border',
            action='store_true',
            help='Hide QR code border'
        )
        
        # Misc group
        misc_group = parser.add_argument_group('📊 Miscellaneous')
        misc_group.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Verbose output with detailed information'
        )
        
        misc_group.add_argument(
            '--quiet',
            action='store_true',
            help='Suppress all non-essential output'
        )
        
        misc_group.add_argument(
            '--version',
            action='store_true',
            help='Show version information and exit'
        )
        
        misc_group.add_argument(
            '--list-styles',
            action='store_true',
            help='List all available style presets and exit'
        )
        
        return parser
    
    def _print_version(self):
        """Print version information"""
        from wallet_qr import __version__, __author__, __license__
        
        version_info = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        Wallet QR Generator v{__version__}                   ║
║                                                          ║
║        Author: {__author__}                              ║
║        License: {__license__}                            ║
║        GitHub: https://github.com/username/wallet-qr-generator ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(version_info)
    
    def _list_styles(self):
        """List all available styles"""
        styles_info = """
╔══════════════════════════════════════════════════════════╗
║                     Available Styles                     ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  🎨 professional - Complete business-style QR with logo  ║
║  🎨 minimalist   - Clean, simple QR code only           ║
║  🎨 dark         - Dark mode with light QR              ║
║  🎨 gradient     - Color gradient background            ║
║  🎨 business     - Corporate style with official look   ║
║  🎨 premium      - Gold-standard premium design         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(styles_info)
        
        # Show color samples
        print("\n🎨 Color Presets:")
        for scheme in ColorScheme:
            print(f"  • {scheme.name.lower():12} - {scheme.value[3]}")
    
    def _load_addresses(self, filepath: str) -> List[str]:
        """Load addresses from text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                addresses = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            # Validate addresses
            valid_addresses = []
            invalid_count = 0
            
            for addr in addresses:
                is_valid, addr_type = validate_wallet_address(addr)
                if is_valid:
                    valid_addresses.append(addr)
                else:
                    invalid_count += 1
                    if self.args.verbose:
                        print_warning(f"Invalid address skipped: {addr[:50]}...")
            
            if invalid_count > 0 and not self.args.quiet:
                print_warning(f"Skipped {invalid_count} invalid addresses")
            
            return valid_addresses
            
        except FileNotFoundError:
            print_error(f"File not found: {filepath}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error reading file: {e}")
            sys.exit(1)
    
    def _load_batch_config(self, filepath: str) -> Dict[str, Any]:
        """Load batch configuration from JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            return config
            
        except FileNotFoundError:
            print_error(f"Config file not found: {filepath}")
            sys.exit(1)
        except json.JSONDecodeError:
            print_error(f"Invalid JSON in config file: {filepath}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error reading config: {e}")
            sys.exit(1)
    
    def _create_qr_config(self) -> QRConfig:
        """Create QRConfig from CLI arguments"""
        # Start with preset
        config = QRConfig.from_preset(self.args.style)
        
        # Override with CLI arguments
        config.fill_color = self.args.color
        config.back_color = self.args.background
        config.error_correction = self.args.error_correction
        config.border = self.args.border
        config.show_address = not self.args.no_address
        config.show_qr_border = not self.args.no_border
        config.add_logo = bool(self.args.logo)
        config.logo_path = self.args.logo
        config.logo_size = self.args.logo_size
        config.watermark = self.args.watermark
        
        # Size mapping
        size_map = {
            1: (2, 8), 2: (3, 10), 3: (4, 12), 4: (5, 14),
            5: (6, 16), 6: (7, 18), 7: (8, 20), 8: (9, 22),
            9: (10, 24), 10: (12, 26)
        }
        config.version, config.box_size = size_map.get(self.args.size, (6, 16))
        
        # Custom titles
        if self.args.title:
            config.title = self.args.title
        if self.args.subtitle:
            config.subtitle = self.args.subtitle
        
        # Gradient style special handling
        if self.args.style == "gradient":
            config.custom_css = {"gradient": True, "gradient_name": "sunset"}
        
        return config
    
    def _print_summary(self, addresses: List[str], config: QRConfig, output_dir: str):
        """Print generation summary"""
        if self.args.quiet:
            return
        
        summary = f"""
╔══════════════════════════════════════════════════════════╗
║                    Generation Summary                    ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  📊 Addresses: {len(addresses):<36} ║
║  🎨 Style: {self.args.style:<39} ║
║  🎯 Color: {config.fill_color:<38} ║
║  📁 Output: {output_dir:<37} ║
║  🖼️  Format: {self.args.format.upper():<38} ║
║  📐 Size: Level {self.args.size}/10 ({config.box_size}px)              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        
        print(summary)
        
        if self.args.verbose:
            print_info(f"QR Version: {config.version}")
            print_info(f"Error Correction: {config.error_correction}")
            print_info(f"Border: {config.border} modules")
            if config.add_logo:
                print_info(f"Logo: {config.logo_path}")
    
    def _run_interactive_mode(self):
        """Run interactive mode with menu"""
        clear_screen()
        print_banner()
        
        print("\n" + "=" * self.terminal_width)
        print("📱 INTERACTIVE MODE")
        print("=" * self.terminal_width)
        
        while True:
            print("\n1. 🎨 Generate Single QR Code")
            print("2. 📚 Generate Batch QR Codes")
            print("3. 🎯 Preview Style Templates")
            print("4. ⚙️  Configuration Wizard")
            print("5. 📖 Documentation")
            print("6. 🚪 Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self._interactive_single()
            elif choice == "2":
                self._interactive_batch()
            elif choice == "3":
                self._preview_styles()
            elif choice == "4":
                self._config_wizard()
            elif choice == "5":
                self._show_documentation()
            elif choice == "6":
                print_success("Goodbye! 👋")
                sys.exit(0)
            else:
                print_error("Invalid choice. Please try again.")
    
    def _interactive_single(self):
        """Interactive single QR generation"""
        clear_screen()
        print("🎨 Single QR Code Generation")
        print("=" * self.terminal_width)
        
        # Get wallet address
        address = input("\nEnter wallet address: ").strip()
        
        is_valid, addr_type = validate_wallet_address(address)
        if not is_valid:
            print_error(f"Invalid {addr_type} address. Please try again.")
            return
        
        # Style selection
        print("\n🎨 Select Style:")
        styles = ["professional", "minimalist", "dark", "gradient", "business", "premium"]
        for i, style in enumerate(styles, 1):
            print(f"  {i}. {style}")
        
        style_choice = input(f"\nChoose style (1-{len(styles)}): ").strip()
        try:
            style_idx = int(style_choice) - 1
            if 0 <= style_idx < len(styles):
                style = styles[style_idx]
            else:
                style = "professional"
        except:
            style = "professional"
        
        # Color selection
        print("\n🎯 Select Color (or enter custom hex):")
        for scheme in ColorScheme:
            print(f"  • {scheme.name.lower():10} - {scheme.value[3]}")
        
        color = input("\nEnter color name or hex code (default: #2E86C1): ").strip()
        if not color:
            color = "#2E86C1"
        
        # Create config
        config = QRConfig.from_preset(style)
        config.fill_color = color if color.startswith("#") else f"#{color}"
        
        # Generate
        output_dir = create_output_dir("output", "interactive")
        generator = QRGenerator(config)
        
        filename = f"qr_{style}_{address[:8]}.png"
        output_path = os.path.join(output_dir, filename)
        
        print("\n" + "=" * self.terminal_width)
        print("🚀 Generating QR Code...")
        
        try:
            result = generator.generate(address, output_path, show_info=True)
            print_success(f"QR code generated: {output_path}")
            print_info(f"Size: {result['size_formatted']}")
            print_info(f"Dimensions: {result['dimensions'][0]}x{result['dimensions'][1]}px")
            
            # Ask to open
            open_choice = input("\nOpen generated file? (y/n): ").strip().lower()
            if open_choice == 'y':
                import subprocess
                try:
                    if sys.platform == "win32":
                        os.startfile(output_path)
                    elif sys.platform == "darwin":
                        subprocess.run(["open", output_path])
                    else:
                        subprocess.run(["xdg-open", output_path])
                except:
                    pass
                    
        except Exception as e:
            print_error(f"Generation failed: {e}")
    
    def _preview_styles(self):
        """Preview different style templates"""
        clear_screen()
        print("🎯 Style Template Preview")
        print("=" * self.terminal_width)
        
        test_address = "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X"
        
        print("\nAvailable styles with sample configurations:")
        print("-" * 60)
        
        for style in ["professional", "minimalist", "dark", "gradient", "business", "premium"]:
            config = QRConfig.from_preset(style)
            print(f"\n🎨 {style.upper():12}")
            print(f"   Title: {config.title}")
            print(f"   Color: {config.fill_color}")
            print(f"   Background: {config.back_color}")
            print(f"   Logo: {'Yes' if config.add_logo else 'No'}")
            print(f"   Show Address: {'Yes' if config.show_address else 'No'}")
        
        print("\n" + "=" * self.terminal_width)
        input("Press Enter to continue...")
    
    def run(self, args=None):
        """Run the CLI application"""
        try:
            # Parse arguments
            self.args = self.parser.parse_args(args)
            
            # Handle special flags
            if self.args.version:
                self._print_version()
                sys.exit(0)
            
            if self.args.list_styles:
                self._list_styles()
                sys.exit(0)
            
            if self.args.interactive:
                self._run_interactive_mode()
                sys.exit(0)
            
            # Check if we have any input
            if not any([self.args.address, self.args.address_file, self.args.batch]):
                if not self.args.quiet:
                    print_banner()
                print_error("Error: No input specified. Use --help for usage information.")
                print_info("Tip: Use --interactive for guided mode.")
                sys.exit(1)
            
            # Print banner if not quiet
            if not self.args.quiet and not self.args.verbose:
                print_banner()
            
            # Load addresses
            addresses = []
            
            if self.args.batch:
                # Load from batch config
                config_data = self._load_batch_config(self.args.batch)
                addresses = config_data.get('addresses', [])
                # Could apply other config from batch file here
                
            elif self.args.address_file:
                # Load from address file
                addresses = self._load_addresses(self.args.address_file)
                
            else:
                # Single address
                is_valid, addr_type = validate_wallet_address(self.args.address)
                if is_valid:
                    addresses = [self.args.address]
                    if self.args.verbose:
                        print_info(f"Detected {addr_type} address format")
                else:
                    print_error(f"Invalid wallet address: {self.args.address}")
                    sys.exit(1)
            
            if not addresses:
                print_error("No valid addresses found")
                sys.exit(1)
            
            # Create configuration
            qr_config = self._create_qr_config()
            
            # Create output directory
            output_dir = create_output_dir(self.args.output, "qr_codes")
            
            # Print summary
            if not self.args.quiet:
                self._print_summary(addresses, qr_config, output_dir)
                print("\n" + "=" * self.terminal_width)
                print("🚀 Starting QR Code Generation...")
            
            # Create generator
            generator = QRGenerator(qr_config)
            
            # Generate QR codes
            if len(addresses) == 1:
                # Single generation
                filename = f"{self.args.prefix}_{qr_config.fill_color.replace('#', '')}.png"
                output_path = os.path.join(output_dir, filename)
                
                if not self.args.quiet:
                    progress = ProgressBar(1, prefix='Progress:', suffix='Complete', length=40)
                
                try:
                    result = generator.generate(addresses[0], output_path, show_info=self.args.verbose)
                    
                    if not self.args.quiet:
                        progress.update(1)
                        print_success(f"\n✅ QR code generated successfully!")
                        print_info(f"   File: {output_path}")
                        print_info(f"   Size: {result['size_formatted']}")
                        print_info(f"   Dimensions: {result['dimensions'][0]}x{result['dimensions'][1]}px")
                
                except Exception as e:
                    print_error(f"Generation failed: {e}")
                    sys.exit(1)
                    
            else:
                # Batch generation
                if not self.args.quiet:
                    progress = ProgressBar(len(addresses), prefix='Generating:', suffix='Complete', length=40)
                
                def update_progress(current, total, address=None):
                    if not self.args.quiet:
                        progress.update()
                    if self.args.verbose and address:
                        print_info(f"  Processing: {address[:40]}...")
                
                try:
                    results = generator.generate_batch(
                        addresses, 
                        output_dir,
                        progress_callback=update_progress
                    )
                    
                    if not self.args.quiet:
                        print_success(f"\n✅ Batch generation complete!")
                        print_info(f"   Generated: {len(results)} QR codes")
                        print_info(f"   Directory: {output_dir}")
                        
                        if self.args.verbose:
                            total_size = sum(r['size_bytes'] for r in results)
                            avg_size = total_size / len(results) if results else 0
                            print_info(f"   Total size: {format_file_size(total_size)}")
                            print_info(f"   Average size: {format_file_size(avg_size)}")
                
                except Exception as e:
                    print_error(f"Batch generation failed: {e}")
                    sys.exit(1)
            
            # Save configuration
            config_data = {
                "version": "1.0.0",
                "timestamp": output_dir.split("_")[-1],
                "address_count": len(addresses),
                "style": self.args.style,
                "color": qr_config.fill_color,
                "output_directory": output_dir,
                "config": qr_config.to_dict(),
                "generated_files": len(addresses)
            }
            
            config_file = save_config(config_data, output_dir)
            
            # Final message
            if not self.args.quiet:
                print("\n" + "=" * self.terminal_width)
                print("🎉 GENERATION COMPLETED SUCCESSFULLY!")
                print("=" * self.terminal_width)
                
                print(f"\n📁 Output Directory: {output_dir}")
                print(f"📄 Generated Files: {len(addresses)}")
                print(f"⚙️  Config File: {config_file}")
                
                print("\n🔧 Next Steps:")
                print("   1. Navigate to output directory")
                print("   2. Test QR codes with wallet app")
                print("   3. Share or print as needed")
                
                if self.args.style == "premium":
                    print("   💎 Premium style is best for business cards")
                elif self.args.style == "minimalist":
                    print("   🎯 Minimalist style is best for apps and websites")
                
                print("\n✅ All done! Your QR codes are ready to use.\n")
            
            return 0
            
        except KeyboardInterrupt:
            if not self.args.quiet:
                print("\n\n⚠️  Operation cancelled by user")
            return 130
        except Exception as e:
            if not self.args.quiet:
                print_error(f"Unexpected error: {e}")
            return 1

def main():
    """Entry point for CLI"""
    cli = WalletQRCLI()
    return cli.run()

if __name__ == "__main__":
    sys.exit(main())