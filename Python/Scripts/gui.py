import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from design.design import Ui_MainWindow
from classes.inputs import Inputs
from classes.window import Window
import coordinates as coords
import win32gui

class NguScriptApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(NguScriptApp, self).__init__(parent)
        self.setupUi(self)  # generate the UI
        self.window_id = 0
        self.w = Window()
        self.i = Inputs()
        self.setup()

    def setup(self):
        """Add logic to UI elements."""
        self.rebirth_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.task_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.get_ngu_window()
        self.w_elapsed.hide()
        self.w_exp.hide()
        self.w_pp.hide()
        self.w_qp.hide()
        self.w_exph.hide()
        self.w_pph.hide()
        self.w_qph.hide()
        self.current_task_text.hide()
        self.task_progress.hide()
        self.current_rb_text.hide()
        self.rebirth_progress.hide()
        self.exit_button.clicked.connect(self.action_exit)
        self.run_button.clicked.connect(self.action_run)
        self.setFixedSize(self.sizeHint())  # shrink window

    def window_enumeration_handler(self, hwnd, top_windows):
        """Add window title and ID to array."""
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    def get_ngu_window(self):
        """Get window ID for NGU IDLE."""
        window_name = "debugg"
        top_windows = []
        win32gui.EnumWindows(self.window_enumeration_handler, top_windows)
        for i in top_windows:
            if window_name in i[1].lower():
                self.window_id = i[0]

        if self.window_id:
            self.window_retry.setText("Show Window")
            self.window_retry.clicked.connect(self.action_show_window)
            self.window_info_text.setText("Window detected!")
            self.get_top_left()
            if Window.x and Window.y:
                self.window_info_text.setStyleSheet("color: green")
                self.window_info_text.setText(f"Window detected! Game detected at: {Window.x}, {Window.y}")
            else:
                self.window_info_text.setText(f"Window detected, but game not found!")
                self.window_info_text.setStyleSheet("color: red")
        else:
            self.window_retry.clicked.connect(self.get_ngu_window)

    def get_top_left(self):
        """Get coordinates for top left of game."""
        Window.x, Window.y = self.i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
        print(Window.x, Window.y)
    def action_show_window(self):
        """Activate game window."""
        win32gui.ShowWindow(self.window_id, 5)
        win32gui.SetForegroundWindow(self.window_id)

    def action_exit(self):
        """Exit app."""
        sys.exit(0)

    def action_run(self):
        runs = ["Static Questing",
                "Static ITOPOD"]
        text = str(self.combo_run.currentText())
        run = runs.index(text)
        print(run)
        if run == 1:
            #import 
            print("value")

def run():
    """Start GUI thread."""
    app = QtWidgets.QApplication(sys.argv)
    GUI = NguScriptApp()
    GUI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

"""
Ideas

Progressbars tracking current long running task (sniping, questing)
Progressbar tracking run progression (if applicable)
Tools for annoying actions while playing manually (cap all diggers)
Quickstart for infinite questing/itopod sniping

"""