""" Sprite Sample Program """

import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 100
SPRITE_SCALING_BOMB = .5
BOMB_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

done = False


class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()


class Bomb(arcade.Sprite):
    """
    This class represents the bombs on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the bomb to a random spot above the screen
        self.center_x = random.randrange(SCREEN_WIDTH + 20,
                                         SCREEN_WIDTH + 300)
        self.center_y = random.randrange(SCREEN_HEIGHT)

    def update(self):

        # Move the coin
        self.center_x -= 2

        # See if the bomb has fallen off the bottom of the screen.
        # If so, reset it.
        if self.center_x < -20:
            self.reset_pos()


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite("wiz.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin("coin.gif", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

        for i in range(BOMB_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            bomb = Bomb("Bomba.gif", SPRITE_SCALING_BOMB)

            # Position the coin
            bomb.center_x = random.randrange(SCREEN_WIDTH)
            bomb.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.bomb_list.append(bomb)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()
        self.bomb_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.bomb_list.update()

        # Generate a list of all sprites that collided with the player.
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)
        bomb_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                 self.bomb_list)

        # Load coin collect sound
        coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        bomb_sound = arcade.load_sound("laser.wav")

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(coin_sound)
            # check if there are any coins left
            if len(self.coin_list) <= 0:
                # Put the text on the screen.
                print("You finished with " + str(self.score) + " points!")


        for bomb in bomb_hit_list:
            bomb.reset_pos()
            self.score -= 1
            arcade.play_sound(bomb_sound)

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()