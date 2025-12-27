import unittest
import json
import tempfile
from wallet_qr.styles import QRConfig, ColorScheme, StyleManager

class TestStyles(unittest.TestCase):
    
    def test_qr_config_defaults(self):
        """Test QRConfig default values"""
        config = QRConfig()
        
        self.assertEqual(config.version, 5)
        self.assertEqual(config.error_correction, "H")
        self.assertEqual(config.box_size, 12)
        self.assertEqual(config.border, 4)
        self.assertEqual(config.fill_color, "#2E86C1")
        self.assertEqual(config.back_color, "white")
        self.assertEqual(config.title, "CRYPTO WALLET")
    
    def test_qr_config_presets(self):
        """Test QRConfig presets"""
        presets = ["professional", "minimalist", "dark", "gradient", "business", "premium"]
        
        for preset in presets:
            config = QRConfig.from_preset(preset)
            self.assertIsInstance(config, QRConfig)
            
            # Verify preset-specific properties
            if preset == "professional":
                self.assertTrue(config.add_logo)
                self.assertTrue(config.show_address)
            elif preset == "minimalist":
                self.assertFalse(config.show_address)
                self.assertEqual(config.fill_color, "black")
            elif preset == "dark":
                self.assertEqual(config.back_color, "#1C2833")
    
    def test_color_schemes(self):
        """Test ColorScheme enum"""
        schemes = list(ColorScheme)
        
        self.assertGreater(len(schemes), 0)
        
        for scheme in schemes:
            self.assertIsInstance(scheme.hex_color, str)
            self.assertIsInstance(scheme.background, str)
            self.assertIsInstance(scheme.text_color, str)
            self.assertIsInstance(scheme.description, str)
            
            # Verify hex colors
            self.assertTrue(scheme.hex_color.startswith("#"))
            self.assertTrue(scheme.background.startswith("#") or scheme.background in ["white", "black"])
    
    def test_config_serialization(self):
        """Test QRConfig serialization to/from dict"""
        config = QRConfig.from_preset("professional")
        
        # Convert to dict
        config_dict = config.to_dict()
        
        # Convert back
        config_from_dict = QRConfig.from_dict(config_dict)
        
        # Verify they're equal
        self.assertEqual(config.version, config_from_dict.version)
        self.assertEqual(config.fill_color, config_from_dict.fill_color)
        self.assertEqual(config.title, config_from_dict.title)
    
    def test_style_manager(self):
        """Test StyleManager"""
        manager = StyleManager()
        
        # List styles
        styles = manager.list_styles()
        self.assertGreater(len(styles), 0)
        
        # Get style
        config = manager.get_style("professional")
        self.assertIsInstance(config, QRConfig)
        
        # Add custom style
        custom_config = QRConfig(title="CUSTOM WALLET")
        manager.add_style("custom", custom_config)
        
        self.assertIn("custom", manager.list_styles())
        
        # Save and load styles
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            manager.save_styles(temp_file)
            
            # Load into new manager
            new_manager = StyleManager()
            new_manager.load_styles(temp_file)
            
            self.assertIn("custom", new_manager.list_styles())
        finally:
            import os
            if os.path.exists(temp_file):
                os.remove(temp_file)

if __name__ == '__main__':
    unittest.main()