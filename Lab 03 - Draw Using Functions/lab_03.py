import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def draw_grass():
    arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT / 3, 0, arcade.color.WHITE)


def draw_tree(x, y):  # prints from the bottom left of the trunk
    arcade.draw_lrtb_rectangle_filled(x, (x + 30), (y + 50), y, arcade.csscolor.SIENNA)
    arcade.draw_triangle_filled((x - 20), (y + 50), (x + 50), (y + 50), (x + 15), (y + 200), arcade.csscolor.DARK_GREEN)


def draw_house(x, y):
    arcade.draw_lrtb_rectangle_filled(x, (x + 100), (y + 80), y, arcade.color.TAN)
    arcade.draw_lrtb_rectangle_filled((x + 60), (x + 90), (y + 150), y, arcade.color.TAN)
    arcade.draw_triangle_filled((x-20), (y + 80), (x + 120), (y + 80), (x + 50), (y + 150), arcade.color.MAHOGANY)
    arcade.draw_lrtb_rectangle_filled((x + 10), (x + 40), (y + 50), y, arcade.color.BROWN)
    arcade.draw_lrtb_rectangle_filled((x + 60), (x + 90), (y + 60), (y + 20), (100, 150, 163))


def draw_snowman(x, y):
    """ Draw a snow person """

    arcade.draw_point(x, y, arcade.color.WHITE, 5)

    arcade.draw_circle_filled(x, 60 + y, 60, (182, 201, 207))
    arcade.draw_circle_filled(x, 140 + y, 50, (182, 201, 207))
    arcade.draw_circle_filled(x, 200 + y, 40, (182, 201, 207))

    arcade.draw_circle_filled(x - 15, 210 + y, 5, arcade.color.NAVY_BLUE)
    arcade.draw_circle_filled(x + 15, 210 + y, 5, arcade.color.NAVY_BLUE)
    arcade.draw_triangle_filled(x, (y + 200), x, (y + 180), (x - 50), (y + 190), arcade.color.OUTRAGEOUS_ORANGE)


def on_draw(delta_time):
    arcade.set_background_color(arcade.color.DARK_BLUE)
    arcade.start_render()
    draw_static_elements()
    draw_snowman(on_draw.snowman, -20)

    on_draw.snowman += 1


def draw_static_elements():
    draw_grass()
    draw_tree(800, 180)
    draw_tree(700, 180)
    draw_tree(600, 180)
    draw_tree(500, 180)
    draw_tree(400, 180)
    draw_tree(630, 150)
    draw_tree(60, 120)
    draw_tree(130, 80)
    draw_tree(710, 120)
    draw_tree(640, 70)
    draw_tree(350, 150)
    draw_tree(400, 80)
    draw_house(200, 180)


def main():

    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Drawing Example")
    on_draw.snowman = 150


    arcade.schedule(on_draw, 1/60)
    arcade.run()


main()