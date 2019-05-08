from PyQt4 import QtCore, QtGui
import sys
import signal
import bluetooth as bt
from struct import pack, unpack
#import qdarkstyle

class SelfieApplication(QtGui.QMainWindow):
    def __init__(self):
        super(SelfieApplication, self).__init__()

        self.selfieAddress = self.getAddressFromFile()
        self.communicationPort = 1
        self.socket = bt.BluetoothSocket(bt.RFCOMM)
        self.connected = False

        self.icon = QtGui.QIcon("./a.png")
        self.setWindowIcon(self.icon)
        self.setWindowTitle("selfieApplication")
        self.showMaximized()
        self.resetVisionButton = QtGui.QPushButton()
        self.KDLabel = QtGui.QLabel()
        self.KDSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.KDLineEdit = QtGui.QLineEdit()
        self.KDPushButton = QtGui.QPushButton()
        self.KPLabel = QtGui.QLabel()
        self.KPSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.KPLineEdit = QtGui.QLineEdit()
        self.KPPushButton = QtGui.QPushButton()
        self.KILabel = QtGui.QLabel()
        self.KISlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.KILineEdit = QtGui.QLineEdit()
        self.KIPushButton = QtGui.QPushButton()
        self.KIPushButton.clicked.connect(self.changeKI)
        self.KDPushButton.clicked.connect(self.changeKD)
        self.KPPushButton.clicked.connect(self.changeKP)
        self.connectionProgressBar = QtGui.QProgressBar()
        self.connectionLabel = QtGui.QLabel()
        self.groupBoxStyle = """QGroupBox#Group {
        border-width: 2px;
        border-style: solid;
        border-color: lightgray;
        border-radius: 4px;
        font: bold 18px;
        padding: 20 0px;}
        QGroupBox::title {
        background: transparent;
        padding: 2 7px;}
        """
        self.toolBar = QtGui.QToolBar()
        self.connectSelfieButton = QtGui.QPushButton("Connect to Selfie")
        self.connectSelfieButton.clicked.connect(self.connectToSelfie)
        self.disconnectSelfieButton = QtGui.QPushButton("Disconnect")
        self.disconnectSelfieButton.clicked.connect(self.disconnectFromSelfie)
        self.changeMACButton = QtGui.QPushButton("Change Selfie's MAC adress")
        #self.changeMACButton.clicked.connect()
        self.toolBar.addWidget(self.connectSelfieButton)
        self.toolBar.addWidget(self.disconnectSelfieButton)
        self.toolBar.addWidget(self.changeMACButton)
        self.toolBar.setMovable(False)
        self.addToolBar(self.toolBar)

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.setCentralWidget(self.createCentralWidget())
        self.statusBar = self.CustomStatusBar(self.connectionLabel, self.connectionProgressBar)
        self.setStatusBar(self.statusBar)

        self.widgets = [self.KIPushButton, self.KDPushButton, self.KPPushButton, self.KISlider, self.KDSlider, self.KPSlider]
        self.changeMACButton.clicked.connect(self.conn)



    def createCentralWidget(self):
        tabWidget = QtGui.QTabWidget()
        firstTab = self.createFirstTab()
        tabWidget.addTab(firstTab,"first tab")
        return tabWidget

    def createFirstTab(self):
        firstTabLayout = QtGui.QGridLayout()
        firstTab = QtGui.QWidget()
        inputGroup = QtGui.QGroupBox("input")
        inputGroup.setObjectName("Group")
        inputGroup.setStyleSheet(self.groupBoxStyle)
        inputLayout = QtGui.QFormLayout()
        inputLayout.addWidget(self.createPIDWidget())
        inputLayout.addWidget(self.createVisionResetWidget())
        inputGroup.setLayout(inputLayout)
        outputGroup = QtGui.QGroupBox("output")

        outputGroup.setObjectName("Group")
        outputGroup.setStyleSheet(self.groupBoxStyle)
        outputSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        outputSizePolicy.setHorizontalStretch(1)
        inputSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        inputSizePolicy.setHorizontalStretch(2)
        outputGroup.setSizePolicy(outputSizePolicy)
        inputGroup.setSizePolicy(inputSizePolicy)
        outputGroup.setMinimumWidth(250)

        outputLayout = QtGui.QFormLayout()
        outputLayout.addWidget(self.createFlagWidget())
        outputGroup.setLayout(outputLayout)
        firstTabLayout.addWidget(inputGroup, 0, 0)
        firstTabLayout.addWidget(outputGroup, 0, 1)
        firstTab.setLayout(firstTabLayout)
        return firstTab



    def createPIDWidget(self):
        PIDWidgetGroup = QtGui.QGroupBox("PID")
        PIDLayout = QtGui.QGridLayout()
        PIDLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.KPLabel.setText("NA")
        self.KDLabel.setText("NA")
        self.KILabel.setText("NA")
        self.KDSlider.setEnabled(False)
        self.KDSlider.setMaximum(20)
        self.KDSlider.setMinimum(0)
        self.KDSlider.setValue(0)
        self.KDSlider.setTickInterval(0.1)
        self.KDSlider.setMinimumWidth(100)
        self.KDSlider.setMaximumWidth(300)
        self.KDLineEdit.setMaximumWidth(100)
        self.KDPushButton.setMaximumWidth(150)
        self.KDLabel.setMaximumWidth(100)
        self.KPSlider.setMaximum(20)
        self.KPSlider.setMinimum(0)
        self.KPSlider.setValue(0)
        self.KPSlider.setMinimumWidth(100)
        self.KPSlider.setMaximumWidth(300)
        self.KPLineEdit.setMaximumWidth(100)
        self.KPLabel.setMaximumWidth(100)
        self.KPPushButton.setMaximumWidth(150)
        self.KPSlider.setTickInterval(0.1)
        self.KISlider.setMaximum(20)
        self.KISlider.setMinimum(0)
        self.KISlider.setValue(0)
        self.KISlider.setTickInterval(0.1)
        self.KISlider.setMinimumWidth(100)
        self.KISlider.setMaximumWidth(300)
        self.KILineEdit.setMaximumWidth(100)
        self.KILabel.setMaximumWidth(100)
        self.KIPushButton.setMaximumWidth(150)
        self.KDPushButton.setEnabled(False)
        self.KPPushButton.setEnabled(False)
        self.KIPushButton.setEnabled(True)
        self.KPSlider.setEnabled(False)
        self.KDSlider.setEnabled(False)
        self.KISlider.setEnabled(False)
        PIDLayout.addWidget(QtGui.QLabel("KP:"),0,0)
        PIDLayout.addWidget(self.KPLabel,0,1)
        PIDLayout.addWidget(self.KPSlider,0,2)
        PIDLayout.addWidget(self.KPLineEdit,0,3)
        PIDLayout.addWidget(self.KPPushButton,0,4)
        PIDLayout.addWidget(QtGui.QLabel("KD:"),1,0)
        PIDLayout.addWidget(self.KDLabel, 1,1)
        PIDLayout.addWidget(self.KDSlider,1,2)
        PIDLayout.addWidget(self.KDLineEdit,1,3)
        PIDLayout.addWidget(self.KDPushButton,1,4)
        PIDLayout.addWidget(QtGui.QLabel("KI:"),2,0)
        PIDLayout.addWidget(self.KILabel,2,1)
        PIDLayout.addWidget(self.KISlider,2,2)
        PIDLayout.addWidget(self.KILineEdit,2,3)
        PIDLayout.addWidget(self.KIPushButton,2,4)
        PIDWidgetGroup.setLayout(PIDLayout)
        return PIDWidgetGroup

    def createVisionResetWidget(self):
        visionResetGroup = QtGui.QGroupBox("Vision Reset")
        visionResetLayout = QtGui.QFormLayout()
        self.resetVisionButton.setEnabled(True)
        self.resetVisionButton.clicked.connect(self.resetVision)
        self.resetVisionButton.setText("reset")
        visionResetLayout.addWidget(self.resetVisionButton)
        visionResetGroup.setLayout(visionResetLayout)
        return visionResetGroup

    def createFlagWidget(self):
        flagGroupBox = QtGui.QGroupBox("some flags")
        flagLayout = QtGui.QGridLayout()
        flagLayout.addWidget(QtGui.QLabel("some flag"),0,0)
        flagLayout.addWidget(QtGui.QLabel("some value"),0,1)
        flagGroupBox.setLayout(flagLayout)
        return flagGroupBox

    def createToolBar(self):
        pass

    class CustomStatusBar(QtGui.QStatusBar):
        def __init__(self, label, progressBar):
            super(SelfieApplication.CustomStatusBar,self).__init__()
            self.defaultColor = self.palette().color(QtGui.QPalette.Window)
            self.actualColor = self.defaultColor
            self.connectionLabel = label
            self.connectionProgressBar = progressBar
            self.addWidget(self.connectionLabel)
            self.addWidget(self.connectionProgressBar)
            self.connectionProgressBar.setVisible(False)
        def paintEvent(self, QPaintEvent):
            self.gradient = QtGui.QRadialGradient(self.width()/2, self.height()/2, self.width()*2./3.)
            self.defaultColor = self.palette().color(QtGui.QPalette.Window)
            self.gradient.setColorAt(0.0, self.actualColor)
            self.gradient.setColorAt(1.0, self.defaultColor)
            self.box = QtCore.QRect(0,0,self.width(), self.height())
            self.brush = QtGui.QBrush(self.gradient)
            paint = QtGui.QPainter(self)
            paint.setBrush(self.brush)
            paint.setPen(QtCore.Qt.NoPen)
            paint.drawRect(self.box)
        def setDisconnected(self):
            self.connectionLabel.setText("Disconnected")
            self.actualColor = QtCore.Qt.red
            self.repaint()
        def setConnected(self, name):
            self.connectionLabel.setText("Connected to " + name)
            self.actualColor = QtCore.Qt.green
            self.repaint()
        def setDefault(self):
            self.actualColor = self.defaultColor
            self.repaint()
        def setConnecting(self):
            pass


    def getAddressFromFile(self):
        selfieAddress = ''
        with open("selfieMAC.txt", "r") as file:
            selfieAddress = file.read()
        return selfieAddress

    def setAddressInFile(self, address):
        with open("selfieMAC.txt", "w") as file:
            file.write(address)

    def connectToSelfie(self):
        if not self.connected:
            self.selfieAddress = self.getAddressFromFile()
            try:

                self.socket = bt.BluetoothSocket(bt.RFCOMM)
                self.socket.connect((self.selfieAddress, self.communicationPort))
            except bt.BluetoothError:
                print "couldnt establish a connection"
                errorMessage = QtGui.QMessageBox()
                errorMessage.setIcon(QtGui.QMessageBox.Critical)
                errorMessage.setStandardButtons(QtGui.QMessageBox.Ok)
                errorMessage.setText("Couldn't establish a connection")
                errorMessage.setModal(True)
                errorMessage.exec_()


            except:
                print "some errrorr"
            else:
                self.connected = True
                self.connectSelfieButton.setEnabled(False)
                self.statusBar.setConnected(bt.lookup_name(self.selfieAddress))
                self.enableWidgets()
        else: print 'already connected'
    def disconnectFromSelfie(self):

        if self.connected:
            try:
                self.socket.close()
            except bt.BluetoothError:
                print "unable to close the connection"
            except:
                print "exception"
            else:
                print "disconnected"
                self.statusBar.setDisconnected()
                self.connectSelfieButton.setEnabled(True)
                self.connected = False
                self.disableWidgets()
        else:
            print "already disconnected"
    def resetVision(self):
        try:
            self.socket.send("resetVision")
        except bt.BluetoothError:
            print "cant send"
    class connector(QtCore.QThread):
        def __init__(self, socket, address, port):
            super(SelfieApplication.connector, self).__init__()
            self.socket = socket
            self.address = address
            self.port = port
            self. a = ''
            self.b = ''
            self.finished.connect(self.finishedFun)
            self.started.connect(self.starFun)

        def run(self):
            self.socket.connect((self.address, self.port))
        def finishedFun(self):
            print "finished"
        def starFun(self):
            print "starting"


    def conn(self):
        self.thread = \
            QtCore.QThread()
        self.thread.run = self.connectToSelfie
        def finishedFun():
            print "finished"
        self.thread.finished.connect(finishedFun)
        def startedFun():
            print "started"
        self.thread.started.connect(startedFun)
        self.thread.start()

    def enableWidgets(self):
        for widget in self.widgets:
            widget.setEnabled(True)
    def disableWidgets(self):
        for widget in self.widgets:
            widget.setEnabled(False)


    def changeKP(self):
        value=0.
        try:
            value = float(self.KPLineEdit.text())
            print value
        except:
            return
        self.socket.send('\x01\x01\x01'+str(pack('f',value)))
        a= '\x01\x01\x01'+str(pack('f',value))
        print unpack('f',a[3:])[0]


    def changeKI(self):
        value=0.
        try:
            value = float(self.KILineEdit.text())
        except:
            return
        self.socket.send('\x01\x01\x02'+str(pack('f',value)))
    def changeKD(self):
        value=0.
        try:
            value = float(self.KDLineEdit.text())
        except:
            return
        self.socket.send('\x01\x01\x03'+str(pack('f',value)))












app = QtGui.QApplication([])
#app.setStyleSheet(qdarkstyle.load_stylesheet())
selfieApplication = SelfieApplication()


sys.exit(app.exec_())
