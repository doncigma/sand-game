import numpy as np
from typing import Tuple
import random
from dataclasses import dataclass
import time

class SandGame:
    elementList = "A,S,R,V,F,W,"
    blockList = "S,R,V,F,W,"

    @dataclass
    class Vine:
        vineMove = "A,R,F"
        chance = 15
    
    def __init__(self, gameSize: Tuple[int, int] = (50, 50), brownian: int = 20) -> None:
        self.gameWidth = gameSize[0]
        self.gameHeight = gameSize[1]
        self.__gameMatrix__ = np.full(gameSize, "A")
        self.__brownian__ = brownian
        self.__gravityOn__ = True
        self.vine = self.Vine()
        self.vineTime = time.time()
        self.lastWaterPos = "L"
    
    # Getters and Setters
    def get_brownian(self) -> int:
        return self.__brownian__
    
    def set_brownian(self, newVal: int):
        if 0 <= newVal <= 100:
            self.__brownian__ = newVal
    
    def toggle_gravity(self) -> bool:
        """Toggles gravity on and off

        Returns:
            bool: True = on, False = off
        """        
        self.__gravityOn__ = not self.__gravityOn__
        return self.__gravityOn__
    
    def get_block(self, x: int, y: int) -> str:
        """Gets block at desired location.

        Args:
            cords[0] (int): x position to get from
            cords[1] (int): y position to get from

        Returns:
            str: char of the block
        """        
        if 0 <= x < self.gameWidth and 0 <= y < self.gameHeight:
            return self.__gameMatrix__[x][y]
        else:
            return ""
    
    def place_block(self, block: str, x: int, y: int):
        """Places block at desired location and performs proper checks for placeability.

        Args:
            block (str): char that represents block type
            cords[0] (int): x position to place at
            cords[1] (int): y position to place at
        """        
        if 0 <= x < self.gameWidth and 0 <= y < self.gameHeight and block in self.blockList:           
            if block == "S" and self.can_move("S", x, y):
                self.__gameMatrix__[x][y] = block
            elif block == "R":
                self.__gameMatrix__[x][y] = block
            elif block == "V" and self.can_move("V", x, y):
                self.__gameMatrix__[x][y] = block
            elif block == "F":
                self.__gameMatrix__[x][y] = block
            elif block == "W" and self.can_move("W", x, y):
                self.__gameMatrix__[x][y] = block
    
    def can_move(self, blockToMove: str, x: int, y: int):
        result = False
        
        if 0 <= x < self.gameWidth and 0 <= y < self.gameHeight:
            spot = self.get_block(x, y)
            if blockToMove == "S" and spot == "A":
                result = True
            elif blockToMove == "V" and spot in self.vine.vineMove:
                if spot == "F":
                    pass
                result = True
            elif blockToMove == "W" and spot == "A":
                result = True
                 
        return result
        
    def remove_block(self, x: int, y: int, blockToReplace: str = "A"):
        if 0 <= x < self.gameWidth and 0 <= y < self.gameHeight:
            self.__gameMatrix__[x][y] = blockToReplace
    
    def get_game_world(self):
        return self.__gameMatrix__
    
    # Physics Processes
    def __apply_gravity_on_block__(self, x: int, y: int, blockToApply: str):
        if self.__gravityOn__ and self.can_move(blockToApply, x, y+1):
            self.remove_block(x, y)
            self.place_block(blockToApply, x, y+1)

    def __apply_brownian_on_block__(self, x: int, y: int, blockToApply: str):
        if self.get_block(x, y) == blockToApply:
            if random.randint(0, 99) < self.__brownian__ :
                coin = random.randint(0, 1)
                if coin == 0 and self.can_move(blockToApply, x-1, y):
                    self.place_block(blockToApply, x-1, y)
                    self.remove_block(x, y)
                elif coin == 1 and self.can_move(blockToApply, x+1, y):
                    self.place_block(blockToApply, x+1, y)
                    self.remove_block(x, y)
        
    def __apply_flow_on_block__(self, x: int, y: int, blockToApply: str):
        if self.get_block(x, y) == blockToApply:
            if self.lastWaterPos == "L":
                # coin = random.randint(0, 1)
                if self.can_move(blockToApply, x-1, y):
                    self.place_block(blockToApply, x-1, y)
                    self.remove_block(x, y)
                    self.lastWaterPos = "L"
                elif self.can_move(blockToApply, x+1, y):
                    self.place_block(blockToApply, x+1, y)
                    self.remove_block(x, y)
                    self.lastWaterPos = "R"
            elif self.lastWaterPos == "R":
                # coin = random.randint(0, 1)
                if self.can_move(blockToApply, x+1, y):
                    self.place_block(blockToApply, x+1, y)
                    self.remove_block(x, y)
                    self.lastWaterPos = "R"
                elif self.can_move(blockToApply, x-1, y):
                    self.place_block(blockToApply, x-1, y)
                    self.remove_block(x, y)
                    self.lastWaterPos = "L"
                    
    def __vine_grow_on_block__(self, x: int, y: int):
        if random.randint(0, 99) < self.vine.chance:
            if random.randint(0, 99) < 15 and self.get_block(x+1, y-1) in self.vine.vineMove and self.get_block(x+1, y+1) in self.vine.vineMove:# and self.get_block(x, y+1) in self.vine.vineMove:
                self.place_block("V", x+1, y)   # right
            elif random.randint(0, 99) < 15 and self.get_block(x-1, y-1) in self.vine.vineMove and self.get_block(x-1, y+1) in self.vine.vineMove:# and self.get_block(x, y+1) in self.vine.vineMove:
                self.place_block("V", x-1, y)   # left
            elif random.randint(0, 99) < 25 and self.get_block(x-1, y-1) in self.vine.vineMove and self.get_block(x+1, y-1) in self.vine.vineMove:
                self.place_block("V", x, y-1)   # up

    def tick_game_world(self):
        """Ticks game world forward by applying gravity and brownian.
        """  
        delta = time.time() - self.vineTime
        
        for y in reversed(range(self.gameHeight)):
            for x in reversed(range(self.gameWidth)):
                cell = self.get_block(x, y)
                if cell == "S":
                    self.__apply_gravity_on_block__(x, y, "S")     
                    self.__apply_brownian_on_block__(x, y, "S")
                elif cell == "V" and delta >= 0.18:
                    self.__vine_grow_on_block__(x, y)
                    self.vineTime = time.time()
                elif cell == "W":
                    self.__apply_gravity_on_block__(x, y, "W")     
                    # self.__apply_brownian_on_block__(x, y, "W")
                    self.__apply_flow_on_block__(x, y, "W")
    
    def reset_game_world(self, newSize: Tuple[int, int] | None = None):
        """Resets the game world with an option to designate new size.
        """        
        if newSize:
            self.gameWidth = newSize[0]
            self.gameHeight = newSize[1]
            
        self.__gameMatrix__ = np.full((self.gameWidth, self.gameHeight), "A")
