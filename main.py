# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtNetwork import QLocalSocket, QLocalServer
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMessageBox
from rc_resources import *   #noqa

class SingleApplication:
    """单实例应用管理器"""
    
    def __init__(self, app_id):
        self.app_id = app_id
        self.server = None
        
    def is_running(self):
        """检查应用是否已经在运行"""
        socket = QLocalSocket()
        socket.connectToServer(self.app_id)
        
        # 如果能连接成功,说明已经有实例在运行
        if socket.waitForConnected(500):
            socket.disconnectFromServer()
            return True
        
        # 创建本地服务器
        self.server = QLocalServer()
        # 先移除可能存在的旧服务器
        QLocalServer.removeServer(self.app_id)
        
        if not self.server.listen(self.app_id):
            return True
            
        return False


def main():
    # 设置应用标识
    QCoreApplication.setOrganizationName("ClockApp")
    QCoreApplication.setApplicationName("Clock")

    app = QApplication()
    app.setStyle("Fusion")

    # 单实例检查
    single_app = SingleApplication("ClockApp_SingleInstance")
    if single_app.is_running():
        print("应用已经在运行中!")
        QMessageBox.information(None, "信息", "应用已经在运行中!")
        sys.exit(0)
    
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
