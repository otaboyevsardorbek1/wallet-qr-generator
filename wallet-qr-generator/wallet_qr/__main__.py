#!/usr/bin/env python3
"""
Entry point when running as module: python -m wallet_qr
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())