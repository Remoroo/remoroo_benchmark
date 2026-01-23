import os
import random
import shutil

REPO_ROOT = "repo"

# Ensure "a" through "y" modules come first to flood the context
PREFIXES = [chr(i) for i in range(ord('a'), ord('z'))] # ['a', 'b', ..., 'y']
MODULE_NAMES = [f"{p}_mod_{i}" for p in PREFIXES for i in range(4)] # ~100 modules

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        f.write(content)

def generate_noise_file(module, name):
    return f"""
import time
import random

class {module.replace('_', '').capitalize()}{name.capitalize()}Manager:
    \"\"\"
    Managed component for {module}.
    Status: Active
    \"\"\"
    def __init__(self):
        self.status = "active"
        self.last_update = time.time()
        
    def process(self, data):
        # Simulation of {module} logic
        if not data:
            return False
        return True
"""

def generate_repo():
    if os.path.exists(REPO_ROOT):
        shutil.rmtree(REPO_ROOT)
    ensure_dir(REPO_ROOT)
    
    print("Generating massive repository... this may take a moment.")
    
    # 1. Generate Noise Modules (Flood the index)
    # 100 modules * 15 files = 1500 files
    # This should be enough to truncate the index if it sorts alphabetically
    for mod in MODULE_NAMES:
        write_file(f"{REPO_ROOT}/pkg/{mod}/__init__.py", "")
        for i in range(15):
            name = f"component_{i}"
            content = generate_noise_file(mod, name)
            write_file(f"{REPO_ROOT}/pkg/{mod}/{name}.py", content)
            
    # 2. Generate Target Module (starts with 'z' to be last)
    target_mod = "z_legacy_systems"
    write_file(f"{REPO_ROOT}/pkg/{target_mod}/__init__.py", "")
    
    # 3. Create HIDDEN target file
    # The file name is generic "processor.py", but the class name is unique
    target_content = """
class LegacyHiddenProcessor:
    \"\"\"
    Legacy processor for hidden data streams.
    Handles critical validation logic.
    \"\"\"
    def __init__(self):
        self.valid = True
        
    def process(self, data):
        # BUG: Returns True even if data is invalid
        # Should check if data is valid
        if not data:
            # return False # Fix is commented out
            return True
        return True
"""
    write_file(f"{REPO_ROOT}/pkg/{target_mod}/processor.py", target_content)
    
    # 4. Create Test File (Entrypoint for verification)
    test_content = """
import unittest
from pkg.z_legacy_systems.processor import LegacyHiddenProcessor

class TestLegacyHiddenProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = LegacyHiddenProcessor()

    def test_invalid_data_returns_false(self):
        # Passing None or empty dict should return False
        result = self.processor.process(None)
        self.assertFalse(result, "Processor should return False for invalid data")

if __name__ == '__main__':
    unittest.main()
"""
    write_file(f"{REPO_ROOT}/pkg/{target_mod}/test_processor.py", test_content)
    
    # root
    write_file(f"{REPO_ROOT}/main.py", "print('Loaded.')")

if __name__ == "__main__":
    generate_repo()
    print(f"Generated massive repo in {os.path.abspath(REPO_ROOT)}")
