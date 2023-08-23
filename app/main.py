import random
import arcade
import math
from objects_classes import Ship
from objects_classes import Rock
from objects_classes import BulletShip
from objects_classes import Invader
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_INFO = 150
SCREEN_TITLE = "The Attack of the Space Invaders"
SCALING = 0.5
SPEED = 3
BULLET_SPEED = 15

class App(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT + SCREEN_INFO, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)
    self.app_started = False
    self.app_lose = False
    self.app_tutorial = False
    self.difficulty = 0
    self.level_diff = 1
    self.score = 0
    self.pause_game = False
    self.dificultad_original = True
  
  def init_game(self):
    self.restart_game()
    arcade.schedule(self.add_rocks, 1)
    arcade.schedule(self.add_invaders,2.5)
  
  def restart_game(self):
    self.dificultad_original = True
    self.app_started = True
    self.app_lose = False
    self.app_tutorial = False
    self.difficulty = 0
    
    for _ in range(self.level_diff+1):
      arcade.unschedule(self.add_rocks)
      arcade.unschedule(self.add_invaders)
    
    self.level_diff = 1
    
    self.sprites = arcade.SpriteList()
    self.player = Ship("assets/Ship5.png",SCALING, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    self.init_stars()
    self.rocks = arcade.SpriteList()
    self.bullet_ships = arcade.SpriteList()
    self.invaders = arcade.SpriteList()
    self.invaders_bullets = arcade.SpriteList()
    
    self.timer_visible = 0
    self.time_play = 0
    self.player.visible = True
    self.appear = False
    self.shield_on = False
    self.time_shield_on = 0
    self.time_shield_off = 36
    self.time_play_two = 0
    
    self.score = 0
    
    self.destroyed_items = arcade.SpriteList()
  
  def show_controls(self):
    self.app_started = False
    self.app_lose = False
    self.app_tutorial = True
  
  def init_stars(self):
    for _ in range(50):
      star = arcade.SpriteCircle(2,arcade.color.WHITE)
      star.left = random.randint(10, SCREEN_WIDTH - 10)
      star.top = random.randint(10, SCREEN_HEIGHT - 10)
      self.sprites.append(star)
      
  def show_introduction(self):
    self.app_started = False
    self.app_lose = False
    self.app_tutorial = False
      
  def on_key_press(self, symbol: int, modifiers: int):
    if self.app_started:
      if not self.pause_game:
        if symbol == arcade.key.UP:
          self.player.speed_y = SPEED
        if symbol == arcade.key.DOWN:
          self.player.speed_y = -SPEED
        if symbol == arcade.key.LEFT:
          self.player.speed_x = -SPEED
        if symbol == arcade.key.RIGHT:
          self.player.speed_x = SPEED
        
        if symbol == arcade.key.W:
          bullet_ship = BulletShip(
            "assets/shot1_4.png",1,20,
            self.player.center_x,self.player.center_y-4,"normal",0)
          self.bullet_ships.append(bullet_ship)
        if symbol == arcade.key.Q and not self.shield_on:
          bullet_one = BulletShip(
            "assets/shot1_exp2.png",1.2,15,
            self.player.center_x,self.player.center_y-4,"bigger",0)
          bullet_two = BulletShip(
            "assets/shot1_exp2.png",1.2,15,
            self.player.center_x,self.player.center_y-4,"bigger",30)
          bullet_three = BulletShip(
            "assets/shot1_exp2.png",1.2,16,
            self.player.center_x,self.player.center_y-4,"bigger",-30)
          self.bullet_ships.append(bullet_one)
          self.bullet_ships.append(bullet_two)
          self.bullet_ships.append(bullet_three)
          
        if symbol == arcade.key.E  and self.time_shield_off > 35:
          self.shield_on = True
          self.time_shield_off = 0
      
      if symbol == arcade.key.P:
        self.pause_game = not self.pause_game
    
    else:
      if ((symbol==arcade.key.I and not self.app_lose and not self.app_tutorial) or
          (symbol == arcade.key.R and self.app_lose)):
        self.init_game()
        
      if symbol == arcade.key.X and not self.app_tutorial:
        arcade.close_window()
        
      if symbol == arcade.key.H and not self.app_lose:
        self.show_controls()
        
      if symbol == arcade.key.E and self.app_tutorial:
        self.show_introduction()
      
  
  def on_key_release(self, symbol: int, modifiers: int):
    if symbol in (arcade.key.UP, arcade.key.DOWN) and self.app_started:
      self.player.speed_y = 0
    if symbol in (arcade.key.LEFT, arcade.key.RIGHT) and self.app_started:
      self.player.speed_x = 0
  
  def check_collision(self, delta_time: float,sprite):
    sprite.damage_time += delta_time
    if sprite.damage_time <= 0.5:
      sprite.damaged = True
    else:
      sprite.damage_time = 0
      sprite.damaged = False
  
  def upgrade_difficult(self, delta_time: float):
    self.difficulty += delta_time
    if self.difficulty >= 90:
      self.difficulty = 0
      self.level_diff += 1
      arcade.schedule(self.add_invaders,2.5)
  
  def add_rocks(self, delta_time: float):
    y_random = random.randint(10,SCREEN_HEIGHT-10)
    rock = Rock("assets/cave_rock3.png",SCALING,SCREEN_WIDTH-10,y_random,
                random.randint(0,1))
    self.rocks.append(rock)
    
  def add_invaders(self, delta_time: float):
    y_random = random.randint(10,SCREEN_HEIGHT-10)
    invader_type = "normal" if random.randint(1,10)%2 == 0 else "bigger"
    invader_figure = "assets/Ship3.png" if invader_type == "normal" else "assets/Ship6.png"
    invader = Invader(invader_figure,SCREEN_WIDTH-10,y_random,180,invader_type)
    self.invaders.append(invader)
    
  def invader_bullets_updater(self, delta_time: float):
    for bullet in self.invaders_bullets:
      dis_player_bullet = math.sqrt((self.player.center_x - bullet.center_x)**2 + 
                              (self.player.center_y - bullet.center_y)**2)
      cond_1 = bullet.collides_with_sprite(self.player) and not self.appear
      cond_2 = bullet.center_x <= 1 or ((dis_player_bullet <= 50 or (dis_player_bullet <= 60 and bullet.type!="normal"))
                                        and self.shield_on)
      if cond_1 or cond_2:
        self.invaders_bullets.remove(bullet)
        if cond_1:
          self.player_damage(bullet.damage,delta_time)
    self.invaders_bullets.update()
  
  def invader_attack(self, delta_time: float, invader):
    if invader.type == "normal":
      if invader.reload_time < 2.5:
        invader.reload_time += delta_time
      else:
        invader.reload_time = 0
        bullet = BulletShip(
        "assets/shot1_4.png",1,7,
        invader.center_x,invader.center_y-4,invader.type,180)
        bullet.damage = 1
        self.invaders_bullets.append(bullet)
    else:
      if invader.reload_time < 5:
        invader.reload_time += delta_time
      else:
        invader.reload_time = 0
        bullet = BulletShip(
        "assets/shot1_exp2.png",2,3.5,
        invader.center_x,invader.center_y-4,invader.type,180)
        bullet.damage = 5
        self.invaders_bullets.append(bullet)
        
  def invader_updater(self, delta_time: float):
    for invader in self.invaders:
      self.invader_attack(delta_time,invader)
      if invader.center_x <= 1 or invader.life_invader <=0:
        self.destroyed_item_getter(invader)
        if invader.life_invader <=0:
          self.score += 1 if invader.type == "normal" else 3
          self.life_increaser()
      elif invader.collides_with_list(self.bullet_ships):
        for bullet_ship in self.bullet_ships:
          if bullet_ship.collides_with_sprite(invader):
              invader.damaged = True
              invader.life_invader -= bullet_ship.damage
              bullet_ship.remove_from_sprite_lists()
      elif invader.collides_with_sprite(self.player) and not self.appear:
        self.player.damaged = True
        self.player_damage(1,delta_time)
      if invader.damaged:
        self.check_collision(delta_time,invader)
        invader.normal_damage.update()
    self.invaders.update()
    
  def shield_updater(self, delta_time: float):
    if self.shield_on:
      self.time_shield_on += delta_time
      if self.time_shield_on >= 5:
        self.time_shield_on = 0
        self.shield_on = False
        self.time_shield_off = 0
    else:
      if self.time_shield_off <= 35:
        self.time_shield_off += delta_time
    
  def bullets_updater(self, delta_time: float):
    for bullet in self.bullet_ships:
      dis = abs(math.sqrt((bullet.center_x-bullet.original_position[0])**2 +
                          (bullet.center_y-bullet.original_position[1])**2))
      if ((bullet.top > SCREEN_HEIGHT or bullet.bottom < 0 or bullet.left < 0 or bullet.right > SCREEN_WIDTH)
          or (bullet.type!="normal" and dis>=100)):
        self.bullet_ships.remove(bullet)
    self.bullet_ships.update()
  
  def player_damage(self,damage,delta_time: float):
    self.player.life -= damage
    self.appear = True
    self.player.visible = False
    if self.player.life > 0:
      self.check_collision(delta_time,self.player)
  
  def player_damage_updater(self, delta_time: float):
    self.timer_visible += delta_time
    self.time_play += delta_time
    if self.time_play >= 3:
      self.appear = False
      self.player.visible = True
      self.timer_visible = 0
      self.time_play = 0
    elif self.timer_visible >=0.3 and self.timer_visible < 3:
      self.player.visible = not self.player.visible
      self.timer_visible = 0
  
  def rocks_updater(self, delta_time: float):
    for rock in self.rocks:
      dis_rock_player = math.sqrt((rock.center_x - self.player.center_x)**2 +
                                  (rock.center_y - self.player.center_y)**2)
      cond_1 = rock.center_x <= 1
      cond_2 = dis_rock_player <= 30 and not self.appear
      cond_3 = dis_rock_player <=50 and self.shield_on
      rock.angle += rock.speed_rotation * delta_time
      rock.angle %= 360
      if cond_1 or cond_2 or cond_3:
        self.destroyed_item_getter(rock)
        if cond_2:
          self.player.damaged = True
          self.player_damage(1,delta_time)
      elif rock.collides_with_list(self.bullet_ships):
        for bullet in self.bullet_ships:
          if bullet.collides_with_sprite(rock) and bullet.type=="normal":
            bullet.remove_from_sprite_lists()
            rock.damaged = True
          elif bullet.collides_with_sprite(rock) and bullet.type!="normal":
            self.destroyed_item_getter(rock)
            bullet.remove_from_sprite_lists()
            break
      elif rock.collides_with_list(self.invaders_bullets):
        for bullet in self.invaders_bullets:
          if bullet.collides_with_sprite(rock) and bullet.type=="normal":
            bullet.remove_from_sprite_lists()
            rock.damaged = True
          elif bullet.collides_with_sprite(rock) and bullet.type!="normal":
            self.destroyed_item_getter(rock)
            break
      elif rock.collides_with_list(self.invaders):
        for invader in self.invaders:
          if invader.collides_with_sprite(rock):
            self.destroyed_item_getter(rock)
            break
      if rock.damaged:
        self.check_collision(delta_time,rock)
        rock.normal_damage.update()
    self.rocks.update()
    
  def life_increaser(self):
    life_incrementer = 0
    if self.score % 200 == 0 and self.score != 0:
      life_incrementer = 10
    elif self.score % 100 == 0 and self.score != 0:
      if self.player.life + 5 <= 10:
        life_incrementer = 5
      else:
        life_incrementer = 10 - self.player.life
    elif self.score % 50 == 0 and self.score != 0:
      if self.player.life + 3 <= 10:
        life_incrementer = 2
      else:
        life_incrementer = 10 - self.player.life
    
    if life_incrementer != 10:
      self.player.life += life_incrementer
    else:
      self.player.life = 10

  def player_updater(self, delta_time: float):
    # Limit Height
    cond_top = self.player.center_y < SCREEN_HEIGHT - 10
    cond_bottom = self.player.center_y > 10
    if cond_top and cond_bottom:
      self.player.original_y = self.player.center_y
    else:
      self.player.center_y = self.player.original_y
    # Limit Width
    cond_left = self.player.center_x > 20
    cond_right = self.player.center_x < SCREEN_WIDTH - 20
    if cond_left and cond_right:
      self.player.original_x = self.player.center_x
    else:
      self.player.center_x = self.player.original_x
    if self.player.damaged:
      self.check_collision(delta_time,self.player)
      self.player.normal_damage.update()
    already_exist = -1
    posible_index = None
    try:
      already_exist = self.destroyed_items.index(self.player)
      posible_index = self.destroyed_items.__getitem__(already_exist)
    except ValueError:
      already_exist = -1
    if self.player.life <= 0 and already_exist==-1 and posible_index == None:
      self.destroyed_item_getter(self.player)
    self.player.update()
  
  def on_update(self, delta_time: float):
    if self.app_started:
      if not self.pause_game:
        self.upgrade_difficult(delta_time)
        self.sprites.update()
        self.rocks_updater(delta_time)
        self.bullets_updater(delta_time)
        self.invader_updater(delta_time)
        self.invader_bullets_updater(delta_time)
        if self.appear:
          self.player_damage_updater(delta_time)
        self.destroyed_items.update()
        self.shield_updater(delta_time)
        self.player_updater(delta_time)
        
        if not self.dificultad_original:
          for _ in range(0,self.level_diff):
            arcade.schedule(self.add_invaders,2.5)
          arcade.schedule(self.add_rocks,1)
          self.dificultad_original = True
      else:
        for _ in range(0,self.level_diff):
          arcade.unschedule(self.add_invaders)
        arcade.unschedule(self.add_rocks)
        self.dificultad_original = False
  
  def damage_drawer(self,sprite_list):
    for sprite in sprite_list:
      sprite.draw()
      if sprite.damaged == True:
        sprite.normal_damage.draw()
    
  def destroyed_item_getter(self,sprite):
    sprite.destroyed = True
    self.destroyed_items.append(sprite.destroyed_item)
    sprite.remove_from_sprite_lists()
    
  def destroyed_items_drawer(self):
    if len(self.destroyed_items) != 0:
      self.destroyed_items.draw()
  
  def navbar_drawer(self):
    top = SCREEN_HEIGHT + SCREEN_INFO - 35
    arcade.draw_text("YOU:",25,top-10,arcade.color.WHITE,12,bold=True)
    space = 50
    for i in range(0,self.player.life,1):
      space += 40 if i != 0 else space
      # space += 30 if i!=0 else 0
      arcade.draw_rectangle_filled(space,top,
                                    35,35,arcade.color.GREEN)
    
    state_game = "continue" if self.pause_game else "pause"
    text_game_message = "Press 'p' to "+state_game
    arcade.draw_text(text_game_message,SCREEN_WIDTH//2 - 75,top-60,arcade.color.WHITE,12,bold=True)
    
    space = 120
    arcade.draw_text("SHIELD:",20,top-60,arcade.color.WHITE,12,bold=True)
    arcade.draw_text((self.time_shield_off//1 if self.time_shield_off <= 35 and not self.shield_on else (
      "READY" if self.time_shield_off > 35 and not self.shield_on else (6-self.time_shield_on)//1
    )),space,top-60,arcade.color.BLUE_VIOLET,12,bold=True)
  
    arcade.draw_text(f"SCORE: {self.score}",SCREEN_WIDTH - space*1.5, top, arcade.color.WHITE,12,bold=True)
    arcade.draw_text(f"LEVEL: {self.level_diff}",SCREEN_WIDTH - space*1.48, top-50, arcade.color.WHITE,12,bold=True)
  
  def draw_introduction(self):
    arcade.draw_text("THE ATTACK OF THE SPACE INVADERS",
                      start_x=110, start_y=SCREEN_HEIGHT//2+150,
                      font_size=20,color=arcade.color.RED_DEVIL,
                      bold=True)
    arcade.draw_text("Press 'i' to start",
                    start_x=SCREEN_WIDTH//2 - 80,start_y=SCREEN_HEIGHT//2 + 100
                    ,font_size=16)
    arcade.draw_text("Press 'x' to quit",
                    start_x=SCREEN_WIDTH//2 - 80,start_y=SCREEN_HEIGHT//2 + 50
                    ,font_size=16)
    arcade.draw_text("Press 'h' to see controls",
                    start_x=SCREEN_WIDTH//2 - 120,start_y=SCREEN_HEIGHT//2
                    ,font_size=16)
  
  def draw_game(self):
    self.sprites.draw()
    arcade.draw_rectangle_outline(
      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
      SCREEN_WIDTH, SCREEN_HEIGHT,
      arcade.color.RED_DEVIL, 10)
    self.damage_drawer(self.rocks)
    self.bullet_ships.draw()
    self.destroyed_items_drawer()
    self.damage_drawer(self.invaders)
    self.destroyed_items.clear()
    self.invaders_bullets.draw()
    if self.shield_on:
      arcade.draw_circle_outline(
        self.player.center_x,self.player.center_y,50,arcade.color.BLUE_SAPPHIRE,5)
    
    if self.player.life > 0:
      self.player.draw()
    else:
      self.app_lose = True
      self.app_started = False
    
    if self.player.damaged:
      self.player.normal_damage.draw()
    self.navbar_drawer()
  
  def draw_instructions(self):
    arcade.draw_text("INSTRUCTIONS",
                      start_x=110, start_y=SCREEN_HEIGHT//2+350,
                      font_size=28,color=arcade.color.RED_DEVIL,
                      bold=True)
    left_distance = 50
    arcade.draw_text("* Use 'LEFT', 'UP', 'DOWN' and 'RIGHT' to move yourself",
                    start_x=left_distance,start_y=SCREEN_HEIGHT//2 + 300
                    ,font_size=16)
    arcade.draw_text("* Use 'w' to shoot normal bullets",
                    start_x=left_distance,start_y=SCREEN_HEIGHT//2 + 250
                    ,font_size=16)
    arcade.draw_text("* Use 'q' to shoot big bullets",
                    start_x=left_distance,start_y=SCREEN_HEIGHT//2 + 200
                    ,font_size=16)
    arcade.draw_text("* Use 'e' to activate your shield for 5 sec",
                    start_x=left_distance,start_y=SCREEN_HEIGHT//2 + 150
                    ,font_size=16)
    arcade.draw_text("Warning: You'll have to wait 35 sec to use it again",
                    start_x=left_distance,start_y=SCREEN_HEIGHT//2 + 100
                    ,font_size=16)
    arcade.draw_text("and you won't be able to shoot big bullets",
                    start_x=left_distance,start_y=SCREEN_HEIGHT//2 + 50
                    ,font_size=16)
    arcade.draw_text("* Difficulty will increase every 90 sec",
                    start_x=left_distance,start_y=SCREEN_HEIGHT//2
                    ,font_size=16)
    arcade.draw_text("Press 'e' to get back",
                    start_x=left_distance,start_y=SCREEN_HEIGHT//2 - 100
                    ,font_size=16)
  
  def draw_game_over(self):
    arcade.draw_text("GAME OVER",
                      start_x=280, start_y=SCREEN_HEIGHT//2+250,
                      font_size=28,color=arcade.color.RED_DEVIL,
                      bold=True)
    arcade.draw_text(f"SCORE: {self.score}",
                      start_x=280, start_y=SCREEN_HEIGHT//2+200,
                      font_size=20,color=arcade.color.RED_DEVIL,
                      bold=True)
    arcade.draw_text(f"LEVEL: {self.level_diff}",
                      start_x=280, start_y=SCREEN_HEIGHT//2+150,
                      font_size=20,color=arcade.color.RED_DEVIL,
                      bold=True)
    arcade.draw_text("Press 'r' to restart",
                      start_x=260, start_y=SCREEN_HEIGHT//2+100,
                      font_size=20,color=arcade.color.RED_DEVIL,
                      bold=True)
    arcade.draw_text("Press 'x' to quit",
                      start_x=280, start_y=SCREEN_HEIGHT//2+50,
                      font_size=20,color=arcade.color.RED_DEVIL,
                      bold=True)
  
  def on_draw(self):
    arcade.start_render()
    if self.app_started:
      self.draw_game()
    elif self.app_lose:
      time.sleep(0.2)
      self.draw_game_over()
    elif self.app_tutorial:
      self.draw_instructions()
    else:
      self.draw_introduction()

if __name__ == "__main__":
  app = App()
  arcade.run()