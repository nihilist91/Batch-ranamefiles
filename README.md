# Batch File Renamer

A modern, user-friendly desktop application for batch renaming files with preview and reordering capabilities.

![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.7.0-41CD52?style=flat&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

## ✨ Features

- 📂 **Multi-file selection** - Select and rename multiple files at once
- 🔢 **Flexible naming modes** - Numeric or date-based renaming
- 📝 **Custom base names** - Replace original names or keep them
- 📅 **Date/Time stamps** - Include timestamps in filenames
- ⬆️⬇️ **Easy reordering** - Move files up/down with buttons
- 👀 **File preview** - Preview text files and images before renaming
- 🎨 **Modern UI** - Clean, intuitive interface with visual feedback
- ✅ **Preview changes** - See new names before applying
- 🛡️ **Error handling** - Duplicate name detection and validation
- 🚀 **Standalone executable** - No Python installation required

## 🖼️ Screenshots

### Main Interface
The app features a split-view design with file list on the left and preview on the right.

### Key Features
- Yellow highlighting for selected files
- Up/Down buttons for precise reordering
- Real-time preview of renamed files
- Support for text and image preview

## 🚀 Quick Start

### Download Release (Recommended)
1. Download `BatchFileRenamer.exe` from [Releases](../../releases)
2. Double-click to run - no installation needed!

### Run from Source
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/batch-file-renamer.git
cd batch-file-renamer

# Install dependencies
pip install -r requirements.txt

# Run the application
python file_renamer_app.py
```

## 📦 Building from Source

Create a standalone executable:

```bash
# Using the build script
python build_exe.py

# Or using the batch file
build.bat
```

The executable will be in the `dist/` folder.

## 📖 Usage Guide

### Basic Workflow
1. **Select Files** - Click "📂 Select Files" and choose multiple files
2. **Configure Options**:
   - Choose rename mode (Numeric or Date-based)
   - Enter custom base name (leave empty to keep original, space to remove)
   - Set starting number
   - Toggle date/time inclusion
3. **Reorder Files** - Select a row and use ⬆️⬇️ buttons to reorder
4. **Preview Changes** - Click "🔍 Preview" to see new filenames
5. **Review Files** - Click any row to preview file content
6. **Apply Rename** - Click "✅ Rename Files" to apply changes

### Naming Examples

**Keep original names with numbering:**
- Base Name: [empty]
- Result: `document_1.txt`, `document_2.txt`

**Custom name with numbering:**
- Base Name: "Photo"
- Result: `Photo_1.jpg`, `Photo_2.jpg`

**Date-based with custom name:**
- Base Name: "Report"
- Include Date: ✓
- Result: `Report_2025-12-04_1.pdf`

**Only numbers (remove original names):**
- Base Name: [space]
- Result: `1.txt`, `2.txt`, `3.txt`

## 🧪 Testing

Generate test files for testing:
```bash
python generate_test_files.py
```

This creates 26 sample files in various formats (documents, images, videos, etc.) in a `test_files/` folder.

## 🛠️ Requirements

- Python 3.8 or higher
- PyQt6 6.7.0
- PyInstaller (for building executable)

## 📋 System Requirements

### For Development
- Windows 10/11
- Python 3.8+
- ~100 MB disk space

### For Executable
- Windows 10/11 (64-bit)
- ~50 MB disk space
- No Python installation required

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is free to use and modify. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Packaged with [PyInstaller](https://www.pyinstaller.org/)

## 📞 Support

If you encounter any issues or have questions:
- Open an [Issue](../../issues)
- Check existing [Discussions](../../discussions)

---

Made with ❤️ for easier file management
