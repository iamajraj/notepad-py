import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QLabel, QStatusBar
from PyQt5.QtCore import Qt, QTimer, QObject, QEvent

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.font_size = 22
        self.init_ui()
        self.current_file = None

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Notepad')

        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet(f"font-size: {self.font_size}px; border-top: 1px solid #dbdbd9;")
        self.setCentralWidget(self.text_edit)
        self.text_edit.installEventFilter(self)
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu)

        self.status_bar = self.statusBar()
        self.info_label = QLabel()
        self.status_bar.addWidget(self.info_label, 1)

        self.github_label = QLabel('<a href="https://github.com/iamajraj" style="color: black;">GitHub</a>')
        self.github_label.setOpenExternalLinks(True)
        self.status_bar.addPermanentWidget(self.github_label)

        self.update_info_timer = QTimer(self)
        self.update_info_timer.timeout.connect(self.update_info)
        self.update_info_timer.start(200)

        self.create_menu_bar()

        self.show()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def new_file(self):
        self.text_edit.clear()
        self.current_file = None

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*.*)')
        if filename:
            self.current_file = filename
            with open(filename, 'r') as file:
                self.text_edit.setPlainText(file.read())

    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()

    def save_as_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*.*)')
        if filename:
            self.current_file = filename
            self.save_to_file(filename)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.text_edit.toPlainText())

    def closeEvent(self, event):
        if self.text_edit.toPlainText().strip() != "":
            reply = QMessageBox.question(self, 'Save Changes', 'Do you want to save changes?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                event.ignore()

    def update_info(self):
        cursor = self.text_edit.textCursor()
        cursor_pos = cursor.position()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1

        text = self.text_edit.toPlainText()
        lines = text.splitlines()
        word_count = sum(len(line.split()) for line in lines if line.strip())
        char_count = sum(len(line) for line in lines if line.strip())

        info_text = f"Line: {line}  |  Col: {col}  |  Words: {word_count}  |  Chars: {char_count}"
        self.info_label.setText(info_text)
    
    def show_context_menu(self, position):
        context_menu = self.text_edit.createStandardContextMenu()
        context_menu.setStyleSheet("font-size: 14px;")
        context_menu.exec_(self.text_edit.mapToGlobal(position))

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel and source is self.text_edit:
            if event.modifiers() & Qt.ControlModifier:
                font = self.text_edit.font()
                if event.angleDelta().y() > 0:
                    self.font_size += 1
                else:
                    self.font_size -= 1
                self.font_size = max(1, self.font_size)
                font.setPointSize(self.font_size)
                self.text_edit.setFont(font)
                self.text_edit.setStyleSheet(f"font-size: {self.font_size}px; border-top:1px solid #dbdbd9;")
                return True
        return super().eventFilter(source, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    notepad = Notepad()
    sys.exit(app.exec_())
