"""
Utility functions for Wallet QR Generator
"""

import os
import sys
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import shutil

def validate_wallet_address(address: str) -> Tuple[bool, str]:
    """
    Validate wallet address format and detect type
    
    Returns:
        Tuple of (is_valid, detected_type)
    """
    if not address or len(address) < 10:
        return False, "invalid"
    
    # Remove whitespace
    address = address.strip()
    
    # Common crypto address patterns
    patterns = {
        "bitcoin": r'^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$',
        "ethereum": r'^0x[a-fA-F0-9]{40}$',
        "litecoin": r'^[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}$',
        "solana": r'^[1-9A-HJ-NP-Za-km-z]{32,44}$',
        "base64": r'^[A-Za-z0-9+/]+={0,2}$',
        "generic": r'^[A-Za-z0-9\-_+=/.]+$'
    }
    
    for coin_type, pattern in patterns.items():
        if re.match(pattern, address):
            return True, coin_type
    
    return False, "unknown"

def get_file_hash(filepath: str, algorithm: str = "sha256") -> str:
    """
    Calculate hash of a file
    """
    hash_func = getattr(hashlib, algorithm)()
    
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def create_output_dir(base_dir: str = "output", prefix: str = "qr_codes") -> str:
    """
    Create output directory with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(base_dir, f"{prefix}_{timestamp}")
    
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def save_config(config: Dict[str, Any], output_dir: str) -> str:
    """
    Save configuration to JSON file
    """
    config_file = os.path.join(output_dir, "generation_config.json")
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return config_file

def load_config(config_file: str) -> Dict[str, Any]:
    """
    Load configuration from JSON file
    """
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_banner():
    """
    Print ASCII art banner
    """
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║    ██████╗ ██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗   ║
    ║    ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗  ║
    ║    ██████╔╝██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║  ║
    ║    ██╔══██╗██╔══██╗  ╚██╔╝  ██╔══██╗   ██║   ██║   ██║  ║
    ║    ██║  ██║██║  ██║   ██║   ██████╔╝   ██║   ╚██████╔╝  ║
    ║    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝    ╚═╝    ╚═════╝   ║
    ║                                                          ║
    ║           C R Y P T O   W A L L E T   Q R                ║
    ║                G E N E R A T O R   v1.0.0                ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_success(message: str):
    """Print success message in green"""
    print(f"\033[92m✓ {message}\033[0m")

def print_error(message: str):
    """Print error message in red"""
    print(f"\033[91m✗ {message}\033[0m")

def print_warning(message: str):
    """Print warning message in yellow"""
    print(f"\033[93m⚠ {message}\033[0m")

def print_info(message: str):
    """Print info message in blue"""
    print(f"\033[94mℹ {message}\033[0m")

class ProgressBar:
    """Professional progress bar implementation"""
    
    def __init__(self, total: int, prefix: str = '', suffix: str = '', 
                 length: int = 50, fill: str = '█', show_percent: bool = True):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.show_percent = show_percent
        self.current = 0
        self.start_time = datetime.now()
    
    def update(self, progress: int = 1):
        """Update progress bar"""
        self.current += progress
        percent = f"{100 * (self.current / float(self.total)):3.1f}"
        
        filled_length = int(self.length * self.current // self.total)
        bar = self.fill * filled_length + '─' * (self.length - filled_length)
        
        if self.show_percent:
            print(f'\r{self.prefix} │{bar}│ {percent}% {self.suffix}', end='\r')
        else:
            print(f'\r{self.prefix} │{bar}│ {self.current}/{self.total} {self.suffix}', end='\r')
        
        if self.current == self.total:
            elapsed = datetime.now() - self.start_time
            print(f'\r{self.prefix} │{self.fill * self.length}│ Done in {elapsed.total_seconds():.1f}s     ')
    
    def finish(self):
        """Force finish the progress bar"""
        self.update(self.total - self.current)

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width() -> int:
    """Get terminal width in characters"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def format_file_size(bytes_size: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0 # type: ignore
    return f"{bytes_size:.1f} TB"

def generate_filename(address: str, style: str, index: int = None) -> str: # type: ignore
    """Generate consistent filename for QR code"""
    # Create short hash from address
    short_hash = hashlib.md5(address.encode()).hexdigest()[:8]
    
    # Remove special characters for filename safety
    safe_style = re.sub(r'[^\w\-]', '_', style)
    
    if index is not None:
        return f"qr_{index:03d}_{safe_style}_{short_hash}.png"
    return f"qr_{safe_style}_{short_hash}.png"