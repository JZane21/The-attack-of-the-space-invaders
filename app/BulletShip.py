import arcade
import math

class BulletShip(arcade.Sprite):
  def __init__(self, image, scale, speed, x, y, type, angle):
    super().__init__(image, scale,angle=angle,center_x=x,center_y=y)
    self.type = type
    self.original_position = (x,y)
    self.damage = 2 if self.type == "normal" else 8
    self.velocity = (
      speed * math.cos(math.radians(angle)),
      speed * math.sin(math.radians(angle))
    )