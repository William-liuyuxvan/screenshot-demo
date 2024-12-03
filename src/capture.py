import win32gui
import win32ui
import win32con
from PIL import ImageGrab
from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QColor, QPainter, QScreen
import tempfile
import os

class SelectionWindow(QWidget):
    def __init__(self, screen_capture):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 获取主屏幕和设备像素比
        self.screen = QApplication.primaryScreen()
        self.device_pixel_ratio = self.screen.devicePixelRatio()
        
        # 获取实际的屏幕尺寸
        self.screen_geometry = self.screen.geometry()
        self.background = self.screen.grabWindow(0)
        
        # 设置窗口大小为实际屏幕大小
        self.setGeometry(self.screen_geometry)
        
        self.screen_capture = screen_capture
        self.begin = QPoint()
        self.end = QPoint()
        self.is_drawing = False
        
    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.is_drawing = True
        
    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        self.is_drawing = False
        self.capture_region()
        self.close()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background)
        
        if self.is_drawing:
            painter.fillRect(0, 0, self.width(), self.height(), 
                           QColor(0, 0, 0, 100))
            
            selection = QRect(self.begin, self.end).normalized()
            painter.drawPixmap(selection, self.background, selection)
            
            painter.setPen(QColor(255, 255, 255))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(selection)
            
    def capture_region(self):
        if self.begin and self.end:
            # 计算实际的像素坐标
            selection = QRect(self.begin, self.end).normalized()
            x = int(selection.x() * self.device_pixel_ratio)
            y = int(selection.y() * self.device_pixel_ratio)
            width = int(selection.width() * self.device_pixel_ratio)
            height = int(selection.height() * self.device_pixel_ratio)
            
            # 使用实际像素坐标进行截图
            screenshot = self.screen.grabWindow(
                0,
                x,
                y,
                width,
                height
            )
            
            image_path = os.path.join(tempfile.gettempdir(), 'screenshot.png')
            screenshot.save(image_path)
            os.startfile(image_path)
            
            from PIL import Image
            self.screen_capture.current_capture = Image.open(image_path)

class ScreenCapture:
    def __init__(self):
        self.current_capture = None
        self.selection_window = None

    def capture_full_screen(self):
        """捕获全屏"""
        screenshot = ImageGrab.grab()
        # 保存到临时文件并显示
        temp_path = os.path.join(tempfile.gettempdir(), 'screenshot.png')
        screenshot.save(temp_path)
        os.startfile(temp_path)  # 使用默认图片查看器打开
        self.current_capture = screenshot
        return screenshot

    def capture_region(self):
        """捕获选定区域"""
        self.selection_window = SelectionWindow(self)
        self.selection_window.show()

    def capture_window(self):
        """捕获当前活动窗口"""
        hwnd = win32gui.GetForegroundWindow()
        
        # 获取窗口尺寸
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        # 保存到临时文件并显示
        temp_path = os.path.join(tempfile.gettempdir(), 'screenshot.png')
        screenshot.save(temp_path)
        os.startfile(temp_path)
        
        self.current_capture = screenshot
        return screenshot

    def save_screenshot(self, parent=None):
        """保存截图到用户选择的位置"""
        if self.current_capture:
            file_path, _ = QFileDialog.getSaveFileName(
                parent,
                "保存截图",
                "screenshot.png",
                "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*.*)"
            )
            if file_path:
                self.current_capture.save(file_path)