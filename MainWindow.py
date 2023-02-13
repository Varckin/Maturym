import sys, re, time, pyperclip, vlc, datetime

from PyQt5 import QtWidgets, QtCore, QtGui
from Program_Logica import Data_base

class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupMainWindow()

    def setupMainWindow(self):

        self.count_timer = 0
        self.timeInterval = 1000
        self.flag_bool = False

        self.vlcInstance = vlc.Instance()
        self.vlcplayer = self.vlcInstance.media_player_new()

        self.label_NameMusic = QtWidgets.QLabel('')
        self.label_Time_stopwatch = QtWidgets.QLabel('')
        label_empty1 = QtWidgets.QLabel('')

        self.label_NameMusic.setFixedSize(360,25)
        self.label_NameMusic.mousePressEvent = self.click_copy_namemusic_clipboard

        self.btm_Delete_Station = QtWidgets.QPushButton('Delete station')
        self.btm_Add_Station = QtWidgets.QPushButton('Add station')
        self.btm_Stop_Start_Playback = QtWidgets.QPushButton('Start')
        self.btm_About = QtWidgets.QPushButton('About')

        self.btm_Stop_Start_Playback.setFixedSize(120,30)
        self.btm_About.setFixedSize(50,30)

        self.btm_Add_Station.clicked.connect(self.click_Add_Station)
        self.btm_Stop_Start_Playback.clicked.connect(self.click_Start_and_Stop)
        self.btm_About.clicked.connect(self.click_About)
        self.btm_Delete_Station.clicked.connect(self.click_delete_station)

        self.comboBox_Name_Station = QtWidgets.QComboBox()
        self.set_name_station()

        self.volumeslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)

        self.volumeslider.setMaximum(100)
        self.volumeslider.setToolTip("Volume 100")
        self.volumeslider.setValue(self.vlcplayer.audio_get_volume())
        self.volumeslider.valueChanged.connect(self.set_volume)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(2)

        hBox1 = QtWidgets.QHBoxLayout()
        hBox1.addWidget(self.btm_Delete_Station)
        hBox1.addWidget(self.btm_Add_Station)

        hBox2 = QtWidgets.QHBoxLayout()
        hBox2.addWidget(self.btm_Stop_Start_Playback)
        hBox2.addWidget(self.volumeslider)

        hBox3 = QtWidgets.QHBoxLayout()
        hBox3.addWidget(self.btm_About)

        grid.addWidget(label_empty1,0,0)
        grid.addWidget(self.label_NameMusic, 1, 1)
        grid.addWidget(self.label_Time_stopwatch, 1, 3)
        grid.addWidget(self.comboBox_Name_Station, 2, 0, 1, 4)
        grid.addLayout(hBox1,3,2,1,2)
        grid.addLayout(hBox2,4,1)
        grid.addLayout(hBox3,4,3)

        self.setLayout(grid)

        framegeometry = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        framegeometry.moveCenter(centerPoint)
        self.move(framegeometry.topLeft())
        self.resize(460,150)
        self.setMinimumSize(455,135)
        self.setMaximumSize(600,150)
        self.setWindowTitle("Maturym FM")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.thread_instance = GetData(mainWindow=self)

    def click_Add_Station(self):
        from DialogWindow import DialogAddWindow

        self.dialog_window = DialogAddWindow(mainwindow=self)

    def click_About(self):
        from DialogWindow import DialogAboutWindow

        self.Aboutwindow = DialogAboutWindow()

    def click_Start_and_Stop(self):

        if self.vlcplayer.is_playing():
            self.vlcplayer.pause()

            self.thread_instance.terminate()

            self.flag_bool = False
            self.timer.stop()
            self.count_timer = 0
            self.label_Time_stopwatch.setText(time.strftime('%H:%M:%S', time.gmtime(self.count_timer)))

            self.btm_Stop_Start_Playback.setText("Start")

        else:
            station = self.comboBox_Name_Station.currentText()
            db_requst = "SELECT name, link FROM STATION WHERE name = ?"
            link_db = Data_base.cursor.execute(db_requst,(station,))

            self.url = link_db.fetchone()[1]

            self.link_station = self.vlcInstance.media_new(self.url)
            self.link_station.get_mrl()

            self.vlcplayer.set_media(self.link_station)
            self.vlcplayer.play()

            self.thread_instance.start()

            self.time_second()
            self.flag_bool = True

            self.btm_Stop_Start_Playback.setText("Stop")

    def set_volume(self, volume):
        self.vlcplayer.audio_set_volume(volume)
        self.volumeslider.setToolTip("Volume " + str(self.vlcplayer.audio_get_volume()))

    def set_name_station(self):
        data_name_station = Data_base.cursor.execute("SELECT name FROM STATION ORDER BY name ASC")
        for i in data_name_station:
            data_name = str(i)
            self.comboBox_Name_Station.addItem(re.sub("[^A-Za-z0-9-А-Яа-яЁ-ё ]", "", data_name))

    def click_copy_namemusic_clipboard(self, *arg, **kwargs):
        pyperclip.copy(self.label_NameMusic.text())

    def time_second(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.setInterval(self.timeInterval)
        self.timer.start()

    def showTime(self):
        if self.flag_bool:
            self.count_timer += 1
        self.label_Time_stopwatch.setText(time.strftime('%H:%M:%S', time.gmtime(self.count_timer)))

    def click_delete_station(self):
        command_delete = 'DELETE FROM STATION WHERE name = ?'
        name_str = self.comboBox_Name_Station.currentText()
        Data_base.cursor.execute(command_delete, (name_str,))
        Data_base.db.commit()

        self.comboBox_Name_Station.clear()
        self.set_name_station()

class GetData (QtCore.QThread):

    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.mainwindow = mainWindow

    def run(self):
        prev = ""

        while True:
            time.sleep(1)
            m = self.mainwindow.link_station.get_meta(12)

            if m != prev:
                print("Now playing", m)
                prev = m
                self.mainwindow.label_NameMusic.setText(m)

                name_file = self.mainwindow.comboBox_Name_Station.currentText()
                text = self.mainwindow.label_NameMusic.text()
                with open(name_file+'.txt', 'at') as file:
                    file.write(datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")+' - '+text+'\n')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())