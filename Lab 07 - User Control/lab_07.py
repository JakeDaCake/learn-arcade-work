""" Lab 7 - User Control """

import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 3


def draw_house(x, y):
    arcade.draw_lrtb_rectangle_filled(x, (x + 100), (y + 80), y, arcade.color.TAN)
    arcade.draw_lrtb_rectangle_filled((x + 60), (x + 90), (y + 150), y, arcade.color.TAN)
    arcade.draw_triangle_filled((x-20), (y + 80), (x + 120), (y + 80), (x + 50), (y + 150), arcade.color.MAHOGANY)
    arcade.draw_lrtb_rectangle_filled((x + 10), (x + 40), (y + 50), y, arcade.color.BROWN)
    arcade.draw_lrtb_rectangle_filled((x + 60), (x + 90), (y + 60), (y + 20), (100, 150, 163))


class Ball:
    def __init__(self, position_x, position_y, radius, change_x, change_y):

        # Take the parameters of the init function above,
        # and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.change_x = change_x
        self.change_y = change_y

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, (182, 201, 207))
        arcade.draw_circle_filled(self.position_x, self.position_y + 20, 20, (182, 201, 207))
        arcade.draw_circle_filled(self.position_x, self.position_y + 40, 15, (182, 201, 207))
        arcade.draw_lrtb_rectangle_filled(self.position_x - 20, self.position_x + 20, self.position_y + 50, self.position_y + 45, arcade.color.BLACK_LEATHER_JACKET)
        arcade.draw_lrtb_rectangle_filled(self.position_x - 10, self.position_x + 10, self.position_y + 70, self.position_y + 45, arcade.color.BLACK_LEATHER_JACKET)
        arcade.draw_triangle_filled(self.position_x, self.position_y + 40, self.position_x, self.position_y + 35, self.position_x - 20, self.position_y + 37.5, arcade.color.OUTRAGEOUS_ORANGE)

    def update(self):
        # Move the ball
        self.position_y += self.change_y
        self.position_x += self.change_x

        hit_side = arcade.load_sound(":resources:sounds/rockHit2.wav")

        # See if the ball hit the edge of the screen. If so, change direction
        if self.position_x < self.radius:
            self.position_x = self.radius
            arcade.play_sound(hit_side)

        if self.position_x > SCREEN_WIDTH - self.radius:
            self.position_x = SCREEN_WIDTH - self.radius
            arcade.play_sound(hit_side)

        if self.position_y < self.radius + 50:
            self.position_y = self.radius + 50
            arcade.play_sound(hit_side)

        if self.position_y > SCREEN_HEIGHT - 70:
            self.position_y = SCREEN_HEIGHT - 70
            arcade.play_sound(hit_side)


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")

        self.ball = Ball(50, 50, 25, 0, 0)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, 50, 0, arcade.color.DARK_GREEN)
        draw_house(100, 50)
        self.ball.draw()

    def update(self, delta_time):
        self.ball.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.ball.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.ball.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.ball.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.ball.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ball.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.ball.change_y = 0


def main():
    window = MyGame()
    arcade.run()


main()