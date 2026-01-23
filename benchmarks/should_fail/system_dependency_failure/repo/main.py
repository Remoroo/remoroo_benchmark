import shutil
import sys

def main():
    print("Checking for ImageMagick 'convert' tool...")
    path = shutil.which("convert")
    
    if not path:
        print("Error: 'convert' command not found in PATH.")
        print("This script requires ImageMagick to be installed on the system.")
        sys.exit(1)
        
    print(f"Success: Found 'convert' at {path}")

if __name__ == "__main__":
    main()
