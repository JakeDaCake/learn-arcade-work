"""
Sprite Bullets

Simple program to show basic sprite usage.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_bullets_aimed
"""

import random
import arcade
import math
import os

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_FIREBALL = 0.5
SPRITE_SCALING_BULLET = 0.5
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Goblins with Guns v1.1"

BULLET_SPEED = 5
MOVEMENT_SPEED = 3

window = None


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.LIVES = 3

        # Variables that will hold sprite lists

        self.frame_count = 0

        self.player_list = None
        self.enemy_list = None
        self.coin_list = None
        self.bullet_list = None
        self.enemybullet_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = None
        self.LIVES_text = None

        # Load sounds.
        self.fireball_sound = arcade.sound.load_sound("../GoblinsWithGuns/laser.wav")
        self.coin_sound = arcade.sound.load_sound(":resources:sounds/coin1.wav")

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def setup(self):

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemybullet_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Player setup
        self.player_sprite = arcade.Sprite("../GoblinsWithGuns/Wiz.gif", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        # Enemy setup
        self.enemy_sprite = arcade.Sprite("../GoblinsWithGuns/Gob.png", SPRITE_SCALING_PLAYER)
        self.enemy_sprite.center_x = SCREEN_WIDTH/3
        self.enemy_sprite.center_y = SCREEN_HEIGHT-50
        self.enemy_list.append(self.enemy_sprite)

        self.enemy_sprite = arcade.Sprite("../GoblinsWithGuns/Gob.png", SPRITE_SCALING_PLAYER)
        self.enemy_sprite.center_x = (SCREEN_WIDTH/3)*2
        self.enemy_sprite.center_y = SCREEN_HEIGHT-50
        self.enemy_list.append(self.enemy_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            coin = arcade.load_spritesheet("Coin.png", 128, 128, 3, 4)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120, SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.coin_list.draw()
        self.bullet_list.draw()
        self.enemybullet_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 40, arcade.color.WHITE, 14)
        output = f"Lives: {self.LIVES}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        if self.LIVES <= 0:
            gameover = "Game Over!"
            arcade.draw_text(gameover, 350, 300, arcade.color.WHITE, 14)
            gameover = "Tap anywhere to restart."
            arcade.draw_text(gameover, 305, 280, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        if self.player_sprite.left < 0:
            self.player_sprite.left = 0

        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        if self.LIVES != 0:
            # Create a bullet
            bullet = arcade.Sprite("../GoblinsWithGuns/fireball.gif", SPRITE_SCALING_FIREBALL)
            arcade.play_sound(self.fireball_sound)

            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y

            # Get from the mouse the destination location for the bullet
            # IMPORTANT! If you have a scrolling screen, you will also need
            # to add in self.view_bottom and self.view_left.
            dest_x = x
            dest_y = y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            bullet.angle = math.degrees(angle)
            print(f"Bullet angle: {bullet.angle:.2f}")

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

        else:
            self.setup()
            self.on_draw()
            self.score = 0
            self.LIVES = 3

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        if self.LIVES != 0:
            self.bullet_list.update()
            self.enemybullet_list.update()
            self.player_list.update()
            self.enemy_list.update()

            # Loop through each bullet
            for bullet in self.bullet_list:

                # Check this bullet to see if it hit a coin
                hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    bullet.remove_from_sprite_lists()

                # For every coin we hit, add to the score and remove the coin
                for coin in hit_list:
                    coin.remove_from_sprite_lists()
                    self.score += 1
                    arcade.play_sound(self.coin_sound)

                # If the bullet flies off-screen, remove it.
                if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                    bullet.remove_from_sprite_lists()


            self.frame_count += 1

            # Loop through each enemy that we have
            for enemy in self.enemy_list:

                # First, calculate the angle to the player. We could do this
                # only when the bullet fires, but in this case we will rotate
                # the enemy to face the player each frame, so we'll do this
                # each frame.

                # Position the start at the enemy's current location
                start_x = enemy.center_x
                start_y = enemy.center_y

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
                enemy.angle = math.degrees(angle) + 180

                # Shoot every 60-180 frames change of shooting each frame
                if self.frame_count % 60 == 0:
                    enemybullet = arcade.Sprite("bullet.png", SPRITE_SCALING_BULLET)
                    enemybullet.center_x = start_x
                    enemybullet.center_y = start_y

                    # Angle the bullet sprite
                    enemybullet.angle = math.degrees(angle)

                    # Taking into account the angle, calculate our change_x
                    # and change_y. Velocity is how fast the bullet travels.
                    enemybullet.change_x = math.cos(angle) * BULLET_SPEED
                    enemybullet.change_y = math.sin(angle) * BULLET_SPEED

                    self.enemybullet_list.append(enemybullet)

            # Get rid of the bullet when it flies off-screen
            for enemybullet in self.enemybullet_list:
                if enemybullet.top < 0:
                    enemybullet.remove_from_sprite_lists()

                hit_list = arcade.check_for_collision_with_list(enemybullet, self.player_list)

                if len(hit_list) > 0:
                    enemybullet.remove_from_sprite_lists()

                # For every coin we hit, add to the score and remove the coin
                for player in hit_list:
                    self.LIVES -= 1
                    if self.LIVES <= 0:
                        player.remove_from_sprite_lists()
            self.bullet_list.update()
            self.enemybullet_list.update()


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()