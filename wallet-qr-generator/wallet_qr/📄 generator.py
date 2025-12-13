"""
Main QR code generation engine
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path
import numpy as np

from .styles import QRConfig, Layout, ColorScheme
from .utils import ProgressBar, generate_filename, format_file_size
from .exceptions import GenerationError

class QRGenerator:
    """Professional QR code generator with advanced features"""
    
    def __init__(self, config: Optional[QRConfig] = None):
        self.config = config or QRConfig()
        self.font_cache = {}
        self.gradients = {
            "sunset": [(255, 107, 107), (255, 167, 38), (255, 193, 7)],
            "ocean": [(41, 128, 185), (52, 152, 219), (93, 173, 226)],
            "forest": [(39, 174, 96), (46, 204, 113), (88, 214, 141)],
            "royal": [(142, 68, 173), (155, 89, 182), (165, 105, 189)],
            "fire": [(231, 76, 60), (235, 152, 78), (241, 196, 15)]
        }
    
    def _load_font(self, size: int, bold: bool = False, italic: bool = False) -> Optional[ImageFont.FreeTypeFont]:
        """Load font with comprehensive fallbacks"""
        cache_key = f"{size}_{bold}_{italic}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        # Try different font paths
        font_paths = []
        
        if bold and italic:
            font_paths.extend([
                "arialbi.ttf", "Arial Bold Italic.ttf",
                "/System/Library/Fonts/Arial Bold Italic.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"
            ])
        elif bold:
            font_paths.extend([
                "arialbd.ttf", "Arial Bold.ttf",
                "/System/Library/Fonts/Arial Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            ])
        elif italic:
            font_paths.extend([
                "ariali.ttf", "Arial Italic.ttf",
                "/System/Library/Fonts/Arial Italic.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
            ])
        else:
            font_paths.extend([
                "arial.ttf", "Arial.ttf",
                "/System/Library/Fonts/Arial.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
            ])
        
        # Also try system fonts
        system_fonts = [
            "DejaVuSans.ttf", "LiberationSans-Regular.ttf",
            "Ubuntu-R.ttf", "Roboto-Regular.ttf"
        ]
        
        font_paths.extend(system_fonts)
        
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, size)
                    self.font_cache[cache_key] = font
                    return font
            except:
                continue
        
        # Final fallback
        font = ImageFont.load_default()
        self.font_cache[cache_key] = font
        return font
    
    def _create_base_qr(self, data: str) -> Image.Image:
        """Create base QR code image with error correction"""
        try:
            # Map error correction string to constant
            ec_map = {
                "L": qrcode.constants.ERROR_CORRECT_L,
                "M": qrcode.constants.ERROR_CORRECT_M,
                "Q": qrcode.constants.ERROR_CORRECT_Q,
                "H": qrcode.constants.ERROR_CORRECT_H
            }
            
            qr = qrcode.QRCode(
                version=self.config.version,
                error_correction=ec_map.get(self.config.error_correction, 
                                           qrcode.constants.ERROR_CORRECT_H),
                box_size=self.config.box_size,
                border=self.config.border,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            return qr.make_image(fill_color=self.config.fill_color, 
                               back_color=self.config.back_color).convert("RGB")
            
        except Exception as e:
            raise GenerationError(f"Failed to create base QR code: {e}")
    
    def _create_gradient_qr(self, data: str) -> Image.Image:
        """Create QR code with gradient colors"""
        try:
            qr = qrcode.QRCode(
                version=self.config.version,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=self.config.box_size,
                border=self.config.border,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Get QR matrix
            matrix = qr.get_matrix()
            
            # Create blank image
            size = len(matrix) * self.config.box_size + 2 * self.config.border * self.config.box_size
            img = Image.new("RGB", (size, size), self.config.back_color)
            draw = ImageDraw.Draw(img)
            
            # Choose gradient
            gradient_name = self.config.custom_css.get("gradient_name", "sunset")
            gradient_colors = self.gradients.get(gradient_name, self.gradients["sunset"])
            
            # Draw QR with gradient
            for y in range(len(matrix)):
                for x in range(len(matrix)):
                    if matrix[y][x]:
                        # Calculate gradient color based on position
                        color_idx = (x + y) % len(gradient_colors)
                        color = gradient_colors[color_idx]
                        
                        # Draw box
                        x_pos = self.config.border * self.config.box_size + x * self.config.box_size
                        y_pos = self.config.border * self.config.box_size + y * self.config.box_size
                        
                        draw.rectangle(
                            [x_pos, y_pos, 
                             x_pos + self.config.box_size, 
                             y_pos + self_config.box_size],
                            fill=color,
                            outline=color
                        )
            
            return img
            
        except Exception as e:
            raise GenerationError(f"Failed to create gradient QR code: {e}")
    
    def _add_logo(self, qr_img: Image.Image) -> Image.Image:
        """Add logo to QR code center with effects"""
        if not self.config.add_logo or not self.config.logo_path:
            return qr_img
        
        try:
            if not os.path.exists(self.config.logo_path):
                print(f"Warning: Logo file not found: {self.config.logo_path}")
                return qr_img
            
            logo = Image.open(self.config.logo_path).convert("RGBA")
            
            # Resize logo
            logo_size = self.config.logo_size
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Create circular mask for logo with shadow
            mask_size = logo_size + 4
            mask = Image.new("L", (mask_size, mask_size), 0)
            draw = ImageDraw.Draw(mask)
            
            # Draw shadow (slightly larger circle)
            draw.ellipse((2, 2, mask_size-2, mask_size-2), fill=100)
            
            # Draw main circle
            draw.ellipse((0, 0, logo_size, logo_size), fill=255)
            
            # Create logo with white background
            logo_bg = Image.new("RGBA", (mask_size, mask_size), (255, 255, 255, 0))
            logo_pos = ((mask_size - logo_size) // 2, (mask_size - logo_size) // 2)
            logo_bg.paste(logo, logo_pos, logo)
            
            # Paste logo on QR code
            qr_size = qr_img.size[0]
            pos = ((qr_size - mask_size) // 2, (qr_size - mask_size) // 2)
            
            # Create composite
            qr_img.paste(logo_bg, pos, mask)
            
            return qr_img
            
        except Exception as e:
            print(f"Warning: Could not add logo: {e}")
            return qr_img
    
    def _create_background(self, size: Tuple[int, int], style: str = "gradient") -> Image.Image:
        """Create stylish background"""
        width, height = size
        
        if style == "gradient":
            # Create vertical gradient
            base = Image.new('RGB', (width, height), (255, 255, 255))
            
            for y in range(height):
                # Gradient from light to slightly darker
                r = int(248 - (y / height) * 20)
                g = int(249 - (y / height) * 30)
                b = int(249 - (y / height) * 40)
                
                for x in range(width):
                    # Add slight horizontal variation
                    variation = int((x / width) * 10)
                    base.putpixel((x, y), (min(255, r + variation), 
                                          min(255, g + variation), 
                                          min(255, b + variation)))
            
            # Apply subtle blur
            base = base.filter(ImageFilter.GaussianBlur(radius=0.5))
            return base
            
        elif style == "noise":
            # Create subtle noise texture
            base = Image.new('RGB', (width, height), (245, 245, 245))
            noise = np.random.randint(240, 250, (height, width, 3), dtype=np.uint8)
            noise_img = Image.fromarray(noise, 'RGB')
            
            # Blend with base
            return Image.blend(base, noise_img, alpha=0.3)
        
        else:
            # Solid color
            if self.config.back_color.startswith("#"):
                return Image.new('RGB', (width, height), self.config.back_color)
            else:
                return Image.new('RGB', (width, height), "white")
    
    def _add_watermark(self, img: Image.Image, text: str) -> Image.Image:
        """Add watermark text"""
        if not text:
            return img
        
        draw = ImageDraw.Draw(img)
        font = self._load_font(20, italic=True)
        
        if font:
            # Semi-transparent watermark
            watermark = Image.new('RGBA', img.size, (255, 255, 255, 0))
            watermark_draw = ImageDraw.Draw(watermark)
            
            # Calculate text size and position (diagonal)
            text_width = draw.textlength(text, font=font)
            text_height = 30
            
            # Draw at 45 degree angle
            for i in range(-img.height, img.width + img.height, 150):
                watermark_draw.text(
                    (i, img.height // 2),
                    text,
                    font=font,
                    fill=(200, 200, 200, 30)
                )
            
            # Composite with original
            img = Image.alpha_composite(img.convert('RGBA'), watermark)
        
        return img.convert('RGB')
    
    def _add_emboss_effect(self, img: Image.Image) -> Image.Image:
        """Add emboss effect to QR border"""
        if not self.config.show_qr_border:
            return img
        
        draw = ImageDraw.Draw(img)
        
        # Create embossed border effect
        border_color = self.config.fill_color
        r, g, b = [int(border_color[i:i+2], 16) for i in (1, 3, 5)]
        
        # Light and dark versions for emboss
        light_color = (min(255, r + 40), min(255, g + 40), min(255, b + 40))
        dark_color = (max(0, r - 40), max(0, g - 40), max(0, b - 40))
        
        # Draw embossed rectangle
        rect = [
            self.config.border * self.config.box_size - 15,
            self.config.border * self.config.box_size - 15,
            img.width - self.config.border * self.config.box_size + 15,
            img.height - self.config.border * self.config.box_size + 15
        ]
        
        # Light top/left
        draw.line([rect[0], rect[1], rect[2], rect[1]], fill=light_color, width=2)
        draw.line([rect[0], rect[1], rect[0], rect[3]], fill=light_color, width=2)
        
        # Dark bottom/right
        draw.line([rect[0], rect[3], rect[2], rect[3]], fill=dark_color, width=2)
        draw.line([rect[2], rect[1], rect[2], rect[3]], fill=dark_color, width=2)
        
        return img
    
    def generate(self, data: str, output_path: str, show_info: bool = False) -> Dict[str, Any]:
        """
        Generate QR code with all enhancements
        
        Returns:
            Dictionary with generation details
        """
        try:
            if show_info:
                print(f"Generating QR code for: {data[:30]}...")
            
            # Create appropriate QR code
            if "gradient" in self.config.custom_css:
                qr_img = self._create_gradient_qr(data)
            else:
                qr_img = self._create_base_qr(data)
            
            # Add logo if configured
            if self.config.add_logo:
                qr_img = self._add_logo(qr_img)
            
            # Create layout
            layout = Layout.auto(qr_img.size, self.config)
            
            # Create final image with background
            if "gradient" in self.config.custom_css:
                final_img = self._create_background((layout.width, layout.height), "gradient")
            else:
                final_img = self._create_background((layout.width, layout.height), "solid")
            
            draw = ImageDraw.Draw(final_img)
            
            # Add emboss effect to QR area
            if self.config.show_qr_border:
                final_img = self._add_emboss_effect(final_img)
            
            # Paste QR code
            final_img.paste(qr_img, layout.qr_position)
            
            # Add title
            if self.config.title:
                title_font = self._load_font(28, bold=True)
                if title_font:
                    title_width = draw.textlength(self.config.title, font=title_font)
                    title_x = (layout.width - title_width) // 2
                    draw.text((title_x, layout.title_position[1]), 
                             self.config.title, 
                             fill=self.config.fill_color, 
                             font=title_font, 
                             stroke_width=1,
                             stroke_fill=self.config.back_color)
            
            # Add subtitle
            if self.config.subtitle:
                subtitle_font = self._load_font(16, italic=True)
                if subtitle_font:
                    subtitle_width = draw.textlength(self.config.subtitle, font=subtitle_font)
                    subtitle_x = (layout.width - subtitle_width) // 2
                    draw.text((subtitle_x, layout.subtitle_position[1]), 
                             self.config.subtitle, 
                             fill="#7F8C8D", 
                             font=subtitle_font)
            
            # Add wallet address
            if self.config.show_address:
                # Label
                label_font = self._load_font(16, bold=True)
                if label_font:
                    draw.text(layout.address_position, 
                             "Wallet Address:", 
                             fill="#2C3E50", 
                             font=label_font)
                
                # Address (shortened for display)
                if len(data) > 30:
                    display_addr = f"{data[:15]}...{data[-15:]}"
                else:
                    display_addr = data
                
                addr_font = self._load_font(14)
                if addr_font:
                    addr_y = layout.address_position[1] + 25
                    draw.text((layout.padding, addr_y), 
                             display_addr, 
                             fill=self.config.fill_color, 
                             font=addr_font)
                
                # Full address in small monospace font
                small_font = self._load_font(10)
                if small_font:
                    full_addr_y = addr_y + 30
                    
                    # Split long address into multiple lines
                    if len(data) > 50:
                        chunks = [data[i:i+50] for i in range(0, len(data), 50)]
                        for i, chunk in enumerate(chunks):
                            draw.text((layout.padding, full_addr_y + i * 15), 
                                     chunk, 
                                     fill="#7F8C8D", 
                                     font=small_font)
                    else:
                        draw.text((layout.padding, full_addr_y), 
                                 data, 
                                 fill="#7F8C8D", 
                                 font=small_font)
            
            # Add watermark
            if self.config.watermark:
                final_img = self._add_watermark(final_img, self.config.watermark)
            
            # Save image with high quality
            final_img.save(output_path, quality=95, optimize=True)
            
            # Return generation info
            file_size = os.path.getsize(output_path)
            
            return {
                "filepath": output_path,
                "size_bytes": file_size,
                "size_formatted": format_file_size(file_size),
                "dimensions": final_img.size,
                "address": data,
                "style": "gradient" if "gradient" in self.config.custom_css else "standard"
            }
            
        except Exception as e:
            raise GenerationError(f"Failed to generate QR code: {e}")
    
    def generate_batch(self, addresses: List[str], output_dir: str, 
                      progress_callback=None) -> List[Dict[str, Any]]:
        """
        Generate multiple QR codes
        
        Returns:
            List of generation results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        total = len(addresses)
        
        for i, address in enumerate(addresses, 1):
            try:
                # Generate unique filename
                filename = generate_filename(address, "batch", i)
                output_path = os.path.join(output_dir, filename)
                
                # Generate QR
                result = self.generate(address, output_path, show_info=False)
                results.append(result)
                
                # Update progress
                if progress_callback:
                    progress_callback(i, total, address)
                    
            except Exception as e:
                print(f"Error generating QR for address {i}: {e}")
                # Continue with next address
        
        return results