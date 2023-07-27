import arcade


class Ball:
    def __init__(self):
        # --- Clss Attributes ---
        # Ball position
        self.x = 0
        self.y = 0

        # Ball's vector
        self.change_x = 0
        self.change_y = 0

        # Ball size
        self.size = 10

        # Ball color
        self.color = [255, 255, 255]

    # --- Class Methods ---
    def move(self):
        self.x += self.change_x
        self.y += self.change_y

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)


the_ball = Ball()
the_ball.x = 100
the_ball.y = 100
the_ball.change_x = 2
the_ball.change_y = 1
the_ball.color = [255, 0, 0]

def main():
    arcade.open_window(600, 600, "Ball")
    the_ball.move()
    the_ball.draw()
    arcade.run()

main()
