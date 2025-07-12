from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys

from motors import MotorControl
from sensorReading import SensorReading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tensile Test Machine")
        self.setGeometry(100, 100, 1000, 600)

        # GUI Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)

        # Canvas for plotting
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Buttons layout
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Test")
        self.start_button.clicked.connect(self.start_test)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Test")
        self.stop_button.clicked.connect(self.stop_test)
        button_layout.addWidget(self.stop_button)

        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.move_forward)
        button_layout.addWidget(self.forward_button)

        self.backward_button = QPushButton("Backward")
        self.backward_button.clicked.connect(self.move_backward)
        button_layout.addWidget(self.backward_button)

        layout.addLayout(button_layout)

        # Variables for storing data
        self.sigma = []
        self.epsilon = []

        # Motor and Sensor Threads
        self.motor = MotorControl()
        self.sensor = SensorReading()

        # Timer for plotting
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update every second

    def start_test(self):
        """ Starts the test and sensor reading """
        self.sensor.start_reading()
        self.motor.start_motor(1, 84000)

    def stop_test(self):
        """ Stops the motor and sensor """
        self.sensor.stop_reading()
        self.motor.stop_motor()

    def move_forward(self):
        """Forward"""
        self.motor.start_motor(1, 18000)

    def move_backward(self):
        """Backwards"""
        self.motor.start_motor(0, 18000)

    def update_plot(self):
        """ Updates the plot with sensor data """
        try:
            sigma = self.sensor.load
            epsilon = 716.28313 * (35 - (self.sensor.distance - 6.5))

            self.sigma.append(sigma)
            self.epsilon.append(epsilon)

            max_elements = 1440
            self.sigma = self.sigma[-max_elements:]
            self.epsilon = self.epsilon[-max_elements:]

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(self.epsilon, self.sigma, color='blue', linewidth=2)
            ax.set_xlabel("Strain")
            ax.set_ylabel("Stress")
            ax.grid(True)

            self.canvas.draw()

        except Exception as e:
            print(f"Error updating plot: {e}")
