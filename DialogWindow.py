from PyQt5 import QtWidgets, QtGui
from Program_Logica import Data_base

class DialogAddWindow(QtWidgets.QDialog):
    def __init__(self, mainwindow, paren=None):
        super().__init__(paren)
        self.setupDialogAddWindow()
        self.mainwindow = mainwindow

    def setupDialogAddWindow(self):
        title_station = QtWidgets.QLabel('Title station')
        link_station = QtWidgets.QLabel('Link station')

        self.title_station_edit = QtWidgets.QLineEdit()
        self.link_station_edit = QtWidgets.QLineEdit()

        self.title_station_edit.displayText()

        self.title_station_edit.textChanged.connect(self.changer)
        self.link_station_edit.textChanged.connect(self.changer)

        self.btm_Save = QtWidgets.QPushButton('Save')

        self.btm_Save.setDisabled(True)
        self.btm_Save.clicked.connect(self.click_add_name_and_link_db)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title_station, 1, 0)
        grid.addWidget(self.title_station_edit, 1, 1)

        grid.addWidget(link_station, 2, 0)
        grid.addWidget(self.link_station_edit, 2, 1)

        grid.addWidget(self.btm_Save,3,1)

        self.setLayout(grid)

        framegeometry = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        framegeometry.moveCenter(centerPoint)
        self.move(framegeometry.topLeft())

        self.resize(460, 150)
        self.setMinimumSize(455, 135)
        self.setMaximumSize(600, 150)
        self.setWindowTitle("Maturym FM")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.show()

    def changer(self):

        title = self.title_station_edit.text()
        link = self.link_station_edit.text()
        if title == '' or link == '':
            self.btm_Save.setDisabled(True)
        else:
            self.btm_Save.setEnabled(True)


    def click_add_name_and_link_db(self):

        command_add_record = 'INSERT INTO STATION (name, link) VALUES (?, ?)'
        name = self.title_station_edit.text()
        link = self.link_station_edit.text()
        Data_base.cursor.execute(command_add_record, (name, link))
        Data_base.db.commit()

        self.close()

        self.mainwindow.comboBox_Name_Station.clear()
        self.mainwindow.set_name_station()

class DialogAboutWindow(QtWidgets.QDialog):
    def __init__(self,paren=None):
        super().__init__(paren)
        self.setupDialogAboutWindow()

    def setupDialogAboutWindow(self):

        Info_About = "Создатель: Markus Varckin\nВерсия: 1.02"
        title_About = QtWidgets.QLabel(Info_About)


        HBox = QtWidgets.QHBoxLayout()

        HBox.addWidget(title_About)

        self.setLayout(HBox)

        framegeometry = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        framegeometry.moveCenter(centerPoint)
        self.move(framegeometry.topLeft())

        self.setFixedSize(455,135)
        self.setWindowTitle("About")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.show()
