from PyQt6 import QtCore, QtGui, QtWidgets
from first import Ui_First_window_base
from second import Ui_Second_window_base
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSlot
from PIL import Image
import numpy as np
from skimage import transform
import os
import pandas as pd

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import keras



class Ui_First_window_work(QtWidgets.QMainWindow, Ui_First_window_base):

    def __init__(self, ):

        super().__init__()
        self.dir = ''
        self.model = keras.saving.load_model("my_Xception.keras")

        self.dict_of_labels = {0:('Яблоня','Парша'),1:('Яблоня','Черный рак'),2:('Яблоня','Ржавчина'),3:('Яблоня','Здоровая'),
                               4:('Черника','Здоровая'),5:('Вишня','Здоровая'),6:('Вишня','Мучнистая роса'),
                               7:('Кукуруза ','Церкоспороз'),8:('Кукуруза ','Ржавчина'),9: ('Кукуруза ','Здоровая'), 10: ('Кукуруза ','Гельминтоспориоз'),
                               11: ('Виноград','Черный рак'), 12: ('Виноград','Еска'), 13: ('Виноград','Здоровый'), 14: ('Виноград','Пятнистость листьев Исариопсиса'),
                               15: ('Персик','Бактериальная пятнистость'), 16: ('Персик','Здоровый'),
                               17: ('Перец','Бактериальная пятнистость'),18: ('Перец','Здоровый'),
                               19: ('Картофель','Ранний фитофтороз '), 20: ('Картофель','Здоровый'), 21: ('Картофель','Поздний фитофтороз '),
                               22: ('Малина','Здоровый'), 23: ('Соя','Здоровый'),
                               24: ('Клубника','Здоровая'), 25: ('Клубника','Ожог листьев'),
                               26: ('Помидор','Бактериальная пятнистость'),27: ('Помидор','Ранний фитофтороз'), 28: ('Помидор','Здоровый'), 29: ('Помидор','Поздний фитофтороз'),
                               30: ('Помидор','Листовая плесень'), 31: ('Помидор','Септориоз листьев'), 32: ('Помидор','Паутинные клещи'), 33: ('Помидор','Коринеспора кассийская'),
                               34: ('Помидор','Вирус мозаики'), 35: ('Помидор','Вирус желтой курчавости листьев'),
                               }

        self.dict_of_rec = {0: 'Обработка фунгицидом.',
                            1: 'Удаление пораженных частей.',
                            2: 'Обработка фунгицидом.',
                            3: 'Рекомендация не нужна',
                            4: 'Рекомендация не нужна.',
                            5: 'Рекомендация не нужна.',
                            6: 'Обработка фунгицидом.',
                            7: 'Устранение пораженных растений.',
                            8: 'Обработка фунгицидом.',
                            9: 'Рекомендация не нужна.',
                            10: 'Обработка фунгицидом.',
                            11: 'Удаление пораженных участков.',
                            12: 'Специализированные препараты использовать.',
                            13: 'Рекомендация не нужна.',
                            14: 'Обработка фунгицидом.',
                            15: 'Удаление пораженных листьев.',
                            16: 'Рекомендация не нужна.',
                            17: 'Медьсодержащие препараты использовать.',
                            18: 'Рекомендация не нужна.',
                            19: 'Обработка фунгицидом.',
                            20: 'Рекомендация не нужна',
                            21: 'Обработка фунгицидом.',
                            22: 'Рекомендация не нужна.',
                            23: 'Рекомендация не нужна.',
                            24: 'Рекомендация не нужна.',
                            25: 'Устранение пораженных листьев.',
                            26: 'Обработка медьсодержащими препаратами.',
                            27: 'Обработка фунгицидом.',
                            28: 'Рекомендация не нужна',
                            29: 'Обработка фунгицидом.',
                            30: 'Обработка фунгицидом.',
                            31: 'Обработка фунгицидом.',
                            32: 'Инсектицидная обработка.',
                            33: 'Обработка фунгицидом.',
                            34: 'Устранение зараженных растений.',
                            35: 'Удаление зараженных растений.'}



    def setupUi(self,get):

        self.actual_window = get
        Ui_First_window_base.setupUi(self, get)

        self.add_funcs()

    def add_funcs(self,):

        self.Choose_dir.clicked.connect(self.browse_button)
        self.Start_pred.clicked.connect(self.make_predictions)

    def load(self, filename):

        np_image = Image.open(filename)
        np_image = np.array(np_image).astype('float32')/255
        np_image = transform.resize(np_image, (256, 256, 3))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image

    def make_predictions(self):

        if self.dir == '':

            pass

        else:
            try:
                images = []
                for i in os.listdir(self.dir):

                    images.append(self.load(f'{self.dir}/{i}'))

                images = np.array(images).reshape(len(os.listdir(self.dir)),256,256,3)

                self.preds = list(self.model.predict(images).argmax(1))
                files = os.listdir(self.dir)
                for i in range(len(self.preds)):
                    one = self.dict_of_labels[self.preds[i]]
                    self.preds[i] = (files[i],one[0], one[1], self.dict_of_rec[self.preds[i]])

                print(self.preds)
                self.open_window()
            except Exception as e:

                print(e)




    def open_window(self):


        # Создаем новое окно
        self.My_window = QtWidgets.QMainWindow()
        # Определяем дизайн
        self.ui_2 = Ui_Second_window_work(self.preds)
        # Ставим дизайн
        self.ui_2.setupUi(self.actual_window)

        self.actual_window.show()






    @pyqtSlot()
    def browse_button(self):

        self.dir = QFileDialog.getExistingDirectory(self,
            "Open File",
            "${HOME}",)

        self.label_2.setText(self.dir)


class Ui_Second_window_work(QtWidgets.QMainWindow, Ui_Second_window_base):

    def __init__(self, preds):
        super().__init__()
        self.preds = preds





    def setupUi(self,get):

        self.actual_window = get
        Ui_Second_window_base.setupUi(self, get)

        self.fill_table()

        self.add_funcs()

    def fill_table(self):

        for i in range(len(self.preds)):
            print(self.preds)
            self.Results.insertRow(i)
            self.Results.setItem(i, 0, QtWidgets.QTableWidgetItem(self.preds[i][0]))
            self.Results.setItem(i, 1, QtWidgets.QTableWidgetItem(self.preds[i][1]))
            self.Results.setItem(i, 2, QtWidgets.QTableWidgetItem(self.preds[i][2]))
            self.Results.setItem(i, 3, QtWidgets.QTableWidgetItem(self.preds[i][3]))




    def add_funcs(self):

        self.Back_1_window.clicked.connect(self.open_window)
        self.Excel_b.clicked.connect(self.to_excel)
        self.CSV_B.clicked.connect(self.to_csv)


    def to_csv(self):
        dataset = pd.DataFrame(self.preds)
        dataset.to_csv('results.csv', index=False)



    def to_excel(self):

        dataset = pd.DataFrame(self.preds)
        dataset.to_excel('results.xlsx', index=False)

    def open_window(self):


        # Создаем новое окно
        self.My_window = QtWidgets.QMainWindow()
        # Определяем дизайн
        self.ui_2 = Ui_First_window_work()
        # Ставим дизайн
        self.ui_2.setupUi(self.actual_window)

        self.actual_window.show()