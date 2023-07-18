import arcade
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class Ball:
    """ This class manages a ball bouncing on the screen. """

    def __init__(self, position_x, position_y, change_x, change_y, radius):
        """ Constructor. """

        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)

        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = (r, g, b)

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self):
        """ Code to control the ball's movement. """

        # Move the ball
        self.position_y += self.change_y
        self.position_x += self.change_x

        klonk = arcade.load_sound(":resources:sounds/rockHit2.wav")

        # See if the ball hit the edge of the screen. If so, change direction
        if self.position_x < self.radius:  # left
            self.change_x *= -1
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            arcade.play_sound(klonk)

        if self.position_x > SCREEN_WIDTH - self.radius:  # right
            self.change_x *= -1
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            arcade.play_sound(klonk)

        if self.position_y < self.radius:  # bottom
            self.change_y *= -1
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            arcade.play_sound(klonk)

        if self.position_y > SCREEN_HEIGHT - self.radius:  # top
            self.change_y *= -1
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            arcade.play_sound(klonk)


class MyGame(arcade.Window):
    """ My window class. """

    def __init__(self, width, height, title):
        """ Constructor. """

        # Call the parent class's init function
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Create a list for the balls
        self.ball_list = []

        # Add three balls to the list
        ball = Ball(50, 50, 3, 3, 15)
        self.ball_list.append(ball)

        ball = Ball(100, 150, 2, 3, 15)
        self.ball_list.append(ball)

        ball = Ball(100, 150, 4, 6, 15)
        self.ball_list.append(ball)

        ball = Ball(150, 250, -3, -1, 15)
        self.ball_list.append(ball)

        ball = Ball(200, 400, -5, 2, 15)
        self.ball_list.append(ball)

        ball = Ball(300, 50, 1, -6, 15)
        self.ball_list.append(ball)
    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        # Use a "for" loop to pull each ball from the list, then call the draw
        # method on that ball.
        for ball in self.ball_list:
            ball.draw()
    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second."""
        for ball in self.ball_list:
            ball.update()


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Balls")
    arcade.run()


main()