from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
import sys
import sqlite3
import csv

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Maintenance Record")
        self.setGeometry(200, 200, 650, 570)
        self.initUI()
        self.initialize_data()
                
    #Main window form design
    def initUI(self):
        self.gridLayoutWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.gridLayoutWidget)
        self.gridLayoutWidget.setGeometry(10, 10, 630, 550)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setText("REFRESH")        
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 2)
        self.pushButton.clicked.connect(self.initialize_data)

        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.comboBox.activated.connect(self.select_car)
        
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.lineEdit.setReadOnly(True)
        
        self.lineEdit_1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_1, 3, 1, 1, 1)
        self.lineEdit_1.setReadOnly(True)
        
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_2, 4, 1, 1, 1)
        self.lineEdit_2.setReadOnly(True)
        
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setText("Id:")        
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_1.setText("Year:")        
        self.gridLayout.addWidget(self.label_1, 2, 0, 1, 1)
        
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setText("Make:")        
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setText("Model:")        
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        
        self.pushButton_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_1.setText("Add a new car")        
        self.gridLayout.addWidget(self.pushButton_1, 5, 0, 1, 2)
        self.pushButton_1.clicked.connect(self.add_a_new_car_clicked)
    
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(50)
        self.gridLayout.addWidget(self.tableWidget, 6, 0, 1, 2)
        self.tableWidget.setHorizontalHeaderLabels(["Entry #", "Car Id", "Date", "Description",
                                                    "Mileage (km)", "Cost ($)", "Comments"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)


        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setText("Add a new record")        
        self.gridLayout.addWidget(self.pushButton_2, 7, 0, 1, 2)
        self.pushButton_2.clicked.connect(self.add_a_new_record_clicked)
        
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setText("Extract to Excel")        
        self.gridLayout.addWidget(self.pushButton_3, 8, 0, 1, 2)
        self.pushButton_3.clicked.connect(self.extract_to_excel_clicked)

    #Initialize data on startup
    def initialize_data(self):
        self.initUI()
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS car
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        year INTEGER,
                        make TEXT,
                        model TEXT)
                        """)
        self.c.execute("""CREATE TABLE IF NOT EXISTS maintenance
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        car INTEGER,
                        date DATE,
                        description TEXT,
                        mileage TEXT,
                        cost INTEGER,
                        comments TEXT)
                        """)
        
        self.c.execute("""SELECT * from car""")
        self.car_records = self.c.fetchall()
        
        car_ids = []
        for row in self.car_records:
            car_ids.append(str(row[0]))
        self.comboBox.addItems(car_ids)
        if self.comboBox.currentText() != '':
            self.lineEdit.setText(str(self.car_records[int(self.comboBox.currentText())-1][1]))
            self.lineEdit_1.setText(str(self.car_records[int(self.comboBox.currentText())-1][2]))
            self.lineEdit_2.setText(str(self.car_records[int(self.comboBox.currentText())-1][3]))

        self.c.execute("""SELECT * from maintenance""")
        self.maintenance_records = self.c.fetchall()

        i = 0
        for row_number, row_data in enumerate(self.maintenance_records):
            if str(row_data[1]) == self.comboBox.currentText():
                self.tableWidget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = str(column_data)
                    self.tableWidget.setItem(i, column_number, QtWidgets.QTableWidgetItem(item))
                i = i + 1
                
        self.conn.commit()
        self.conn.close()
        
    #Load new record when user select a different car
    def select_car(self):
        self.lineEdit.setText(str(self.car_records[int(self.comboBox.currentText())-1][1]))
        self.lineEdit_1.setText(str(self.car_records[int(self.comboBox.currentText())-1][2]))
        self.lineEdit_2.setText(str(self.car_records[int(self.comboBox.currentText())-1][3]))

        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(50)

        i = 0
        for row_number, row_data in enumerate(self.maintenance_records):
            if str(row_data[1]) == self.comboBox.currentText():
                self.tableWidget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = str(column_data)
                    self.tableWidget.setItem(i, column_number, QtWidgets.QTableWidgetItem(item))
                i = i + 1
                
    def add_a_new_car_clicked(self):
        new_car_dialog = NewCar()
        new_car_dialog.exec_()

    def add_a_new_record_clicked(self):
        new_record_dialog = NewRecord()
        new_record_dialog.exec_()

    #Write maintenance data for the selected car to csv file
    def extract_to_excel_clicked(self):
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("""SELECT * from maintenance""")
        self.maintenance_records = self.c.fetchall()
        with open("maintenance_record.csv", "w", newline = "") as f:
            writer = csv.writer(f)
            for temp_row_number, temp_row_data in enumerate(self.maintenance_records):
                if str(temp_row_data[1]) == self.comboBox.currentText():      
                    writer.writerow(temp_row_data)
        done_dialog = Done()
        done_dialog.exec_()
        self.conn.commit()
        self.conn.close()

class NewCar(QDialog):
    def __init__(self):
        super(NewCar, self).__init__()
        self.setWindowTitle("Add New Car")
        self.setGeometry(300, 300, 250, 200)
        self.initUI()

    #Add a new car form design
    def initUI(self):
        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout()
        self.setLayout(self.gridLayout)

        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
               
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setText("Year:")        
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setText("Make:")        
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setText("Model:")        
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setText("Add")        
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 2)
        self.pushButton.clicked.connect(self.add_car_clicked)

    #Save new car data to database
    def add_car_clicked(self):
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("""INSERT INTO car(year, make, model)
                        VALUES(?,?,?)""", (self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        self.close()

class NewRecord(QDialog):
    def __init__(self):
        super(NewRecord, self).__init__()
        self.setWindowTitle("Add New Record")
        self.setGeometry(300, 300, 450, 400)
        self.initUI()

    #Add a new car form design
    def initUI(self):
        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout()
        self.setLayout(self.gridLayout)

        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_1, 1, 1, 1, 1)
        
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_3, 3, 1, 1, 1)

        self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_4, 4, 1, 1, 1)

        self.lineEdit_5 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_5, 5, 1, 1, 1)
               
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setText("Car ID:")        
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_1.setText("Date:")        
        self.gridLayout.addWidget(self.label_1, 1, 0, 1, 1)
        
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setText("Description:")        
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setText("Mileage:")        
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setText("Cost:")        
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setText("Comments:")        
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setText("Add")        
        self.gridLayout.addWidget(self.pushButton, 6, 0, 1, 2)
        self.pushButton.clicked.connect(self.add_record_clicked)

    #Save new maintenance record to database
    def add_record_clicked(self):
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("""INSERT INTO maintenance(car, date, description, mileage, cost, comments)
                        VALUES(?,?,?,?,?,?)""", (self.lineEdit.text(), self.lineEdit_1.text(),
                        self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text()))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        self.close()

class Done(QMessageBox):
    def __init__(self):
        super(Done, self).__init__()
        self.setGeometry(400, 400, 0, 0)
        self.setIcon = (QMessageBox.Information)
        self.setWindowTitle("Extracted")
        self.setText("Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
