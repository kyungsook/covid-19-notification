import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import DBManager
import Calculator

ACCEPT = 0
CANCEL = -1

# implement dialog for input "region, latitude, longitude"
class InputWidget(QDialog):
    def __init__(self, title):
        super().__init__()

        self.mode = CANCEL

        self.initUI(title)

        self.exec_()

    def initUI(self, title):
        self.setWindowTitle(title)

        # Label to print "region, latitude, longitude"
        regionLabel = QLabel("&지역:")
        latitudeLabel = QLabel("&위도:")
        longitudeLabel = QLabel("&경도: ")

        # text color: white
        regionLabel.setStyleSheet("color: white")
        latitudeLabel.setStyleSheet("color: white")
        longitudeLabel.setStyleSheet("color: white")

        # LineEdit for inputs
        self.regionLineEdit = QLineEdit()
        self.latitudeLineEdit = QLineEdit()
        self.longitudeLineEdit = QLineEdit()

        # text color: white
        self.regionLineEdit.setStyleSheet("color: white")
        self.latitudeLineEdit.setStyleSheet("color: white")
        self.longitudeLineEdit.setStyleSheet("color: white")

        regionLabel.setBuddy(self.regionLineEdit)
        latitudeLabel.setBuddy(self.latitudeLineEdit)
        longitudeLabel.setBuddy(self.longitudeLineEdit)

        validator = QDoubleValidator(self)
        self.latitudeLineEdit.setValidator(validator)
        self.longitudeLineEdit.setValidator(validator)

        self.inputBox = QWidget()
        self.buttonBox = QWidget()

        # Buttons (Ok, Cancel)
        okButton = QPushButton("&OK")
        okButton.setDefault(True)
        okButton.clicked.connect(self.okButton_on_clicked)

        cancelButton = QPushButton("&Cancel")
        cancelButton.clicked.connect(self.cancelButton_on_clicked)

        # set layouts
        gridLayout = QGridLayout()
        gridLayout.addWidget(regionLabel, 0, 0)
        gridLayout.addWidget(self.regionLineEdit, 0, 1)
        gridLayout.addWidget(latitudeLabel, 1, 0)
        gridLayout.addWidget(self.latitudeLineEdit, 1, 1)
        gridLayout.addWidget(longitudeLabel, 2, 0)
        gridLayout.addWidget(self.longitudeLineEdit, 2, 1)
        self.inputBox.setLayout(gridLayout)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.inputBox)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        self.show()

    def okButton_on_clicked(self):
        # get inputs from LineEdit
        self.mode = ACCEPT
        self.myRegion = self.regionLineEdit.text()
        self.myLatitude = float(self.latitudeLineEdit.text())
        self.myLongitude = float(self.longitudeLineEdit.text())
        self.accept()

    def cancelButton_on_clicked(self):
        self.mode = CANCEL
        self.reject()

