from PyQt6.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from typing import Tuple

class Slider(QWidget):
    def __init__(self, customLabel: str, min: int, max: int, val: int):
        super().__init__()
        
        # Create slider
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(val)

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
