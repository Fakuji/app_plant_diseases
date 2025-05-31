from classes import Ui_First_window_work
from PyQt6 import QtCore, QtGui, QtWidgets
import sys

if __name__ == "__main__":

    # Запускаем приложение
    app = QtWidgets.QApplication(sys.argv)
    # Создаем главное окно
    My_window = QtWidgets.QMainWindow()
    # Определяем дизайн
    ui = Ui_First_window_work()
    # Ставим дизайн
    ui.setupUi(My_window)
    # Показываем окно
    My_window.show()








    sys.exit(app.exec())