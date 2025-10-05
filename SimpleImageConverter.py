import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, 
    QComboBox, QMessageBox, QProgressBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from convert import convert_image, SUPPORTED_EXTENSIONS, SAVE_FOLDER

class ImageConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.folder_path = ""
        self.setWindowIcon(QIcon('simple_logo.ico')) 
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Simple Image Converter | by nzmk")
        self.resize(400, 250)
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        self.label = QLabel("Drag & Drop a folder here\nor click the button below.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.select_button = QPushButton("Choose Folder")
        self.select_button.clicked.connect(self.choose_folder)
        layout.addWidget(self.select_button)

        self.format_combo = QComboBox()
        self.format_combo.addItems(SUPPORTED_EXTENSIONS)
        layout.addWidget(self.format_combo)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.convert_button = QPushButton("Convert Images")
        self.convert_button.clicked.connect(self.convert_images)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                self.folder_path = path
                self.label.setText(f"Folder selected: {path}")
            else:
                QMessageBox.warning(self, "Error", "Please drop a folder, not a file.")

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.label.setText(f"Folder selected: {folder}")

    def convert_images(self):
        if not self.folder_path:
            QMessageBox.warning(self, "Warning", "Please select a folder first.")
            return

        output_ext = self.format_combo.currentText()
        images = [f for f in os.listdir(self.folder_path)
                  if any(f.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS)]

        if not images:
            QMessageBox.warning(self, "Error", "No supported images found in folder.")
            return

        os.makedirs(SAVE_FOLDER, exist_ok=True)

        total = len(images)
        for i, img_name in enumerate(images, start=1):
            input_path = os.path.join(self.folder_path, img_name)
            output_name = os.path.splitext(img_name)[0] + output_ext
            output_path = os.path.join(SAVE_FOLDER, output_name)
            convert_image(input_path, output_path)

            progress = int((i / total) * 100)
            self.progress_bar.setValue(progress)
            QApplication.processEvents() 

        QMessageBox.information(self, "Done", "All images converted successfully!")
        self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterApp()
    window.show()
    sys.exit(app.exec_())
