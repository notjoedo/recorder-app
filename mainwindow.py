# This Python file uses the following encoding: utf-8
import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem
import shutil
import os

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set up model for QListView
        self.model = QStandardItemModel(self.ui.listView)
        self.ui.listView.setModel(self.model)

        # Connect the Import File action from the menu
        self.ui.actionMenu.triggered.connect(self.import_py_file)

        # Connect the Refresh List button
        self.ui.refreshList.clicked.connect(self.refresh_list)

        # Load Python files from the recorder directory
        self.load_python_files()

    def import_py_file(self):
        # Open a file dialog to select a .py file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Python File", "", "Python Files (*.py)")
        if file_name:
            # Add the file to the QListView
            self.add_file_to_list_view(file_name)
            # Copy the .py file to the recorder directory
            self.copy_file_to_recorder(file_name)

    def add_file_to_list_view(self, file_name):
        # Create an item with the file name and add it to the list view
        item = QStandardItem(os.path.basename(file_name))  # Display only the file name
        self.model.appendRow(item)

    def copy_file_to_recorder(self, file_name):
        # Define the destination path where you want to copy the .py file
        destination_directory = "pythonfiles"  # Make sure this directory exists
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)  # Create the directory if it doesn't exist

        # Copy the file to the destination directory
        shutil.copy(file_name, os.path.join(destination_directory, os.path.basename(file_name)))

        # Load the updated list of Python files from the pythonfiles directory
        self.load_python_files()

    def load_python_files(self):
        # Clear the current model before loading files
        self.model.clear()

        # Load .py files from the pythonfiles directory
        destination_directory = "pythonfiles"
        if os.path.exists(destination_directory):
            for file_name in os.listdir(destination_directory):
                if file_name.endswith('.py'):
                    self.add_file_to_list_view(os.path.join(destination_directory, file_name))

    def refresh_list(self):
        # Reload the list of Python files
        self.load_python_files()

    def closeEvent(self, event):
        # This function is called when the application is about to close
        event.accept()  # Accept the event to proceed with closing

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
