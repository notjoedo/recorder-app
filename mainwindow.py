# This Python file uses the following encoding: utf-8
import sys
import subprocess
import shutil
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connections
        self.ui.actionMenu.triggered.connect(self.import_py_file)
        self.ui.actionClear.triggered.connect(self.clear_console)
        self.ui.refreshList.clicked.connect(self.refresh_list)
        self.ui.saveButton.clicked.connect(self.save_settings)
        self.ui.deleteFile.clicked.connect(self.delete_selected_file)
        self.ui.runScript.clicked.connect(self.run_script)

        # Load Python files from the recorder directory
        self.load_python_files()

        # Variables to store input values
        self.sad = None
        self.sod = None
        self.samrate = None
        self.mic_count = None
        self.total_spread = None

    def clear_console(self):
        self.ui.consoleLog.clear()

    def import_py_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Python File", "", "Python Files (*.py)")
        if file_name:
            self.add_file_to_list_view(file_name)
            self.copy_file_to_recorder(file_name)

    def add_file_to_list_view(self, file_name):
        item = QListWidgetItem(os.path.basename(file_name))
        item.setData(1000, file_name)  # Store the full file path as user data
        self.ui.listView.addItem(item)

    def copy_file_to_recorder(self, file_name):
        destination_directory = "pythonfiles"
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        shutil.copy(file_name, os.path.join(destination_directory, os.path.basename(file_name)))
        self.load_python_files()

    def load_python_files(self):
        self.ui.listView.clear()
        destination_directory = "pythonfiles"
        if os.path.exists(destination_directory):
            for file_name in os.listdir(destination_directory):
                if file_name.endswith('.py'):
                    self.add_file_to_list_view(os.path.join(destination_directory, file_name))

    def refresh_list(self):
        self.load_python_files()

    def delete_selected_file(self):
        selected_item = self.ui.listView.currentItem()

        if selected_item is None:
            self.ui.consoleLog.append("No Selection: Please select a file to delete.")
            return

        file_path = selected_item.data(1000)

        confirm = "Yes"  # Simulating confirmation for deletion; you can adjust as needed
        if confirm == "Yes":
            if os.path.exists(file_path):
                os.remove(file_path)
                self.ui.listView.takeItem(self.ui.listView.row(selected_item))
                self.ui.consoleLog.append(f"Deleted: '{selected_item.text()}' has been deleted.")
            else:
                self.ui.consoleLog.append("Error: File not found.")

    def closeEvent(self, event):
        event.accept()

    def save_settings(self):
        self.sad = self.ui.SAD.text()
        self.sod = self.ui.SOD.text()
        self.samrate = self.ui.samRate.text()
        self.mic_count = self.ui.micCount.text()
        self.total_spread = self.ui.totalSpread.text()
        self.ui.consoleLog.append("Variables saved.\n\tSAD: " + self.sad + "\n\tSOD: " + self.sod + "\n\tSamrate: " + self.samrate + "\n\tMic Count: " + self.mic_count + "\n\tTotal Spread: " + self.total_spread)

    def run_script(self):
        selected_item = self.ui.listView.currentItem()

        if selected_item is None:
            self.ui.consoleLog.append("No Selection: Please select a Python file to run.")
            return

        script_path = selected_item.data(1000)

        if not script_path.endswith('.py'):
            self.ui.consoleLog.append("Invalid File: The selected file is not a Python file.")
            return

        args = [
            self.sad,
            self.sod,
            self.samrate,
            self.mic_count,
            self.total_spread
        ]

        try:
            result = subprocess.run(
                ["python", script_path] + args,
                capture_output=True,
                text=True,
                check=True
            )
            self.ui.consoleLog.append(result.stdout)

        except subprocess.CalledProcessError as e:
            self.ui.consoleLog.append(f"Error: {e.stderr}")

        except Exception as e:
            self.ui.consoleLog.append(f"Execution Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
