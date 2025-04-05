import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt6.QtCore import QThread, pyqtSignal
from shuba import 一键爬取

class CrawlerThread(QThread):
    finished = pyqtSignal()
    
    def __init__(self, link):
        super().__init__()
        self.link = link
        
    def run(self):
        一键爬取(self.link)
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("一键爬取")
        self.setGeometry(100, 100, 400, 150)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建输入框
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("请输入链接...")
        layout.addWidget(self.link_input)

        # 创建按钮
        self.process_button = QPushButton("爬取")
        self.process_button.clicked.connect(self.process_link)
        layout.addWidget(self.process_button)

    def process_link(self):
        link = self.link_input.text()
        # 在这里添加你的链接处理逻辑
        print(f"正在爬取链接: {link}")
        self.process_button.setEnabled(False)
        self.crawler_thread = CrawlerThread(link)
        self.crawler_thread.finished.connect(self.on_crawler_finished)
        self.crawler_thread.start()
        # 一键爬取(link)

    def on_crawler_finished(self):
        # 爬取完成后重新启用按钮
        self.process_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

# pyinstaller main.py