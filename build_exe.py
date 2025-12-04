"""
Build script to create an executable file for the Batch File Renamer app.
This script uses PyInstaller to package the app into a standalone .exe file.
"""

import os
import subprocess
import sys
from pathlib import Path


def build_executable():
    """Build the executable using PyInstaller."""
    
    print("=" * 60)
    print("Building Batch File Renamer Executable")
    print("=" * 60)
    print()
    
    # Define the PyInstaller command
    app_name = "BatchFileRenamer"
    script_name = "file_renamer_app.py"
    
    # Check if the script exists
    if not Path(script_name).exists():
        print(f"❌ Error: {script_name} not found!")
        return False
    
    # PyInstaller arguments
    pyinstaller_args = [
        sys.executable,                        # Use the current Python interpreter
        "-m", "PyInstaller",                   # Run PyInstaller as a module
        "--name", app_name,                    # Name of the executable
        "--onefile",                           # Create a single executable file
        "--windowed",                          # Don't show console window (GUI app)
        "--clean",                             # Clean PyInstaller cache
        "--noconfirm",                         # Replace output directory without asking
        script_name
    ]
    
    print("🔨 Building executable with PyInstaller...")
    print(f"Command: {' '.join(pyinstaller_args)}")
    print()
    
    try:
        # Run PyInstaller
        result = subprocess.run(pyinstaller_args, check=True)
        
        if result.returncode == 0:
            print()
            print("=" * 60)
            print("✅ Build Successful!")
            print("=" * 60)
            print()
            print(f"📦 Executable location: dist/{app_name}.exe")
            print()
            print("You can now:")
            print(f"  1. Find the executable in the 'dist' folder")
            print(f"  2. Copy '{app_name}.exe' to any Windows computer")
            print(f"  3. Run it without installing Python or any dependencies!")
            print()
            print("Note: The first run might take a few seconds to start.")
            print("=" * 60)
            return True
        else:
            print("❌ Build failed!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during build: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found! Please install it first:")
        print("   pip install pyinstaller")
        return False


def clean_build_files():
    """Clean up build artifacts (optional)."""
    import shutil
    
    print()
    cleanup = input("Do you want to clean up build files? (keeps only the .exe) [y/N]: ").strip().lower()
    
    if cleanup == 'y':
        dirs_to_remove = ['build', '__pycache__']
        files_to_remove = ['BatchFileRenamer.spec']
        
        for dir_name in dirs_to_remove:
            if Path(dir_name).exists():
                shutil.rmtree(dir_name)
                print(f"🗑️  Removed: {dir_name}/")
        
        for file_name in files_to_remove:
            if Path(file_name).exists():
                Path(file_name).unlink()
                print(f"🗑️  Removed: {file_name}")
        
        print("✅ Cleanup complete!")
        print(f"📦 Your executable is in: dist/BatchFileRenamer.exe")


if __name__ == "__main__":
    print()
    success = build_executable()
    
    if success:
        clean_build_files()
    
    print()
    input("Press Enter to exit...")
