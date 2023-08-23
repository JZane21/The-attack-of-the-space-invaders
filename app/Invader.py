import arcade


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
