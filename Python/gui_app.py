import sys
import serial
import serial.tools.list_ports
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import tools
from colors import *

DEBUG = True

def serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

class MyApp(QWidget):
    CONFIG_FILE_NAME = "config.json"
    SUPPORTED_BAUDRATES = [9600, 19200, 38400, 57600, 115200]
    baudrate = 115200

    com_port_text = "Sériový COM port: "

    def supported_baudrates(self, baudrate):
        return baudrate in self.SUPPORTED_BAUDRATES

    def __init__(self):
        super().__init__()
        self.initUI()

        data = tools.load_dic_from_file(self.CONFIG_FILE_NAME)

        if data:
            print(f"Loaded port: {Blue + data['port'] + NC}")
            self.comLabel.setText(self.com_port_text + data["port"])

            if self.supported_baudrates(data["baudrate"]):
                print(f"Loaded baudrate: {Blue}{data['baudrate']}{NC}")
                self.baudrate = int(data["baudrate"])
        else:
            print(f"Config file: {Blue + self.CONFIG_FILE_NAME + NC} not found!")


    def initUI(self):
        # Hlavní layout
        mainLayout = QHBoxLayout()

        # Levý sloupec s tlačítky a volbami
        leftLayout = QVBoxLayout()

        # Sériový port
        self.comLabel = QLabel('Sériový COM port:')
        self.comComboBox = QComboBox()
        self.comComboBox.addItems(serial_ports())
        self.comComboBox.currentIndexChanged.connect(self.update_comLabel)
        self.saveButton = QPushButton('Save COM')
        self.saveButton.clicked.connect(self.save_config)
        self.connectButton = QPushButton('Připojit')

        # Audio loop a další volby
        self.audioLoopButton = QPushButton('Audio LOOP')
        self.aliveButton = QPushButton('ALive')
        self.signalButton = QPushButton('Signál z STM')
        self.aprLoopButton = QPushButton('APR Loop')

        # FIR volby
        self.leftChannelCheck = QCheckBox('Left channel')
        self.rightChannelCheck = QCheckBox('Right channel')
        self.firSelectComboBox = QComboBox()
        self.firSelectComboBox.addItems(['0.2 0.2 0.2', 'FIR_34.mat', 'FIR_46.mat', 'DP 2. fádu'])

        # FFT tlačítka
        self.fftTest1024 = QPushButton('FFT test 1024')
        self.fftTest2048 = QPushButton('FFT test 2048')

        # Přidání prvků do levého layoutu
        leftLayout.addWidget(self.comLabel)
        leftLayout.addWidget(self.comComboBox)
        leftLayout.addWidget(self.saveButton)
        leftLayout.addWidget(self.connectButton)
        leftLayout.addWidget(self.audioLoopButton)
        leftLayout.addWidget(self.aliveButton)
        leftLayout.addWidget(self.signalButton)
        leftLayout.addWidget(self.aprLoopButton)
        leftLayout.addWidget(self.leftChannelCheck)
        leftLayout.addWidget(self.rightChannelCheck)
        leftLayout.addWidget(self.firSelectComboBox)
        leftLayout.addWidget(self.fftTest1024)
        leftLayout.addWidget(self.fftTest2048)
        # add spacer
        
        

        # Pravý sloupec s grafem
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Přidání layoutů do hlavního rozvržení
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(self.canvas)

        # Nastavení hlavního okna
        self.setLayout(mainLayout)
        self.setWindowTitle('PyQt5 App Example')
        self.setGeometry(300, 300, 800, 600)

    def plot_data(self, data):
        self.ax.clear()
        self.ax.plot(data)
        self.canvas.draw()

    def update_comLabel(self, index):
        # Aktualizace textu v QLabel na základě vybrané položky v QComboBox
        selected_text = self.comComboBox.currentText()
        self.comLabel.setText(self.com_port_text + selected_text)

    def connect_to_serial(self):
        port = self.comComboBox.currentText()

        ser = serial.Serial(port, self.baudrate)
        ser.flushInput()

        """
        while True:
            try:
                line = ser.readline().decode("utf-8")
                data = np.array([int(x) for x in line.split(",")])
                self.plot_data(data)
            except KeyboardInterrupt:
                ser.close()
                break
        """

    def save_config(self):
        data = {
            "port": self.comComboBox.currentText(),
            "baudrate": int(self.baudrate)
        }

        tools.save_to_json(self.CONFIG_FILE_NAME, data)

        print(f"Configuration saved to {Blue + self.CONFIG_FILE_NAME + NC}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
