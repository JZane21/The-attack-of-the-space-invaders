import arcade
import math

class Ship(arcade.Sprite):
  def __init__(self,image,scale, x, y):
    super().__init__(image,scale,center_x=x,center_y=y)
    self.speed_x = 0
    self.speed_y = 0
    self.life = 10
    self.original_y = y
    self.original_x = x
    self.bullets = []
    self.damage_time = 0
    self.damaged = False
    self.destroyed = False
    self.normal_damage = arcade.Sprite(filename="assets/Explosion1_1.png",
                                      scale=1,center_x=x,center_y=y)
    self.destroyed_item = arcade.Sprite(filename="assets/Explosion1_7.png",
                                      scale=1,center_x=x,center_y=y)
  def update(self):
    self.center_x += self.speed_x
    self.center_y += self.speed_y
    self.normal_damage.center_x += self.speed_x
    self.normal_damage.center_y += self.speed_y
    self.destroyed_item.center_x += self.speed_x
    self.destroyed_item.center_y += self.speed_y
  