import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,QHBoxLayout, QPushButton, QLabel, QFileDialog, 
    QComboBox, QMessageBox, QProgressBar, QListWidget, QListWidgetItem, QFrame
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from convert import convert_image, SUPPORTED_EXTENSIONS, SAVE_FOLDER

ver = "1.1"

class ImageConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.folder_path = ""
        self.setWindowTitle(f"Simple Image Converter | version {ver} by nzmk")

        self.setFixedSize(500, 400)

        self.setAcceptDrops(True)

        self.init_ui()

    def init_ui(self):
        vLayout = QVBoxLayout()
        hLayout = QHBoxLayout()

        self.dragDropLabel = QLabel("Drag & Drop a folder or a file here\nor click the button below.", self)
        self.dragDropLabel.setAlignment(Qt.AlignCenter)
        vLayout.addWidget(self.dragDropLabel)

        
        self.previewLabel = QLabel("Files to convert:", self)
        self.previewLabel.setFixedSize(150,13)
        vLayout.addWidget(self.previewLabel)

        self.fileList = QListWidget(self)
        self.fileList.setStyleSheet("font-size: 7pt;")
        self.fileList.setFixedHeight(60)
        vLayout.addWidget(self.fileList)

        self.clear_btn = QPushButton("Clear List",self)
        self.clear_btn.clicked.connect(self.clear_list)
        vLayout.addWidget(self.clear_btn)

        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        vLayout.addWidget(self.progressBar)

        self.selectionLabel = QLabel("Select Input Folder/File:", self)
        self.selectionLabel.setFixedSize(150,13)
        vLayout.addWidget(self.selectionLabel)
        
        self.selection_btn = QPushButton("Select Folder/File",self)
        self.selection_btn.clicked.connect(self.choose_file_or_folder)

        vLayout.addWidget(self.selection_btn)

        self.formatLabel = QLabel("Select Output Format:", self)
        self.formatLabel.setFixedSize(150,13)
        vLayout.addWidget(self.formatLabel)
        
        self.format_combo = QComboBox(self)
        self.format_combo.addItems(SUPPORTED_EXTENSIONS)
        vLayout.addWidget(self.format_combo)

        self.convert_btn = QPushButton("Convert Files",self)
        self.convert_btn.clicked.connect(self.convert_all_files)

        vLayout.addWidget(self.convert_btn)

        self.properties_btn = QPushButton("🌣 Properties",self)
        self.properties_btn.setStyleSheet("color: gray;"
                                          "font-weight: bold;")
        self.properties_btn.setFixedSize(83,25)
        hLayout.addWidget(self.properties_btn)

        self.setLayout(vLayout)
        
    def choose_file_or_folder(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Images (*.*)", options=options)

        if file_path:
            self.add_path_to_list(file_path)
        else:
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder_path:
                self.add_path_to_list(folder_path)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.exists(path):
                self.add_path_to_list(path)
    def clear_list(self):
        self.fileList.clear()
        self.progressBar.setValue(0)

    def add_path_to_list(self, path):
        items = [self.fileList.item(i).text() for i in range(self.fileList.count())]
        if path in items:
            return 

        if os.path.isdir(path):
            self.fileList.addItem(path)
        elif os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                self.fileList.addItem(path)
            else:
                QMessageBox.warning(self, "Unsupported file",
                                    f"File '{os.path.basename(path)}' has unsupported format.\nPlease select only images or folders.)")
    def convert_all_files(self):
        total_items = self.fileList.count()
        if total_items == 0:
            QMessageBox.warning(self, "No files", "Please add at least one file or folder.")
            return

        output_ext = self.format_combo.currentText()
        all_files = []

        for i in range(total_items):
            path = self.fileList.item(i).text()
            if os.path.isdir(path):
                for filename in os.listdir(path):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in SUPPORTED_EXTENSIONS:
                        all_files.append(os.path.join(path, filename))
            elif os.path.isfile(path):
                ext = os.path.splitext(path)[1].lower()
                if ext in SUPPORTED_EXTENSIONS:
                    all_files.append(path)

        total_files = len(all_files)
        if total_files == 0:
            QMessageBox.warning(self, "No images", "No supported images found to convert.")
            self.fileList.clear()
            self.progressBar.setValue(0)
            return

        converted_count = 0

        for idx, input_path in enumerate(all_files):
            filename = os.path.basename(input_path)
            output_filename = os.path.splitext(filename)[0] + output_ext
            output_path = os.path.join(SAVE_FOLDER, output_filename)

            success = convert_image(input_path, output_path)
            if success:
                converted_count += 1

            progress = int((idx + 1) / total_files * 100)
            self.progressBar.setValue(progress)
            QApplication.processEvents() 
        QMessageBox.information(
            self,
            "Conversion Complete",
            f"Converted {converted_count}/{total_files} files successfully!"
        )
        self.fileList.clear()
        self.progressBar.setValue(0)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterApp()
    window.show()
    sys.exit(app.exec_())
