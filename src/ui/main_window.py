from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QToolBar, QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from ..capture import ScreenCapture

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("截图工具")
        self.setMinimumSize(200, 150)
        
        # 初始化截图工具
        self.screen_capture = ScreenCapture()
        
        # 创建主界面
        self.init_ui()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # 添加按钮
        self.full_screen_btn = QPushButton("全屏截图")
        self.region_screen_btn = QPushButton("区域截图")
        self.window_screen_btn = QPushButton("窗口截图")
        
        layout.addWidget(self.full_screen_btn)
        layout.addWidget(self.region_screen_btn)
        layout.addWidget(self.window_screen_btn)
        
        # 连接信号
        self.full_screen_btn.clicked.connect(self.screen_capture.capture_full_screen)
        self.region_screen_btn.clicked.connect(self.screen_capture.capture_region)
        self.window_screen_btn.clicked.connect(self.screen_capture.capture_window)
        
        central_widget.setLayout(layout)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 添加工具栏按钮
        save_action = QAction("保存", self)
        save_action.setStatusTip("保存截图")
        save_action.triggered.connect(lambda: self.screen_capture.save_screenshot(self))
        toolbar.addAction(save_action)
        
        edit_action = QAction("编辑", self)
        edit_action.setStatusTip("编辑截图")
        toolbar.addAction(edit_action) 