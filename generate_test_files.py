"""
Script to generate test files for the Batch File Renamer app.
This creates various types of files in a 'test_files' folder.
"""

import os
from pathlib import Path


def create_test_files():
    """Create a variety of test files for renaming."""
    
    # Create test_files directory
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    print(f"Creating test files in: {test_dir.absolute()}")
    
    # List of test files to create with different extensions
    test_files = [
        # Documents
        "document1.txt",
        "document2.txt",
        "report.pdf",
        "presentation.pptx",
        "spreadsheet.xlsx",
        "notes.docx",
        
        # Images
        "photo1.jpg",
        "photo2.jpg",
        "photo3.png",
        "screenshot.png",
        "image.gif",
        
        # Videos
        "video1.mp4",
        "clip.avi",
        "movie.mkv",
        
        # Audio
        "song1.mp3",
        "track2.wav",
        "audio.flac",
        
        # Code files
        "script.py",
        "program.js",
        "style.css",
        "index.html",
        
        # Archives
        "archive.zip",
        "backup.rar",
        
        # Misc
        "data.json",
        "config.xml",
        "readme.md",
    ]
    
    # Create each file
    created_count = 0
    for filename in test_files:
        file_path = test_dir / filename
        try:
            # Create empty file
            file_path.touch()
            
            # Add some sample content based on file type
            if filename.endswith('.txt'):
                file_path.write_text(f"This is a test file: {filename}")
            elif filename.endswith('.md'):
                file_path.write_text(f"# {filename}\n\nThis is a test markdown file.")
            elif filename.endswith('.json'):
                file_path.write_text('{"test": "data", "file": "' + filename + '"}')
            elif filename.endswith('.xml'):
                file_path.write_text('<?xml version="1.0"?>\n<root>\n  <file>' + filename + '</file>\n</root>')
            elif filename.endswith('.html'):
                file_path.write_text(f'<!DOCTYPE html>\n<html>\n<head><title>{filename}</title></head>\n<body><h1>Test File</h1></body>\n</html>')
            
            created_count += 1
            print(f"✓ Created: {filename}")
            
        except Exception as e:
            print(f"✗ Failed to create {filename}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Successfully created {created_count} test files!")
    print(f"Location: {test_dir.absolute()}")
    print(f"{'='*50}")
    print("\nYou can now use these files to test the Batch File Renamer app.")
    print("Instructions:")
    print("1. Run the file_renamer_app.py")
    print("2. Click 'Select Files' button")
    print("3. Navigate to the 'test_files' folder")
    print("4. Select multiple files and test the renaming features!")


def cleanup_test_files():
    """Remove all test files (optional cleanup function)."""
    test_dir = Path("test_files")
    
    if not test_dir.exists():
        print("No test_files directory found.")
        return
    
    deleted_count = 0
    for file_path in test_dir.iterdir():
        if file_path.is_file():
            file_path.unlink()
            deleted_count += 1
            print(f"✓ Deleted: {file_path.name}")
    
    # Remove the directory
    test_dir.rmdir()
    print(f"\n✓ Removed test_files directory")
    print(f"Total files deleted: {deleted_count}")


if __name__ == "__main__":
    print("="*50)
    print("Test File Generator for Batch File Renamer")
    print("="*50)
    print("\nOptions:")
    print("1. Create test files")
    print("2. Delete test files (cleanup)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        create_test_files()
    elif choice == "2":
        confirm = input("Are you sure you want to delete all test files? (yes/no): ").strip().lower()
        if confirm == "yes":
            cleanup_test_files()
        else:
            print("Cleanup cancelled.")
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice. Please run the script again.")
