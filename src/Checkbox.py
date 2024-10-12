from PyQt6.QtWidgets import QWidget, QCheckBox, QHBoxLayout

class Checkbox(QWidget):
    def __init__(self, label: str):
        super().__init__()
        
        # Setup box
        self.checkbox = QCheckBox(label, self)

        # Set layout
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        self.setLayout(layout)

    @property
    def checkboxWidget(self):
        return self.checkbox
