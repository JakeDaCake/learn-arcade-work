import arcade
import random
import math
import os
import time

SPRITE_SCALING = 0.5
TILE_SCALING = 0.5
GRID_PIXEL_SIZE = 128
GRAVITY = 0.25

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Goblins With Guns"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 220

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 2
JUMP_SPEED = 4.5

# How fast the projectiles move
PROJECTILE_SPEED = 5

# How fast the goblins move
GOBLIN_MOVEMENT_SPEED = 2

EXPLOSION_TEXTURE_COUNT = 25
COIN_TEXTURE_COUNT = 12


class Mana_Bar(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

        self.last_first_frame = 0

    def update(self, frame):
        self.set_texture(frame)


class Goblin(arcade.Sprite):
    def __init__(self, texture_list, wall_list, box_list, coinbox_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

        self.last_first_frame = 0

        self.physics_engine = None
        self.box_physics_engine = None
        self.coinbox_physics_engine = None

        self.walls = wall_list
        self.boxes = box_list
        self.coinboxes = coinbox_list

    def setup(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self,
            self.walls,
            gravity_constant=GRAVITY
        )
        self.box_physics_engine = arcade.PhysicsEnginePlatformer(
            self,
            self.boxes,
            gravity_constant=0
        )
        self.coinbox_physics_engine = arcade.PhysicsEnginePlatformer(
            self,
            self.coinboxes,
            gravity_constant=0
        )

    def update(self):
        self.setup()
        self.set_texture(0)
        self.physics_engine.update()
        self.box_physics_engine.update()
        self.coinbox_physics_engine.update()


class Tree_Goblin(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

        self.last_first_frame = 0

        self.count = 0

        self.lives = 2

    def update(self, first_frame, last_frame):
        if self.last_first_frame != first_frame:
            # If the frame range has changed, reset to the beginning of the new animation
            self.current_texture = first_frame
            self.count = 999  # must be >=

        # Delay the next sprite frame change. to slow down the animation
        if self.count < 4:
            self.set_texture(self.current_texture)
            self.count += 1
            return
        self.count = 0

        # Move the animation forward one frame.
        self.last_first_frame = first_frame
        self.current_texture += 1
        if self.current_texture < last_frame:
            self.set_texture(self.current_texture)
        else:
            self.current_texture = first_frame

class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """
    def __init__(self, texture_list):
        super().__init__()
        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):
        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class Coin(arcade.Sprite):
    """ This class creates an explosion animation """
    def __init__(self, texture_list):
        super().__init__()
        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

        self.count = 0

    def update(self):
        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        if self.count < 4:
            self.set_texture(self.current_texture)
            self.count += 1
            return
        self.current_texture += 1
        self.count = 0
        if self.current_texture >= len(self.textures):
            self.current_texture = 0


class Player(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

        self.last_first_frame = 0

        self.count = 0

    def update(self, first_frame, last_frame):
        if self.last_first_frame != first_frame:
            # If the frame range has changed, reset to the beginning of the new animation
            self.current_texture = first_frame
            self.count = 999  # must me >=

        # Delay the next sprite frame change. to slow down the animation
        if self.count < 4:
            self.set_texture(self.current_texture)
            self.count += 1
            return
        self.count = 0

        # Move the animation forward one frame.
        self.last_first_frame = first_frame
        self.current_texture += 1
        if self.current_texture < last_frame:
            self.set_texture(self.current_texture)
        else:
            self.current_texture = first_frame


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Initializer """
        super().__init__(width, height, title, resizable=True)

        # How many lives and mana the player has left
        self.LIVES = 3
        self.MANA = 6

        self.frame_count = 0

        self.last_move = 'right'

        # Sprite lists
        self.player_list = None
        # self.mana_bar_list = None
        self.goblin_list = None
        self.tree_goblin_list = None
        self.wall_list = None
        self.coinbox_list = None
        self.coin_list = None
        self.box_list = None
        self.explosions_list = None
        self.explodingbox_list = None
        self.fireball_list = None
        self.bullet_list = None

        # Set up the player
        self.player_sprite = None
        self.mana_bar_sprite = None
        self.LIVES_text = None
        self.score = 0
        self.score_text = None

        # Set up the goblins
        self.goblin_sprite = None

        # Physics engine so we don't run into walls.
        self.physics_engine = None
        self.boxes_physics_engine = None
        self.coin_boxes_physics_engine = None
        self.goblin_boxes_physics_engine = None
        self.tree_goblin_physics_engine = None
        self.tree_goblin_boxes_physics_engine = None
        self.entity_physics_engine = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        # Store our tile map
        self.tile_map = None

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

        # Load explosion textures
        self.explosion_texture_list = []
        columns = 5
        count = 25
        sprite_width = 98
        sprite_height = 96
        file_name = "boom.png"
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

        # Load coin textures
        self.coin_texture_list = []
        columns = 3
        count = 12
        sprite_width = 64
        sprite_height = 64
        file_name = "Coin.png"
        self.coin_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

        # Load sounds
        self.fireball_sound = arcade.sound.load_sound("laser.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/hurt1.wav")
        self.explosion_sound = arcade.sound.load_sound(":resources:sounds/explosion2.wav")
        self.coin_sound = arcade.sound.load_sound(":resources:sounds/coin1.wav")

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.goblin_list = arcade.SpriteList()
        self.tree_goblin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coinbox_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.box_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.explodingbox_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # --- Load our map

        # Read in the tiled map
        map_name = "Level1.json"
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        # Set wall and coin SpriteLists
        # Any other layers here. Array index must be a layer.
        self.wall_list = self.tile_map.sprite_lists["Walls"]
        self.coinbox_list = self.tile_map.sprite_lists["Coin Boxes"]
        self.box_list = self.tile_map.sprite_lists["Boxes"]
        self.explodingbox_list = self.tile_map.sprite_lists["Explodey Boxes"]

        # self.coin_list = self.tile_map.sprite_lists["Coins"]

        # --- Other stuff

        # Set up the player
        def draw_player(x, y):
            player_texture_list = arcade.load_spritesheet("Wiz.png", 64, 64, 3, 8)
            self.player_sprite = Player(player_texture_list)  # arcade.load_spritesheet("Wiz.png", 128, 128, 3, 12)
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y
            self.player_list.append(self.player_sprite)
        draw_player(256, 512)


        mana_texture_list = arcade.load_spritesheet("Mana.png", 64, 128, 4, 7)
        self.mana_bar_sprite = Mana_Bar(mana_texture_list)

        # Set up the Goblins
        def draw_goblin(x, y):
            goblin_texture_list = arcade.load_spritesheet("Gob.png", 64, 64, 1, 2)
            self.goblin_sprite = Goblin(goblin_texture_list, self.wall_list, self.box_list, self.coinbox_list)
            self.goblin_sprite.center_x = x
            self.goblin_sprite.center_y = y
            self.goblin_list.append(self.goblin_sprite)
        #draw_goblin(500, 200)
        #draw_goblin(900, 250)
        #draw_goblin(1000, 200)

        # Set up Tree Goblins
        def draw_tree_goblin(x, y):
            tree_goblin_texture_list = arcade.load_spritesheet("Tree_Gob.png", 128, 128, 2, 3)
            self.tree_goblin_sprite = Tree_Goblin(tree_goblin_texture_list)
            self.tree_goblin_sprite.center_x = x
            self.tree_goblin_sprite.center_y = y
            self.tree_goblin_list.append(self.tree_goblin_sprite)
        draw_tree_goblin(1771, 342)

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Keep player from running through the wall_list layer
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.wall_list,
            gravity_constant=GRAVITY
        )
        self.tree_goblin_physics_engine = arcade.PhysicsEnginePlatformer(
            self.tree_goblin_sprite,
            self.wall_list,
            gravity_constant=GRAVITY
        )
        self.tree_goblin_boxes_physics_engine = arcade.PhysicsEnginePlatformer(
            self.tree_goblin_sprite,
            self.box_list,
            gravity_constant=0
        )
        self.entity_physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.goblin_list,
            gravity_constant=0
        )

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.wall_list.draw()
        self.coinbox_list.draw()
        self.coin_list.draw()
        self.box_list.draw()
        self.explosions_list.draw()
        self.explodingbox_list.draw()
        self.player_list.draw()
        self.goblin_list.draw()
        self.tree_goblin_list.draw()
        self.fireball_list.draw()
        self.bullet_list.draw()

        # Draw the mana bar
        self.mana_bar_sprite.center_x = 50 + self.camera_sprites.position[0]
        self.mana_bar_sprite.center_y = 150 + self.camera_sprites.position[1]
        self.mana_bar_sprite.draw()


        output = f"Score: {self.score}"
        arcade.draw_text(output, 10 + self.camera_sprites.position[0], 40 + self.camera_sprites.position[1],
                         arcade.color.WHITE, 14)

        output = f"Lives: {self.LIVES}"
        arcade.draw_text(output, 10 + self.camera_sprites.position[0], 20 + self.camera_sprites.position[1],
                         arcade.color.WHITE, 14)
        if self.LIVES == 0:
            gameover = "Game Over!"
            arcade.draw_text(gameover, self.camera_sprites.position[0] + 200, DEFAULT_SCREEN_HEIGHT / 2,
                             arcade.color.WHITE, 14)
            gameover = "Tap anywhere to restart."
            arcade.draw_text(gameover, self.camera_sprites.position[0] + 200, DEFAULT_SCREEN_HEIGHT / 2 - 20,
                             arcade.color.WHITE, 14)
            self.player_sprite.remove_from_sprite_lists()



        """# Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Draw the GUI
        arcade.draw_rectangle_filled(self.width // 2,
                                     20,
                                     self.width,
                                     40,
                                     arcade.color.ALMOND)
        text = f"Scroll value: ({self.camera_sprites.position[0]:5.1f}, " \
               f"{self.camera_sprites.position[1]:5.1f})"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)"""

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
            elif self.boxes_physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
            elif self.coin_boxes_physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
            elif arcade.check_for_collision_with_list(self.player_sprite, self.coin_list) is True:
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        if self.LIVES > 0:
            if self.MANA > 0:
                # Create a fireball
                fireball = arcade.Sprite("fireball.gif", SPRITE_SCALING)
                arcade.play_sound(self.fireball_sound)

                # Position the fireball at the player's current location
                start_x = self.player_sprite.center_x
                start_y = self.player_sprite.center_y
                fireball.center_x = start_x
                fireball.center_y = start_y

                # Get from the mouse the destination location for the fireball
                # Adjust mouse coordinates based on camera position
                dest_x = x + self.camera_sprites.position[0]
                dest_y = y + self.camera_sprites.position[1]

                # Do math to calculate how to get the fireball to the destination.
                # Calculation the angle in radians between the start points
                # and end points. This is the angle the fireball will travel.
                x_diff = (dest_x - start_x) * DEFAULT_SCREEN_WIDTH
                y_diff = (dest_y - start_y) * DEFAULT_SCREEN_HEIGHT
                angle = math.atan2(y_diff, x_diff)

                # Angle the fireball sprite so it doesn't look like it is flying
                # sideways.
                fireball.angle = math.degrees(angle)
                print(f"Fireball angle: {fireball.angle:.2f}")

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the fireball travels.
                fireball.change_x = math.cos(angle) * PROJECTILE_SPEED
                fireball.change_y = math.sin(angle) * PROJECTILE_SPEED

                # Add the fireball to the appropriate lists
                self.fireball_list.append(fireball)
                self.MANA -= 1

        else:
            self.setup()
            self.LIVES = 3
            self.score = 0
            self.MANA = 6

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.explosions_list.update()
        self.coin_list.update()

        if self.LIVES > 0:
            # Update everything.
            if self.MANA == 6:
                self.mana_bar_sprite.update(0)
            elif self.MANA == 5:
                self.mana_bar_sprite.update(1)
            elif self.MANA == 4:
                self.mana_bar_sprite.update(2)
            elif self.MANA == 3:
                self.mana_bar_sprite.update(3)
            elif self.MANA == 2:
                self.mana_bar_sprite.update(4)
            elif self.MANA == 1:
                self.mana_bar_sprite.update(5)
            else:
                self.mana_bar_sprite.update(6)
            self.fireball_list.update()
            self.goblin_list.update()
            self.bullet_list.update()
            if self.tree_goblin_sprite.lives == 2:
                self.tree_goblin_sprite.update(0, 0)
            elif self.tree_goblin_sprite.lives == 1:
                self.tree_goblin_sprite.update(1, 1)
            else:
                self.tree_goblin_sprite.update(2, 2)

            # Calculate speed based on the keys pressed
            self.player_sprite.change_x = 0
            # self.player_sprite.change_y = 0

            if self.left_pressed and not self.right_pressed:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                self.player_sprite.update(0, 4)
                self.last_move = 'left'
            elif self.right_pressed and not self.left_pressed:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
                self.player_sprite.update(5, 7)
                self.last_move = 'right'
            else:
                if self.last_move == 'left':
                    self.player_sprite.update(0, 0)
                else:
                    self.player_sprite.update(7, 7)

            # Call update on all sprites (The sprites don't do much in this
            # example though.)
            self.physics_engine.update()
            self.boxes_physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                self.box_list,
                gravity_constant=0
            )
            self.boxes_physics_engine.update()
            self.coin_boxes_physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                self.coinbox_list,
                gravity_constant=0
            )
            self.coin_boxes_physics_engine.update()
            self.entity_physics_engine.update()
            self.tree_goblin_boxes_physics_engine.update()
            self.tree_goblin_physics_engine.update()

            # Scroll the screen to the player
            self.scroll_to_player()

            # Loop through each fireball
            for fireball in self.fireball_list:

                # Check this fireball to see if it hit a wall
                hit_list = arcade.check_for_collision_with_list(fireball, self.wall_list)
                # If it did, get rid of the fireball
                if len(hit_list) > 0:
                    fireball.remove_from_sprite_lists()
                # Check this fireball to see if it hit a tree goblin
                hit_list = arcade.check_for_collision_with_list(fireball, self.tree_goblin_list)
                # If it did, get rid of the fireball and goblin
                if len(hit_list) > 0 and self.tree_goblin_sprite.lives > 0:
                    arcade.play_sound(self.hit_sound)
                    fireball.remove_from_sprite_lists()
                    self.tree_goblin_sprite.lives -= 1
                    self.score += 5

                # Check this fireball to see if it flew too far
                num = 250
                max_x = self.player_sprite.center_x + num
                min_x = self.player_sprite.center_x - num
                max_y = self.player_sprite.center_y + num
                min_y = self.player_sprite.center_y - num
                if fireball.center_x > max_x or fireball.center_x < min_x or fireball.center_y > max_y or fireball.center_y < min_y:
                    fireball.remove_from_sprite_lists()

            # Goblin follows player
            # if

            self.frame_count += 1

            if self.MANA < 6 and self.frame_count % 100 == 0:
                self.MANA += 1

            for box in self.box_list:
                # Check this bullet to see if it hit a wall
                hit_list = arcade.check_for_collision_with_list(box, self.fireball_list)
                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    arcade.play_sound(self.hit_sound)
                    box.remove_from_sprite_lists()
                    fireball.remove_from_sprite_lists()

            for coin_box in self.coinbox_list:
                # Check this bullet to see if it hit a wall
                hit_list = arcade.check_for_collision_with_list(coin_box, self.fireball_list)
                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    # Make an explosion
                    coin = Coin(self.coin_texture_list)
                    # Move it to the location of the box
                    coin.center_x = coin_box.center_x
                    coin.center_y = coin_box.center_y
                    # Call update() because it sets which image we start on
                    coin.update()
                    # Add to a list of sprites that are explosions
                    self.coin_list.append(coin)
                    coin_box.remove_from_sprite_lists()
                    fireball.remove_from_sprite_lists()
                    arcade.play_sound(self.coin_sound)

            for exploding_box in self.explodingbox_list:
                # Check the box was hit
                hit_list = arcade.check_for_collision_with_list(exploding_box, self.fireball_list)
                # If it was, get rid of the box and fireball
                if len(hit_list) > 0:
                    # Make an explosion
                    explosion = Explosion(self.explosion_texture_list)
                    # Move it to the location of the box
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    # Call update() because it sets which image we start on
                    explosion.update()
                    # Add to a list of sprites that are explosions
                    self.explosions_list.append(explosion)
                    exploding_box.remove_from_sprite_lists()
                    fireball.remove_from_sprite_lists()
                    arcade.play_sound(self.explosion_sound)
                hit_list = arcade.check_for_collision_with_list(exploding_box, self.player_list)
                if len(hit_list) > 0:
                    # Make an explosion
                    explosion = Explosion(self.explosion_texture_list)
                    # Move it to the location of the box
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    # Call update() because it sets which image we start on
                    explosion.update()
                    # Add to a list of sprites that are explosions
                    self.explosions_list.append(explosion)
                    exploding_box.remove_from_sprite_lists()
                    self.LIVES = 0
                    arcade.play_sound(self.explosion_sound)

            if self.tree_goblin_sprite.lives > 0:
                # Loop through each tree goblin that we have
                for goblin in self.tree_goblin_list:
                    # First, calculate the angle to the player. We could do this
                    # only when the bullet fires, but in this case we will rotate
                    # the enemy to face the player each frame, so we'll do this
                    # each frame.

                    # Position the start at the enemy's current location
                    start_x = goblin.center_x
                    start_y = goblin.center_y - 50

                    # Get the destination location for the bullet
                    dest_x = self.player_sprite.center_x
                    dest_y = self.player_sprite.center_y

                    # Do math to calculate how to get the bullet to the destination.
                    # Calculation the angle in radians between the start points
                    # and end points. This is the angle the bullet will travel.
                    x_diff = dest_x - start_x
                    y_diff = dest_y - start_y
                    angle = math.atan2(y_diff, x_diff)


                    # Shoot every 60-180 frames change of shooting each frame
                    if self.frame_count % random.randint(20, 100) == 0:
                        bullet = arcade.Sprite("bullet.png", SPRITE_SCALING)
                        bullet.center_x = start_x
                        bullet.center_y = start_y

                        # Angle the bullet sprite
                        bullet.angle = math.degrees(angle)

                        # Taking into account the angle, calculate our change_x
                        # and change_y. Velocity is how fast the bullet travels.
                        bullet.change_x = math.cos(angle) * PROJECTILE_SPEED
                        bullet.change_y = math.sin(angle) * PROJECTILE_SPEED

                        self.bullet_list.append(bullet)

                    if self.tree_goblin_sprite.lives == 2:
                        # First, calculate the angle to the player. We could do this
                        # only when the bullet fires, but in this case we will rotate
                        # the enemy to face the player each frame, so we'll do this
                        # each frame.

                        # Position the start at the enemy's current location
                        start_x = goblin.center_x
                        start_y = goblin.center_y

                        # Get the destination location for the bullet
                        dest_x = self.player_sprite.center_x
                        dest_y = self.player_sprite.center_y

                        # Do math to calculate how to get the bullet to the destination.
                        # Calculation the angle in radians between the start points
                        # and end points. This is the angle the bullet will travel.
                        x_diff = dest_x - start_x
                        y_diff = dest_y - start_y
                        angle = math.atan2(y_diff, x_diff)

                        # Shoot every 60-180 frames change of shooting each frame
                        if self.frame_count % random.randint(20, 100) == 0:
                            bullet = arcade.Sprite("bullet.png", SPRITE_SCALING)
                            bullet.center_x = start_x
                            bullet.center_y = start_y

                            # Angle the bullet sprite
                            bullet.angle = math.degrees(angle)

                            # Taking into account the angle, calculate our change_x
                            # and change_y. Velocity is how fast the bullet travels.
                            bullet.change_x = math.cos(angle) * (PROJECTILE_SPEED + 2)
                            bullet.change_y = math.sin(angle) * (PROJECTILE_SPEED + 2)

                            self.bullet_list.append(bullet)

                        # Loop through each standard goblin that we have
                    for goblin in self.goblin_list:

                        hit_list = arcade.check_for_collision_with_list(goblin, self.fireball_list)
                        # If it did, get rid of the fireball and goblin
                        if len(hit_list) > 0:
                            goblin.remove_from_sprite_lists()
                            fireball.remove_from_sprite_lists()
                            arcade.play_sound(self.hit_sound)
                            self.score += 5

                        # First, calculate the angle to the player. We could do this
                        # only when the bullet fires, but in this case we will rotate
                        # the enemy to face the player each frame, so we'll do this
                        # each frame.

                        # Position the start at the enemy's current location
                        start_x = goblin.center_x
                        start_y = goblin.center_y

                        # Get the destination location for the bullet
                        dest_x = self.player_sprite.center_x
                        dest_y = self.player_sprite.center_y

                        # Do math to calculate how to get the bullet to the destination.
                        # Calculation the angle in radians between the start points
                        # and end points. This is the angle the bullet will travel.
                        x_diff = dest_x - start_x
                        y_diff = dest_y - start_y
                        angle = math.atan2(y_diff, x_diff)

                        # Set the enemy to face the player.
                        # goblin.angle = math.degrees(angle) + 180

                        # Make the enemy follow the player if they are close enough
                        if math.fabs(goblin.center_x - self.player_sprite.center_x) <= 300:
                            if goblin.center_x > self.player_sprite.center_x:
                                goblin.center_x -= GOBLIN_MOVEMENT_SPEED
                                goblin.set_texture(0)
                            elif goblin.center_x < self.player_sprite.center_x:
                                goblin.center_x += GOBLIN_MOVEMENT_SPEED
                                goblin.set_texture(1)

                        # Shoot every 60-180 frames change of shooting each frame
                        if self.frame_count % random.randint(20, 100) == 0:
                            bullet = arcade.Sprite("bullet.png", SPRITE_SCALING)
                            bullet.center_x = start_x
                            bullet.center_y = start_y

                            # Angle the bullet sprite
                            bullet.angle = math.degrees(angle)

                            # Taking into account the angle, calculate our change_x
                            # and change_y. Velocity is how fast the bullet travels.
                            bullet.change_x = math.cos(angle) * PROJECTILE_SPEED
                            bullet.change_y = math.sin(angle) * PROJECTILE_SPEED

                            self.bullet_list.append(bullet)

            for bullet in self.bullet_list:

                # Check this bullet to see if it hit a wall
                hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    bullet.remove_from_sprite_lists()
                # Check this bullet to see if it hit a goblin
                hit_list = arcade.check_for_collision_with_list(bullet, self.player_list)
                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    bullet.remove_from_sprite_lists()
                    self.LIVES -= 1
                    arcade.play_sound(self.hit_sound)
                # Check if this bullet hit a fireball
                hit_list = arcade.check_for_collision_with_list(bullet, self.fireball_list)
                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    bullet.remove_from_sprite_lists()
                    fireball.remove_from_sprite_lists()

                # Check this bullet to see if it flew too far
                num = 500
                max_x = self.player_sprite.center_x + num
                min_x = self.player_sprite.center_x - num
                max_y = self.player_sprite.center_y + num
                min_y = self.player_sprite.center_y - num
                if bullet.center_x > max_x or bullet.center_x < min_x or bullet.center_y > max_y or bullet.center_y < min_y:
                    bullet.remove_from_sprite_lists()

            for coin in self.coin_list:
                hit_list = arcade.check_for_collision_with_list(coin, self.fireball_list)
                if len(hit_list) > 0:
                    arcade.play_sound(self.coin_sound)
                    coin.remove_from_sprite_lists()
                    fireball.remove_from_sprite_lists()
                    self.score += 1
                hit_list = arcade.check_for_collision_with_list(coin, self.player_list)
                if len(hit_list) > 0:
                    arcade.play_sound(self.coin_sound)
                    coin.remove_from_sprite_lists()
                    self.score += 1
                hit_list = arcade.check_for_collision_with_list(coin, self.bullet_list)
                if len(hit_list) > 0:
                    arcade.play_sound(self.hit_sound)
                    coin.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()

            if self.player_sprite.center_y < -300:
                self.LIVES = 0

    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a
        smoother pan.
        """

        position = self.player_sprite.center_x - self.width / 2, \
                   (DEFAULT_SCREEN_HEIGHT-600) / 2
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    """ Main function """
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()