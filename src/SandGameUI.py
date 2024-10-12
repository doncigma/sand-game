from PyQt6.QtWidgets import QMainWindow, QWidget, QGraphicsView, QGraphicsItem, QGraphicsScene, QVBoxLayout, QHBoxLayout, QGraphicsRectItem, QGraphicsEllipseItem, QRadioButton, QCheckBox, QDateTimeEdit
from PyQt6.QtCore import QTimer, QRectF, QPointF, QPoint
from PyQt6.QtGui import QColor, QMouseEvent
from typing import Tuple

import time

from SandGame import SandGame
from Slider import Slider

class SandGameUI(QMainWindow):
    def __init__(self, gameSize: Tuple[int, int] = (50, 50), brownian = 20):
        super().__init__()
        self.setWindowTitle("I Hate Sand")
        
        self.SandGame = SandGame(gameSize, brownian)
        self.blockList = SandGame.blockList
        self.effectList = "ERASE,FAT_ERASE"
        self.allElements = self.blockList + ",ERASE,FAT_ERASE"

        self.cellSide = 14
        self.gameWidth = gameSize[0] * self.cellSide
        self.gameHeight = gameSize[1] * self.cellSide

        # Mouse Modes
        self.mouseDown = False
        self.mouseMode = ""
        self.lastPos = None
        self.sandBox = QRadioButton("Sand")
        self.sandBox.toggled.connect(lambda: self.set_mouse_mode("S"))

        self.rockBox = QRadioButton("Rock")
        self.rockBox.toggled.connect(lambda: self.set_mouse_mode("R"))

        self.vineBox = QRadioButton("Vine")
        self.vineBox.toggled.connect(lambda: self.set_mouse_mode("V"))

        self.fertBox = QRadioButton("Fertilizer")
        self.fertBox.toggled.connect(lambda: self.set_mouse_mode("F"))

        self.eraseBox = QRadioButton("Erase")
        self.eraseBox.toggled.connect(lambda: self.set_mouse_mode("ERASE"))

        self.fatEraseBox = QRadioButton("Fat Erase")
        self.fatEraseBox.toggled.connect(lambda: self.set_mouse_mode("FAT_ERASE"))

        # Physics UI
        self.gravityBox = QCheckBox("Gravity")
        self.gravityBox.setChecked(True)
        self.gravityBox.stateChanged.connect(self.gravity_checkbox_toggle)

        self.brownianSlider = Slider("Brownian: " + str(brownian))
        self.brownianSlider.slider.valueChanged.connect(self.brownian_slider_change)
        
        # Setup Scene (interactable game world) and View (renderer of scene)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(QRectF(0, 0, self.gameWidth, self.gameHeight))
        self.view = QGraphicsView(self.scene, self)

        # Function override
        self.view.mousePressEvent = self.scenePressEvent
        self.view.mouseMoveEvent = self.sceneMoveEvent
        self.view.mouseReleaseEvent = self.sceneReleaseEvent

        # Layout Widgets
        toolbarWidget = QWidget()
        toolbar = QHBoxLayout(toolbarWidget)
        toolbar.addWidget(self.brownianSlider)
        toolbar.addWidget(self.gravityBox)
        toolbar.addWidget(self.sandBox)
        toolbar.addWidget(self.rockBox)
        toolbar.addWidget(self.vineBox)
        toolbar.addWidget(self.fertBox)
        toolbar.addWidget(self.eraseBox)
        toolbar.addWidget(self.fatEraseBox)
        
        layout = QVBoxLayout()
        layout.addWidget(toolbarWidget)
        layout.addWidget(self.view)
        
        # Set layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(layout)
    
    # Input Event Handlers
    def gravity_checkbox_toggle(self):
        self.SandGame.toggle_gravity()

    def brownian_slider_change(self, val):
        self.brownianSlider.label.setText("Brownian: " + str(val))
        self.SandGame.set_brownian(val)

    def set_mouse_mode(self, mode: str):
        if mode in self.allElements:
            self.mouseMode = mode
    
    def scenePressEvent(self, event: QMouseEvent):
        self.mouseDown = True
        self.process_mouse_event(self.view.mapToScene(event.pos()))

    def sceneMoveEvent(self, event: QMouseEvent):
        if self.mouseDown:
            self.process_mouse_event(self.view.mapToScene(event.pos()))

    def sceneReleaseEvent(self, event: QMouseEvent):
        self.mouseDown = False

    def process_mouse_event(self, scenePos: QPoint):
        self.lastPos = scenePos
        # save data not object
        x = int(scenePos.x() // self.cellSide)
        y = int(scenePos.y() // self.cellSide)
        
        if self.mouseMode in self.blockList:
            self.SandGame.place_block(self.mouseMode, x, y)
        elif self.mouseMode == "ERASE":
            self.erase(x, y)
        elif self.mouseMode == "FAT_ERASE":
            self.fat_erase(x, y)

    def erase(self, x: int, y: int):
        self.SandGame.remove_block(x, y)

    def fat_erase(self, x: int, y: int):
        self.SandGame.remove_block(x, y)
        self.SandGame.remove_block(x+1, y)
        self.SandGame.remove_block(x-1, y)
        self.SandGame.remove_block(x, y+1)
        self.SandGame.remove_block(x, y-1)
        self.SandGame.remove_block(x+1, y+1)
        self.SandGame.remove_block(x-1, y-1)
    
    # UI Drawing
    def draw_block(self, drawType: str, x: int, y: int):
        # Set color
        if drawType == "S":
            color = QColor(194, 178, 128)
        elif drawType == "R":
            color = QColor(150, 75, 0)
        elif drawType == "V":
            color = QColor(1, 50, 32)
        elif drawType == "F":
            color = QColor(39, 34, 28)
        
        block = QGraphicsRectItem(x*self.cellSide, y*self.cellSide, self.cellSide, self.cellSide)
        block.setBrush(color)
        # block.setPen(Qt.NoPen)
        self.scene.addItem(block)
    
    def redraw_scene(self):
        """Iterates over game world and draws blocks based on type and cell-pixel math
        """        
        gameWorld = self.SandGame.get_game_world()
        self.scene.clear()
        
        for x, col in enumerate(gameWorld):
            for y, cell in enumerate(col):
                if cell in self.blockList:
                    self.draw_block(cell, x, y)

        # Draw erase circles
        if self.mouseMode == "ERASE" and self.mouseDown:
            erase = QGraphicsRectItem(self.lastPos.x()-4, self.lastPos.y()-4, self.cellSide, self.cellSide)
            erase.setBrush(QColor(255, 0, 0))
            self.scene.addItem(erase)
        elif self.mouseMode == "FAT_ERASE" and self.mouseDown:
            self.scene.addEllipse(self.lastPos.x()-self.cellSide*1.75, self.lastPos.y()-self.cellSide*1.75, self.cellSide*4, self.cellSide*4, QColor(255, 0, 0), QColor(255, 0, 0))
    
    # Game Loop
    def tick(self):
        if self.mouseDown:
            self.process_mouse_event(self.lastPos)
        self.SandGame.tick_game_world()
        self.redraw_scene()
    
    def start_game(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000//60) # 30hz conversion to msec
