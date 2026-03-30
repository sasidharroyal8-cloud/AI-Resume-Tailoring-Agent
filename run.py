#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add project root and src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(project_root))

# Change to project root directory
os.chdir(str(project_root))

from src.main import main

if __name__ == "__main__":
    main()
