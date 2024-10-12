from PyQt6.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class Slider(QWidget):
    def __init__(self, customLabel):
        super().__init__()
        
        # Create slider
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(20)

        # Label
        self.label = QLabel(customLabel, self.slider)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        self.setLayout(layout)
    
    @property
    def sliderWidget(self):
        return self.slider
