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

class Invader(arcade.Sprite):
  def __init__(self,image, x, y, angle, type):
    scale = 0.5 if type == "normal" else 1
    super().__init__(image,scale,center_x=x,center_y=y, angle=angle)
    self.type = type
    self.speed = 2 if self.type == "normal" else 1
    self.life_invader = 10 if self.type == "normal" else 50
    self.reload_time = 0
    self.damage_time = 0
    self.damaged = False
    self.destroyed = False
    scale_damage = 1 if self.type == "normal" else 2
    self.normal_damage = arcade.Sprite(filename="assets/Explosion1_1.png",
                                      scale=scale_damage,center_x=x,center_y=y)
    image_src = "assets/Explosion1_9.png" if self.type == "normal" else "assets/Explosion1_8.png"
    self.destroyed_item = arcade.Sprite(filename=image_src,
                                      scale=2,center_x=x,center_y=y)
  def update(self):
    self.center_x += -self.speed
    self.normal_damage.center_x += -self.speed
    self.destroyed_item.center_x += -self.speed

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