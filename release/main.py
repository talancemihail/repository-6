import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from main1 import Ui_MainWindow
from main2 import Ui_MainWindow2

class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data\coffee.db")
        self.update_result()
        self.pushButton.clicked.connect(self.new_coffee)
        self.pushButton_2.clicked.connect(self.update_coffee)

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("Select * from coffee").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        n = 0
        for i, elem in enumerate(result):
            n += 1
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.spinBox.setMaximum(n)

    def new_coffee(self):
        res = ['@', '', '', '', '', '', '']
        self.new_coffee = MyWidget2(res)
        self.new_coffee.show()
        self.close()

    def update_coffee(self):
        n = self.spinBox.value()
        cur = self.con.cursor()
        q = "Select * from coffee WHERE ID = " + str(n)
        result = cur.execute(q).fetchall()
        res = []
        for i in result[0]:
            res.append(i)
        self.new_coffee = MyWidget2(res)
        self.new_coffee.show()
        self.close()


class MyWidget2(QMainWindow, Ui_MainWindow2):
    def __init__(self, res):
        super().__init__()
        self.setupUi(self)
        self.lineEdit.setText(res[1])
        self.lineEdit_2.setText(res[2])
        self.lineEdit_3.setText(res[3])
        self.lineEdit_4.setText(res[4])
        self.lineEdit_5.setText(res[5])
        self.lineEdit_6.setText(res[6])
        self.n = res[0]
        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.cancellation)

    def save(self):
        a = self.lineEdit.text()
        b = self.lineEdit_2.text()
        cc = self.lineEdit_3.text()
        d = self.lineEdit_4.text()
        e = self.lineEdit_5.text()
        f = self.lineEdit_6.text()
        if bool(a) and bool(b) and bool(cc) and bool(d) and bool(e) and bool(f):
            con = sqlite3.connect('data\coffee.db')
            cur = con.cursor()
            if self.n != '@':
                res = "UPDATE coffee SET variety = {} WHERE ID = {}".format("'" + a + "'", self.n)
                cur.execute(res).fetchall()
                res = "UPDATE coffee SET degree = {} WHERE ID = {}".format("'" + b + "'", self.n)
                cur.execute(res).fetchall()
                res = "UPDATE coffee SET groundortgrains = {} WHERE ID = {}".format("'" + cc + "'", self.n)
                cur.execute(res).fetchall()
                res = "UPDATE coffee SET description = {} WHERE ID = {}".format("'" + d + "'", self.n)
                cur.execute(res).fetchall()
                res = "UPDATE coffee SET price = {} WHERE ID = {}".format("'" + e + "'", self.n)
                cur.execute(res).fetchall()
                res = "UPDATE coffee SET volume = {} WHERE ID = {}".format("'" + f + "'", self.n)
                cur.execute(res).fetchall()
            else:
                res = ("INSERT INTO coffee(variety, degree, groundortgrains, description, price, volume) " +
                       "VALUES('{}', '{}', '{}', '{}', '{}', '{}')").format(a, b, cc, d, e, f)
                cur.execute(res).fetchall()
            con.commit()
            con.close()
            self.ex = MyWidget()
            self.ex.show()
            self.close()

    def cancellation(self):
        self.ex = MyWidget()
        self.ex.show()
        self.close()

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
