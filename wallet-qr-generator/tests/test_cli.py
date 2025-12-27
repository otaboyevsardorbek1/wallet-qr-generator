import unittest
import tempfile
import os
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

from wallet_qr.cli import WalletQRCLI

class TestCLI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.cli = WalletQRCLI()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_cli_help(self):
        """Test CLI help output"""
        # Capture help output
        with redirect_stdout(StringIO()) as stdout:
            try:
                self.cli.run(["--help"])
            except SystemExit:
                pass
        
        output = stdout.getvalue()
        self.assertIn("usage:", output)
        self.assertIn("Wallet QR Generator", output)
    
    def test_cli_version(self):
        """Test CLI version output"""
        with redirect_stdout(StringIO()) as stdout:
            try:
                self.cli.run(["--version"])
            except SystemExit:
                pass
        
        output = stdout.getvalue()
        self.assertIn("Wallet QR Generator", output)
        self.assertIn("v1.0.0", output)
    
    def test_cli_list_styles(self):
        """Test CLI list-styles output"""
        with redirect_stdout(StringIO()) as stdout:
            try:
                self.cli.run(["--list-styles"])
            except SystemExit:
                pass
        
        output = stdout.getvalue()
        self.assertIn("Available Styles", output)
        self.assertIn("professional", output)
        self.assertIn("minimalist", output)
    
    def test_cli_invalid_address(self):
        """Test CLI with invalid address"""
        with redirect_stderr(StringIO()) as stderr:
            try:
                self.cli.run(["invalid_address"])
            except SystemExit as e:
                self.assertNotEqual(e.code, 0)
        
        error_output = stderr.getvalue()
        self.assertIn("Invalid wallet address", error_output)
    
    def test_cli_valid_address(self):
        """Test CLI with valid address (dry run)"""
        # Create a temporary output directory
        temp_output = os.path.join(self.temp_dir, "test_output")
        
        with redirect_stdout(StringIO()) as stdout:
            with redirect_stderr(StringIO()) as stderr:
                try:
                    # Use --quiet to suppress banner
                    self.cli.run([
                        "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X",
                        "--quiet",
                        "--output", temp_output,
                        "--no-address"  # Simpler generation for test
                    ])
                except SystemExit as e:
                    # CLI should exit with 0 on success
                    self.assertEqual(e.code, 0)
    
    def test_cli_with_address_file(self):
        """Test CLI with address file"""
        # Create temporary address file
        address_file = os.path.join(self.temp_dir, "addresses.txt")
        
        with open(address_file, "w") as f:
            f.write("UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X\n")
            f.write("0x1234567890abcdef1234567890abcdef12345678\n")
        
        temp_output = os.path.join(self.temp_dir, "test_batch_output")
        
        with redirect_stdout(StringIO()) as stdout:
            with redirect_stderr(StringIO()) as stderr:
                try:
                    self.cli.run([
                        "--address-file", address_file,
                        "--quiet",
                        "--output", temp_output,
                        "--no-address"
                    ])
                except SystemExit as e:
                    self.assertEqual(e.code, 0)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()