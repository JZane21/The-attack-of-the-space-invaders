import arcade
import random
import math


class Rock(arcade.Sprite):
  def __init__(self,image,scale, x, y, speed_rotation):
    super().__init__(image,scale,center_x=x,center_y=y)
    self.speed_rotation = 30 if speed_rotation==1 else -30
    self.speed = 1.5
    self.angle = 0
    self.damage_time = 0
    self.damaged = False
    self.destroyed = False
    self.normal_damage = arcade.Sprite(filename="assets/Explosion1_1.png",
                                      scale=1,center_x=x,center_y=y)
    self.destroyed_item = arcade.Sprite(filename="assets/Explosion1_10.png",
                                      scale=2,center_x=x,center_y=y)
  def update(self):
    self.center_x += -self.speed
    self.normal_damage.center_x += -self.speed
    self.destroyed_item.center_x += -self.speed