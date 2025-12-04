import sys
import os
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QFileDialog, 
                             QSpinBox, QCheckBox, QMessageBox, QGroupBox,
                             QHeaderView, QRadioButton, QButtonGroup, QTextEdit,
                             QSplitter, QAbstractItemView)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont, QPixmap, QDesktopServices


class FileRenamerApp(QMainWindow):
    """Main application window for batch file renaming."""
    
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.init_ui()
        self.center_window()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Batch File Renamer")
        self.setMinimumSize(900, 600)
        
        # Apply modern styling
        self.apply_styles()
        
        # Central widget with splitter for main content and preview
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter to divide main controls and file preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Main controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("📁 Batch File Renamer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(title_label)
        
        # File selection button
        select_btn = QPushButton("📂 Select Files")
        select_btn.setToolTip("Click to select multiple files to rename")
        select_btn.clicked.connect(self.select_files)
        select_btn.setMinimumHeight(40)
        left_layout.addWidget(select_btn)
        
        # Renaming options group
        options_group = QGroupBox("Renaming Options")
        options_layout = QVBoxLayout()
        
        # Rename mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Rename Mode:")
        self.mode_group = QButtonGroup()
        self.numeric_radio = QRadioButton("Numeric (e.g., file_1, file_2)")
        self.date_radio = QRadioButton("Date-based (e.g., file_2025-10-18)")
        self.numeric_radio.setChecked(True)
        self.mode_group.addButton(self.numeric_radio)
        self.mode_group.addButton(self.date_radio)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.numeric_radio)
        mode_layout.addWidget(self.date_radio)
        mode_layout.addStretch()
        options_layout.addLayout(mode_layout)
        
        # Base name input
        base_layout = QHBoxLayout()
        base_label = QLabel("Base Name:")
        base_label.setMinimumWidth(120)
        self.base_name_input = QLineEdit()
        self.base_name_input.setPlaceholderText("Custom name (leave empty to keep original, space to remove)")
        self.base_name_input.setToolTip("Enter a custom name, leave empty to keep original names, or enter a space to remove original names")
        base_layout.addWidget(base_label)
        base_layout.addWidget(self.base_name_input)
        options_layout.addLayout(base_layout)
        
        # Starting number
        number_layout = QHBoxLayout()
        number_label = QLabel("Starting Number:")
        number_label.setMinimumWidth(120)
        self.start_number_spin = QSpinBox()
        self.start_number_spin.setMinimum(0)
        self.start_number_spin.setMaximum(9999)
        self.start_number_spin.setValue(1)
        self.start_number_spin.setToolTip("Choose the starting number for sequential naming")
        number_layout.addWidget(number_label)
        number_layout.addWidget(self.start_number_spin)
        number_layout.addStretch()
        options_layout.addLayout(number_layout)
        
        # Date/Time options
        datetime_layout = QHBoxLayout()
        self.include_date_check = QCheckBox("Include Date (YYYY-MM-DD)")
        self.include_time_check = QCheckBox("Include Time (HH-MM-SS)")
        datetime_layout.addWidget(self.include_date_check)
        datetime_layout.addWidget(self.include_time_check)
        datetime_layout.addStretch()
        options_layout.addLayout(datetime_layout)
        
        options_group.setLayout(options_layout)
        left_layout.addWidget(options_group)
        
        # Preview table with reordering controls
        preview_header_layout = QHBoxLayout()
        preview_label = QLabel("Preview:")
        preview_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        preview_header_layout.addWidget(preview_label)
        preview_header_layout.addStretch()
        
        # Reorder buttons
        self.move_up_btn = QPushButton("⬆️ Move Up")
        self.move_up_btn.setToolTip("Move selected file up in the list")
        self.move_up_btn.clicked.connect(self.move_file_up)
        self.move_up_btn.setEnabled(False)
        self.move_up_btn.setMaximumWidth(120)
        
        self.move_down_btn = QPushButton("⬇️ Move Down")
        self.move_down_btn.setToolTip("Move selected file down in the list")
        self.move_down_btn.clicked.connect(self.move_file_down)
        self.move_down_btn.setEnabled(False)
        self.move_down_btn.setMaximumWidth(120)
        
        preview_header_layout.addWidget(self.move_up_btn)
        preview_header_layout.addWidget(self.move_down_btn)
        
        left_layout.addLayout(preview_header_layout)
        
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)
        self.preview_table.setHorizontalHeaderLabels(["Original Name", "New Name"])
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.preview_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.preview_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.preview_table.itemSelectionChanged.connect(self.on_selection_changed)
        left_layout.addWidget(self.preview_table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        preview_btn = QPushButton("🔍 Preview")
        preview_btn.setToolTip("Preview the renamed files before applying changes")
        preview_btn.clicked.connect(self.preview_rename)
        preview_btn.setMinimumHeight(40)
        
        rename_btn = QPushButton("✅ Rename Files")
        rename_btn.setToolTip("Apply the renaming to all selected files")
        rename_btn.clicked.connect(self.rename_files)
        rename_btn.setMinimumHeight(40)
        rename_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setToolTip("Clear all selections and reset options")
        reset_btn.clicked.connect(self.reset_app)
        reset_btn.setMinimumHeight(40)
        reset_btn.setStyleSheet("background-color: #f44336; color: white;")
        
        button_layout.addWidget(preview_btn)
        button_layout.addWidget(rename_btn)
        button_layout.addWidget(reset_btn)
        
        left_layout.addLayout(button_layout)
        
        # Right side - File Preview
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 20, 20, 20)
        
        preview_title = QLabel("📄 File Preview")
        preview_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        preview_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(preview_title)
        
        # File info label
        self.file_info_label = QLabel("Select a file to preview")
        self.file_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_info_label.setStyleSheet("color: #757575; padding: 10px;")
        right_layout.addWidget(self.file_info_label)
        
        # Preview area for text files
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText("File content will appear here...")
        right_layout.addWidget(self.preview_text)
        
        # Preview area for images
        self.preview_image_label = QLabel()
        self.preview_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_image_label.setStyleSheet("border: 2px solid #e0e0e0; background-color: #f5f5f5;")
        self.preview_image_label.setMinimumSize(200, 200)
        self.preview_image_label.hide()
        right_layout.addWidget(self.preview_image_label)
        
        # Open file button
        open_file_btn = QPushButton("🔗 Open in Default App")
        open_file_btn.setToolTip("Open the selected file in its default application")
        open_file_btn.clicked.connect(self.open_selected_file)
        right_layout.addWidget(open_file_btn)
        
        # Add widgets to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 400])  # 60-40 split
        
        main_layout.addWidget(splitter)
        
    def apply_styles(self):
        """Apply modern styling to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                color: #212121;
            }
            QLabel {
                color: #212121;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                font-weight: bold;
                color: #212121;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #212121;
            }
            QLineEdit, QSpinBox {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                color: #212121;
            }
            QLineEdit:focus, QSpinBox:focus {
                border: 2px solid #2196F3;
            }
            QTableWidget {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                color: #212121;
                alternate-background-color: #E3F2FD;
            }
            QTableWidget::item {
                color: #212121;
                padding: 5px;
            }
            QTableWidget::item:alternate {
                color: #212121;
            }
            QTableWidget::item:selected {
                background-color: #FFD54F;
                color: #212121;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #42A5F5;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }
            QCheckBox, QRadioButton {
                spacing: 8px;
                color: #212121;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #2196F3;
                border: none;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #1976D2;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 6px solid white;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid white;
                width: 0px;
                height: 0px;
            }
            QMessageBox {
                background-color: white;
                color: #212121;
            }
            QMessageBox QLabel {
                color: #212121;
                background-color: white;
            }
            QMessageBox QPushButton {
                background-color: #2196F3;
                color: white;
                min-width: 80px;
                padding: 5px 15px;
            }
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
                color: #212121;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QSplitter::handle {
                background-color: #e0e0e0;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #2196F3;
            }
        """)
        
    def center_window(self):
        """Center the window on the screen."""
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
        
    def select_files(self):
        """Open file dialog to select multiple files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files to Rename",
            "",
            "All Files (*.*)"
        )
        
        if files:
            self.selected_files = files
            QMessageBox.information(
                self,
                "Files Selected",
                f"Successfully selected {len(files)} file(s)."
            )
            self.preview_rename()
    
    def show_file_preview(self):
        """Show preview of the selected file."""
        selected_items = self.preview_table.selectedItems()
        if not selected_items:
            self.file_info_label.setText("Select a file to preview")
            self.preview_text.clear()
            self.preview_image_label.hide()
            self.preview_text.show()
            return
        
        # Get the row of the selected item
        row = selected_items[0].row()
        if row >= len(self.selected_files):
            return
        
        file_path = Path(self.selected_files[row])
        
        # Update file info
        file_size = file_path.stat().st_size
        size_str = self.format_file_size(file_size)
        self.file_info_label.setText(
            f"📁 {file_path.name}\n"
            f"📊 Size: {size_str} | Type: {file_path.suffix.upper() or 'No extension'}"
        )
        
        # Preview based on file type
        extension = file_path.suffix.lower()
        
        # Image files
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico']:
            self.preview_text.hide()
            self.preview_image_label.show()
            pixmap = QPixmap(str(file_path))
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.preview_image_label.width() - 20,
                    self.preview_image_label.height() - 20,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_image_label.setPixmap(scaled_pixmap)
            else:
                self.preview_image_label.setText("Cannot preview image")
        
        # Text files
        elif extension in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv', '.log']:
            self.preview_image_label.hide()
            self.preview_text.show()
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(10000)  # Read first 10KB
                    if len(content) == 10000:
                        content += "\n\n... (preview truncated)"
                    self.preview_text.setText(content)
            except Exception as e:
                self.preview_text.setText(f"Cannot preview file: {str(e)}")
        
        # Other files
        else:
            self.preview_image_label.hide()
            self.preview_text.show()
            self.preview_text.setText(
                f"Preview not available for {extension} files.\n\n"
                f"Click 'Open in Default App' to view this file."
            )
    
    def on_selection_changed(self):
        """Handle table selection change to enable/disable move buttons and show preview."""
        selected_items = self.preview_table.selectedItems()
        
        if selected_items:
            row = selected_items[0].row()
            total_rows = self.preview_table.rowCount()
            
            # Enable/disable buttons based on position
            self.move_up_btn.setEnabled(row > 0)
            self.move_down_btn.setEnabled(row < total_rows - 1)
        else:
            self.move_up_btn.setEnabled(False)
            self.move_down_btn.setEnabled(False)
        
        # Show file preview
        self.show_file_preview()
    
    def move_file_up(self):
        """Move the selected file up in the list."""
        selected_items = self.preview_table.selectedItems()
        if not selected_items:
            return
        
        current_row = selected_items[0].row()
        if current_row <= 0:
            return
        
        # Swap files in the selected_files list
        self.selected_files[current_row], self.selected_files[current_row - 1] = \
            self.selected_files[current_row - 1], self.selected_files[current_row]
        
        # Refresh the preview with updated order
        self.preview_rename()
        
        # Re-select the moved item at its new position
        self.preview_table.selectRow(current_row - 1)
    
    def move_file_down(self):
        """Move the selected file down in the list."""
        selected_items = self.preview_table.selectedItems()
        if not selected_items:
            return
        
        current_row = selected_items[0].row()
        if current_row >= self.preview_table.rowCount() - 1:
            return
        
        # Swap files in the selected_files list
        self.selected_files[current_row], self.selected_files[current_row + 1] = \
            self.selected_files[current_row + 1], self.selected_files[current_row]
        
        # Refresh the preview with updated order
        self.preview_rename()
        
        # Re-select the moved item at its new position
        self.preview_table.selectRow(current_row + 1)
    
    def format_file_size(self, size_bytes):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def open_selected_file(self):
        """Open the selected file in its default application."""
        selected_items = self.preview_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a file first.")
            return
        
        row = selected_items[0].row()
        if row >= len(self.selected_files):
            return
        
        file_path = Path(self.selected_files[row])
        if file_path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(file_path)))
        else:
            QMessageBox.warning(self, "File Not Found", f"The file {file_path.name} was not found.")
        
    def generate_new_name(self, original_path, index):
        """Generate new filename based on current settings."""
        file_path = Path(original_path)
        extension = file_path.suffix
        
        # Get base name - if user enters anything (even spaces), use it; otherwise use original name
        base_name = self.base_name_input.text()
        
        # If user entered text (including spaces), use only that as base
        # If empty, keep the original filename
        if base_name:  # User entered something (custom name or spaces)
            base_name = base_name.strip()
            if not base_name:  # User entered only spaces - start fresh without original name
                new_name_parts = []
            else:  # User entered a custom name
                new_name_parts = [base_name]
        else:  # Input is empty - keep original name
            new_name_parts = [file_path.stem]
        
        # Add numbering or date based on mode
        if self.date_radio.isChecked():
            # Date-based mode
            if self.include_date_check.isChecked():
                new_name_parts.append(datetime.now().strftime("%Y-%m-%d"))
            if self.include_time_check.isChecked():
                new_name_parts.append(datetime.now().strftime("%H-%M-%S"))
            # Add index for uniqueness
            new_name_parts.append(str(self.start_number_spin.value() + index))
        else:
            # Numeric mode
            if self.include_date_check.isChecked():
                new_name_parts.append(datetime.now().strftime("%Y-%m-%d"))
            if self.include_time_check.isChecked():
                new_name_parts.append(datetime.now().strftime("%H-%M-%S"))
            # Add sequential number
            new_name_parts.append(str(self.start_number_spin.value() + index))
        
        # Build the new name - filter out empty parts
        new_name_parts = [part for part in new_name_parts if part]
        
        # If somehow all parts are empty, use just the number
        if not new_name_parts:
            new_name_parts = [str(self.start_number_spin.value() + index)]
        
        new_name = "_".join(new_name_parts) + extension
        return new_name
        
    def preview_rename(self):
        """Preview the renamed files in the table."""
        if not self.selected_files:
            QMessageBox.warning(self, "No Files", "Please select files first.")
            return
        
        self.preview_table.setRowCount(len(self.selected_files))
        
        for i, file_path in enumerate(self.selected_files):
            original_name = Path(file_path).name
            new_name = self.generate_new_name(file_path, i)
            
            self.preview_table.setItem(i, 0, QTableWidgetItem(original_name))
            self.preview_table.setItem(i, 1, QTableWidgetItem(new_name))
            
    def check_duplicate_names(self):
        """Check for duplicate names in the preview."""
        new_names = set()
        for i in range(self.preview_table.rowCount()):
            new_name_item = self.preview_table.item(i, 1)
            if new_name_item:
                new_name = new_name_item.text()
                if new_name in new_names:
                    return True, new_name
                new_names.add(new_name)
        return False, None
        
    def rename_files(self):
        """Apply the renaming to all selected files."""
        if not self.selected_files:
            QMessageBox.warning(self, "No Files", "Please select files first.")
            return
        
        # Check for duplicates
        has_duplicates, duplicate_name = self.check_duplicate_names()
        if has_duplicates:
            QMessageBox.critical(
                self,
                "Duplicate Names",
                f"Duplicate name detected: {duplicate_name}\n"
                "Please adjust your settings to avoid conflicts."
            )
            return
        
        # Confirm action
        reply = QMessageBox.question(
            self,
            "Confirm Rename",
            f"Are you sure you want to rename {len(self.selected_files)} file(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Perform renaming
        success_count = 0
        error_count = 0
        
        for i, original_path in enumerate(self.selected_files):
            try:
                file_path = Path(original_path)
                new_name = self.generate_new_name(original_path, i)
                new_path = file_path.parent / new_name
                
                # Check if target file already exists
                if new_path.exists():
                    error_count += 1
                    continue
                
                file_path.rename(new_path)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"Error renaming {original_path}: {str(e)}")
        
        # Show results
        if error_count == 0:
            QMessageBox.information(
                self,
                "Success",
                f"Successfully renamed {success_count} file(s)!"
            )
            self.reset_app()
        else:
            QMessageBox.warning(
                self,
                "Partial Success",
                f"Renamed {success_count} file(s).\n"
                f"Failed to rename {error_count} file(s)."
            )
            
    def reset_app(self):
        """Reset the application to initial state."""
        self.selected_files = []
        self.preview_table.setRowCount(0)
        self.base_name_input.clear()
        self.start_number_spin.setValue(1)
        self.include_date_check.setChecked(False)
        self.include_time_check.setChecked(False)
        self.numeric_radio.setChecked(True)
        self.file_info_label.setText("Select a file to preview")
        self.preview_text.clear()
        self.preview_image_label.clear()
        self.preview_image_label.hide()
        self.preview_text.show()


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Batch File Renamer")
    
    window = FileRenamerApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()