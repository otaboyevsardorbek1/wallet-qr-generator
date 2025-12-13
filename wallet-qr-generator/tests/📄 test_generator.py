import unittest
import os
import tempfile
from PIL import Image

from wallet_qr.generator import QRGenerator
from wallet_qr.styles import QRConfig
from wallet_qr.utils import validate_wallet_address
from wallet_qr.exceptions import GenerationError

class TestQRGenerator(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_address = "UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X"
        self.temp_dir = tempfile.mkdtemp()
    
    def test_address_validation(self):
        """Test address validation"""
        # Valid addresses
        valid_cases = [
            ("0x1234567890abcdef1234567890abcdef12345678", "ethereum"),
            ("bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq", "bitcoin"),
            ("Lc7g9hUJ8GJgUPUg7nz9JN6bgh8J7hK9t8", "generic"),
            ("UQDe1kBdULQE3RBtE24jIZYDD7nPov5S-xM-PA3dCzGXHc7X", "base64"),
        ]
        
        for address, expected_type in valid_cases:
            is_valid, detected_type = validate_wallet_address(address)
            self.assertTrue(is_valid, f"Address should be valid: {address}")
        
        # Invalid addresses
        invalid_cases = [
            "",
            "short",
            "address with spaces",
            "0xinvalid",
        ]
        
        for address in invalid_cases:
            is_valid, _ = validate_wallet_address(address)
            self.assertFalse(is_valid, f"Address should be invalid: {address}")
    
    def test_qr_generation_basic(self):
        """Test basic QR generation"""
        config = QRConfig()
        generator = QRGenerator(config)
        
        output_file = os.path.join(self.temp_dir, "test_qr.png")
        
        # Generate QR
        result = generator.generate(self.test_address, output_file)
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_file))
        
        # Verify image properties
        with Image.open(output_file) as img:
            self.assertEqual(img.format, 'PNG')
            self.assertGreater(img.width, 0)
            self.assertGreater(img.height, 0)
    
    def test_qr_generation_different_styles(self):
        """Test generation with different style presets"""
        styles = ["professional", "minimalist", "dark", "gradient"]
        
        for style in styles:
            config = QRConfig.from_preset(style)
            generator = QRGenerator(config)
            
            output_file = os.path.join(self.temp_dir, f"test_{style}.png")
            
            try:
                result = generator.generate(self.test_address, output_file)
                self.assertTrue(os.path.exists(output_file))
            except Exception as e:
                self.fail(f"Failed to generate {style} style: {e}")
    
    def test_batch_generation(self):
        """Test batch QR generation"""
        addresses = [
            self.test_address,
            "0x1234567890abcdef1234567890abcdef12345678",
            "bc1qtestaddress1234567890abcdefghijklmnopq"
        ]
        
        config = QRConfig()
        generator = QRGenerator(config)
        
        # Generate batch
        results = generator.generate_batch(addresses, self.temp_dir)
        
        # Verify results
        self.assertEqual(len(results), len(addresses))
        
        for result in results:
            self.assertTrue(os.path.exists(result['filepath']))
            self.assertIn('size_bytes', result)
            self.assertIn('dimensions', result)
    
    def test_invalid_config(self):
        """Test generation with invalid configuration"""
        config = QRConfig(version=1, box_size=0)  # Invalid config
        generator = QRGenerator(config)
        
        output_file = os.path.join(self.temp_dir, "test_invalid.png")
        
        # Should raise GenerationError
        with self.assertRaises(GenerationError):
            generator.generate(self.test_address, output_file)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()