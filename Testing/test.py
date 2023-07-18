import arcade


def draw_snowman(x, y):

    arcade.draw_circle_filled(x, y, 25, (182, 201, 207))
    arcade.draw_circle_filled(x, y + 20, 20, (182, 201, 207))
    arcade.draw_circle_filled(x, y + 40, 15, (182, 201, 207))
    arcade.draw_lrtb_rectangle_filled(x - 20, x + 20, y + 50, y + 45, arcade.color.BLACK_LEATHER_JACKET)
    arcade.draw_lrtb_rectangle_filled(x - 10, x + 10, y + 70, y + 45, arcade.color.BLACK_LEATHER_JACKET)
    arcade.draw_triangle_filled(x, y + 40, x, y + 35, x - 20, y + 37.5, arcade.color.OUTRAGEOUS_ORANGE)

def main():
    arcade.open_window(300, 300, "Sound Demo")
    arcade.start_render()
    arcade.set_background_color(arcade.color.ASH_GREY)
    draw_snowman(100, 100)
    draw_snowman(200, 200)
    draw_snowman(150, 50)
    draw_snowman(69, 69)
    arcade.run()