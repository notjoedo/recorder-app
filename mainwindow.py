# This Python file uses the following encoding: utf-8
import sys, subprocess, shutil, os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMessageBox

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

        # Connections
        self.ui.actionMenu.triggered.connect(self.import_py_file)
        self.ui.refreshList.clicked.connect(self.refresh_list)
        self.ui.saveButton.clicked.connect(self.save_settings)
        self.ui.deleteFile.clicked.connect(self.delete_selected_file)

        # Load Python files from the recorder directory
        self.load_python_files()

        # Variables to store input values
        self.sad = None
        self.sod = None
        self.sample_rate = None
        self.mic_count = None
        self.total_spread = None

    def import_py_file(self):
        # Open a file dialog to select a .py file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Python File", "", "Python Files (*.py)")
        if file_name:
            self.add_file_to_list_view(file_name)
            self.copy_file_to_recorder(file_name)

    def add_file_to_list_view(self, file_name):
        # Add item directly to QListWidget
        item = QListWidgetItem(os.path.basename(file_name))  # Display only the file name
        item.setData(1000, file_name)  # Store the full file path as user data
        self.ui.listView.addItem(item)

    def copy_file_to_recorder(self, file_name):
        destination_directory = "pythonfiles"  # Make sure this directory exists
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)  # Create the directory if it doesn't exist
        shutil.copy(file_name, os.path.join(destination_directory, os.path.basename(file_name)))
        self.load_python_files()

    def load_python_files(self):
        # Clear the current items in the QListWidget
        self.ui.listView.clear()

        # Load .py files from the pythonfiles directory
        destination_directory = "pythonfiles"
        if os.path.exists(destination_directory):
            for file_name in os.listdir(destination_directory):
                if file_name.endswith('.py'):
                    self.add_file_to_list_view(os.path.join(destination_directory, file_name))

    def refresh_list(self):
        self.load_python_files()

    def delete_selected_file(self):
        # Get the currently selected item in the list
        selected_item = self.ui.listView.currentItem()

        if selected_item is None:
            QMessageBox.warning(self, "No Selection", "Please select a file to delete.")
            return

        # Get the file path stored in the item’s user data
        file_path = selected_item.data(1000)

        # Confirm deletion with the user
        confirm = QMessageBox.question(
            self, "Confirm Deletion", f"Are you sure you want to delete '{selected_item.text()}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            # Remove the file from the directory
            if os.path.exists(file_path):
                os.remove(file_path)
                # Remove the item from the QListWidget
                self.ui.listView.takeItem(self.ui.listView.row(selected_item))
                QMessageBox.information(self, "Deleted", f"'{selected_item.text()}' has been deleted.")
            else:
                QMessageBox.warning(self, "Error", "File not found.")

    def closeEvent(self, event):
        event.accept()

    def save_settings(self):
        # Retrieve the values from the QLineEdit widgets
        self.sad = self.ui.SAD.text()
        self.sod = self.ui.SOD.text()
        self.sample_rate = self.ui.samRate.text()
        self.mic_count = self.ui.micCount.text()
        self.total_spread = self.ui.totalSpread.text()
        print(self.sad + " " + self.sod + " " + self.sample_rate + " " + self.mic_count + " " + self.total_spread)
        # You can store these values for later use, or pass them as arguments in a subprocess call
        # Example: subprocess.run(["python", "some_script.py", self.sad, self.sod, self.sample_rate, self.mic_count, self.total_spread])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
