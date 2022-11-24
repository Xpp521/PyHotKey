# -*- coding: utf-8 -*-
# @Time    : 2022/11/11 12:17
# @Author  : Xpp
# @GitHub  : github.com/Xpp521
# @Email   : Xpp233@foxmail.com
"""
This is a small demo for recording hotkey.
"""
from sys import argv, exit
from PySide6.QtCore import Qt, Signal
from PyHotKey import keyboard_manager as manager
from PySide6.QtWidgets import QApplication, QDialog, QWidget, QLabel, QComboBox, QPushButton, QRadioButton, QLineEdit, \
    QTextEdit


class PushButton(QPushButton):
    def keyPressEvent(self, event):
        pass


class RadioButton(QRadioButton):
    def keyPressEvent(self, event):
        pass


class Dialog(QDialog):
    def keyPressEvent(self, event):
        pass


class AlertDialog(Dialog):
    def __init__(self, parent, title='Alert Dialog', text='Text'):
        super().__init__(parent=parent)
        self.setFixedSize(250, 150)
        self.setWindowTitle(title)
        self.label = QLabel(parent=self, text=text)
        self.label.setGeometry(25, 25, 200, 30)
        self.btn = PushButton(parent=self, text='OK')
        self.btn.setGeometry(25, 75, 200, 50)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.clicked.connect(self.accept)

    def open_(self, title, text):
        self.setWindowTitle(title)
        self.label.setText(text)
        super().open()


class RecordingHotKeyDialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Recording HotKey')
        self.setFixedSize(300, 400)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.label_type = QLabel(parent=self, text='HotKey type')
        self.label_type.setGeometry(25, 25, 200, 25)
        self.radio_btn_single_key = RadioButton('Single key', self)
        self.radio_btn_single_key.setGeometry(25, 50, 200, 25)
        self.radio_btn_single_key.setCursor(Qt.PointingHandCursor)
        self.radio_btn_multiple_key = RadioButton('Multiple key', self)
        self.radio_btn_multiple_key.setGeometry(25, 75, 200, 25)
        self.radio_btn_multiple_key.setCursor(Qt.PointingHandCursor)
        self.label_key_setting = QLabel(parent=self, text='Press your hotkey')
        self.label_key_setting.setGeometry(25, 130, 200, 25)
        self.line_keys = QLineEdit(self)
        self.line_keys.setGeometry(25, 160, 250, 25)
        self.line_keys.setReadOnly(True)
        self.line_keys.setFocusPolicy(Qt.NoFocus)
        self.label_repetitions = QLabel(parent=self, text='Repetitions')
        self.label_repetitions.setGeometry(25, 220, 200, 25)
        self.combo_repetitions = QComboBox(self)
        self.combo_repetitions.setGeometry(25, 250, 90, 25)
        self.combo_repetitions.setCursor(Qt.PointingHandCursor)
        self.combo_repetitions.addItem('')
        self.combo_repetitions.addItem('')
        self.combo_repetitions.addItem('')
        self.combo_repetitions.addItem('')
        self.combo_repetitions.setItemText(0, '2')
        self.combo_repetitions.setItemText(1, '3')
        self.combo_repetitions.setItemText(2, '4')
        self.combo_repetitions.setItemText(3, '5')
        self.btn_ok = PushButton(parent=self, text='OK')
        self.btn_ok.setCursor(Qt.PointingHandCursor)
        self.btn_ok.setGeometry(25, 310, 250, 30)
        self.btn_cancel = PushButton(parent=self, text='Cancel')
        self.btn_cancel.setObjectName('btn_cancel')
        self.btn_cancel.setGeometry(25, 350, 250, 30)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.keys = []
        self.radio_btn_multiple_key.toggled.connect(self.__radio_btn_multiple_key_toggled)
        self.radio_btn_single_key.toggled.connect(self.__radio_btn_single_key_toggled)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def __radio_btn_single_key_toggled(self, state):
        if state:
            manager.start_recording_hotkey_single(self.__set_keys)
            self.combo_repetitions.setEnabled(True)
        else:
            manager.stop_recording()
            self.__set_keys()

    def __radio_btn_multiple_key_toggled(self, state):
        if state:
            manager.start_recording_hotkey_multiple(self.__set_keys)
            self.combo_repetitions.setEnabled(False)
        else:
            manager.stop_recording()
            self.__set_keys()

    def __set_keys(self, list_=None):
        if list_ and isinstance(list_, list):
            self.line_keys.setText('+'.join([repr(k).strip("'") for k in list_]))
            self.keys = list_
        else:
            self.line_keys.clear()
            self.keys.clear()

    def open_(self, type_=2):
        self.__set_keys()
        if 1 == type_:
            if self.radio_btn_single_key.isChecked():
                self.__radio_btn_single_key_toggled(True)
            else:
                self.radio_btn_single_key.toggle()
        else:
            if self.radio_btn_multiple_key.isChecked():
                self.__radio_btn_multiple_key_toggled(True)
            else:
                self.radio_btn_multiple_key.toggle()
        super().open()

    def accept(self):
        manager.stop_recording()
        super().accept()

    def reject(self):
        manager.stop_recording()
        super().reject()

    @property
    def count(self):
        return int(self.combo_repetitions.currentText())


class MainWindow(QWidget):
    signal = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 300)
        self.setWindowTitle('Recording Example')
        self.dialog_recording = RecordingHotKeyDialog(self)
        self.dialog_alert = AlertDialog(self, 'Trigger Dialog')
        self.label = QLabel(parent=self, text='Hotkey list :')
        self.label.setGeometry(50, 25, 155, 30)
        self.text = QTextEdit(self)
        self.text.setGeometry(50, 60, 400, 100)
        self.text.setReadOnly(True)
        self.text.setFocusPolicy(Qt.NoFocus)
        self.btn = PushButton(parent=self, text='Record a new hotkey')
        self.btn.setGeometry(50, 175, 400, 100)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.clicked.connect(self.dialog_recording.open_)
        self.dialog_recording.finished.connect(self.__recording_dialog_finished)
        self.signal.connect(self.dialog_alert.open_)
        with open('Recording.qss', encoding='utf') as f:
            self.setStyleSheet(f.read())

    def __recording_dialog_finished(self, r):
        if QDialog.Accepted == r:
            i = manager.register_hotkey(lambda s: self.signal.emit('Hotkey triggered', s),
                                        self.dialog_recording.keys, self.dialog_recording.count,
                                        '+'.join([repr(k).strip("'") for k in self.dialog_recording.keys]))
            if -1 == i:
                self.dialog_alert.open_('Register failed', 'Already registered !')
            elif 0 == i:
                self.dialog_alert.open_('Register failed', 'Invalid parameters !')
            else:
                self.text.setText('\n'.join([repr(hotkey) for hotkey in manager.hotkeys]))


def main():
    app = QApplication(argv)
    manager.logger = True
    manager.set_log_file('Loggerrrrrrr.txt')
    window = MainWindow()
    window.show()
    exit(app.exec())


if __name__ == '__main__':
    main()
    # input()
