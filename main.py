import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, \
    QPlainTextEdit
from dotenv import load_dotenv
from BackgroundWorker import BackgroundWorker


class MoveFlowsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.flow_id_label = None
        self.flow_id_entry = None
        self.get_flow_button = None
        self.output = None

        self.__thread = QThread()

        load_dotenv()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Move Flows')
        self.output = QPlainTextEdit()
        self.get_flow_button = QPushButton('Move AFs')
        self.get_flow_button.clicked.connect(self.get_flow_config)

        layout = QVBoxLayout()
        layout.addWidget(self.get_flow_button)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def update_text(self, text):
        self.output.appendPlainText(text)

    def update_finished(self):
        self.output.appendPlainText('Finished')
        self.__thread.quit()

    def __getThread(self):
        thread = QThread()
        worker = BackgroundWorker()
        worker.moveToThread(thread)
        thread.worker = worker
        thread.started.connect(worker.run)
        worker.update.connect(lambda msg: self.update_text(msg))
        worker.finished.connect(lambda: self.update_finished())

        return thread

    def get_flow_config(self):
        if not self.__thread.isRunning():
            self.__thread = self.__getThread()
            self.__thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MoveFlowsApp()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec_())