class App(QMainWindow, QWidget):
    NORMAL = 0
    VERY_DANGER = 1
    SEMI_DANGER = 2

    # Height of Notification image
    NORMAL_HEIGHT = 160
    NOTIFI_HEIGHT = 240
    OTHER_HEIGHT = 130

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Talking Potatoes')

        # Center the window.
        qtFrame = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtFrame.moveCenter(centerPoint)
        self.resize(700, 700)

        # Create mainViewWidget
        self.mainViewWidget = QWidget()
        self.mainViewWidget.setLayout(self.createMainView())

        self.setCentralWidget(self.mainViewWidget)

        self.show()

    def createMainView(self):
        totalLayout = QHBoxLayout()

        totalWidget = QWidget()
        totalWidget.setStyleSheet("background-color: white;"
                                  "border-radius: 40px;")
        totalWidget.setFixedSize(630, 630)

        # 3 notifications are displayed
        self.mainLayout = QVBoxLayout()
        self.notiText1 = QLabel()
        self.notiText2 = QLabel()
        self.notiText3 = QLabel()

        """
        self.notiText1.setFixedSize(550, 240)
        self.notiText2.setFixedSize(550, 130)
        self.notiText3.setFixedSize(550, 130)
        """

        self.notiText1.setFixedSize(550, 160)
        self.notiText2.setFixedSize(550, 160)
        self.notiText3.setFixedSize(550, 160)

        self.notiText1.setStyleSheet("background-color: #c0c0c0;"
                                     "border-radius: 20px;")
        self.notiText2.setStyleSheet("background-color: #c0c0c0;"
                                     "border-radius: 20px;")
        self.notiText3.setStyleSheet("background-color: #c0c0c0;"
                                     "border-radius: 20px;")

        font = QFont("나눔스퀘어 Bold", QFont.Normal, False)
        self.notiText1.setFont(font)
        self.notiText2.setFont(font)
        self.notiText3.setFont(font)

        # Set text of notifications
        self.notiText1.setText(
            "<p style=\"font-size:25px\"><font color=\"#88EEFF\">&nbsp; &nbsp; &nbsp;●</font> 날씨 &nbsp;|  &nbsp;Bixby 제안</p>"
            "<p style=\"font-size:30px\"> &nbsp; &nbsp;  대구광역시의 날씨 보기</p>")
        self.notiText1.setWordWrap(True)
        self.notiText1.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.notiText2.setText(
            "<p style=\"font-size:25px\"><font color=\"#FF6699\">&nbsp; &nbsp; &nbsp;●</font> 인스타그램 알림</p>"
            "<p style=\"font-size:30px\"> &nbsp; &nbsp; 최감자님이 스토리를 올렸습니다.</p>")
        self.notiText2.setWordWrap(True)
        self.notiText2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.notiText3.setText(
            "<p style=\"font-size:25px\"><font color=\"yellow\">&nbsp; &nbsp; &nbsp;●</font> 감자톡 알림</p>"
            "<p style=\"font-size:30px\"> &nbsp; &nbsp; 김감자: 햄버거 먹으러 가자!!!!!</p>")
        self.notiText3.setWordWrap(True)
        self.notiText3.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # add widgets to mainLayout
        self.mainLayout.addWidget(self.notiText1, 1, Qt.AlignHCenter)
        self.mainLayout.addWidget(self.notiText2, 1, Qt.AlignHCenter)
        self.mainLayout.addWidget(self.notiText3, 1, Qt.AlignHCenter)

        totalWidget.setLayout(self.mainLayout)

        totalLayout.addWidget(totalWidget, Qt.AlignCenter)
        return totalLayout

    def keyPressEvent(self, e):
        # press enter key to display Dialog
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.user = InputWidget("My Location")

            # if user clicked "OK" button
            if self.user.mode != CANCEL:
                # connect DB to get info
                self.db = DBManager.DBManager('./path.db')

                self.adjacent = self.db.select_data(self.user.myRegion)
                self.userloc = (self.user.myLatitude, self.user.myLongitude)

                adjList = Calculator.adjacent_list(self.userloc, self.adjacent)

                if adjList[0] == self.VERY_DANGER:
                    self.showScreen(self.VERY_DANGER, adjList)

                elif adjList[0] == self.SEMI_DANGER:
                    self.showScreen(self.SEMI_DANGER, adjList)

                self.db.close_db()

    # show infos on the notification
    def showScreen(self, mode, adjList):

        # red notification
        if mode == self.VERY_DANGER:
            self.notiText1.setFixedSize(550, 240)
            self.notiText2.setFixedSize(550, 130)
            self.notiText3.setFixedSize(550, 130)

            self.notiText1.setStyleSheet("background-color: red;"
                                         "border-radius: 20px;")

            self.notiText1.setText("<p style=\"font-size:33px\">위험! 해당 지역은 "
                                   "<font color=white>" + adjList[1][5] + "</font></p>"
                                   "<p style=\"font-size:33px\">확진자가 방문한 경로입니다!</p>"
                                   "<p style=\"font-size:33px\">방역일: " + adjList[1][6] +"</p>"
                                   "<p style=\"font-size: 30px\"><font color=white> 장소: </font>" + adjList[1][2] +"</p>")
            self.notiText1.setWordWrap(True)
            self.notiText1.setAlignment(Qt.AlignCenter)

            self.notiText2.setText(
                "<p style=\"font-size:25px\"><font color=\"yellow\">&nbsp; &nbsp; &nbsp;●</font> 감자톡 알림</p>"
                "<p style=\"font-size:30px\"> &nbsp; &nbsp; 김감자: 자니?</p>")
            self.notiText2.setWordWrap(True)
            self.notiText2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.notiText3.setText(
                "<p style=\"font-size:25px\"><font color=\"yellow\">&nbsp; &nbsp; &nbsp;●</font> 감자톡 알림</p>"
                "<p style=\"font-size:30px\"> &nbsp; &nbsp; 김감자: 잘 지내?</p>")
            self.notiText3.setWordWrap(True)
            self.notiText3.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # yello notification
        elif mode == self.SEMI_DANGER:
            self.notiText1.setFixedSize(550, 240)
            self.notiText2.setFixedSize(550, 130)
            self.notiText3.setFixedSize(550, 130)

            self.notiText1.setStyleSheet("background-color: #FFD966;"
                                         "border-radius: 20px;")

            self.notiText1.setText("<p style=\"font-size:33px\">경고! 해당 지역은 "
                                   "<font color=red>" + adjList[1][5] + "</font></p>"
                                   "<p style=\"font-size:33px\">확진자가 방문한 경로입니다!</p>"
                                   "<p style=\"font-size:33px\">방역일: " +
                                   adjList[1][6] + "</p>"
                                   "<p style=\"font-size: 30px\"><font color = red>장소: </font>"
                                   + adjList[1][2] + "</p>")
            self.notiText1.setWordWrap(True)
            self.notiText1.setAlignment(Qt.AlignCenter)

            self.notiText2.setText(
                "<p style=\"font-size:25px\"><font color=\"#88EEFF\">&nbsp; &nbsp; &nbsp;●</font> 날씨 &nbsp;|  &nbsp;Bixby 제안</p>"
                "<p style=\"font-size:30px\"> &nbsp; &nbsp;  대구광역시의 날씨 보기</p>")
            self.notiText2.setWordWrap(True)
            self.notiText2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.notiText3.setText(
                "<p style=\"font-size:25px\"><font color=\"#2E75B6\">&nbsp; &nbsp; &nbsp;●</font> 포이스북 알림</p>"
                "<p style=\"font-size:30px\"> &nbsp; &nbsp; 이감자님의 새로운 소식을 확인하세요</p>")
            self.notiText3.setWordWrap(True)
            self.notiText3.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.mainLayout.addWidget(self.notiText1, 1, Qt.AlignHCenter)
        self.mainLayout.addWidget(self.notiText2, 1, Qt.AlignHCenter)
        self.mainLayout.addWidget(self.notiText3, 1, Qt.AlignHCenter)

        return self.mainLayout

def setStyle(qApp):
    qApp.setStyle("Fusion")

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, Qt.black)
    dark_palette.setColor(QPalette.WindowText, Qt.black)
    dark_palette.setColor(QPalette.Base, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.AlternateBase, Qt.black)
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.black)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.white)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    qApp.setPalette(dark_palette)

    qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


if __name__ == '__main__':
   app = QApplication(sys.argv)
   setStyle(app)
   ex = App()
   sys.exit(app.exec_())