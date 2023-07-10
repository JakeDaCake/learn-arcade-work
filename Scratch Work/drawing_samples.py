"""
Hello, my name is Bob Ross, and welcome to 'The Joy of Drawing with Python'
Remember, there are no mistakes, only happy accidents.
"""

import arcade

#  opens window
arcade.open_window(600, 600, "Drawing Example")

#  sets bg color
arcade.set_background_color(arcade.csscolor.SKY_BLUE)

#  gets ready to draw
arcade.start_render()

#  DRAWING CODE:
arcade.draw_lrtb_rectangle_filled(0, 599, 300, 0, arcade.csscolor.GREEN)

arcade.draw_lrtb_rectangle_filled(100, 120, 350, 290, arcade.csscolor.SIENNA)
arcade.draw_circle_filled(110, 350, 30, arcade.csscolor.DARK_GREEN)

arcade.draw_lrtb_rectangle_filled(200, 220, 350, 290, arcade.csscolor.SIENNA)
arcade.draw_ellipse_filled(210, 380, 60, 80, arcade.csscolor.DARK_GREEN)

arcade.draw_lrtb_rectangle_filled(300, 320, 350, 290, arcade.csscolor.SIENNA)
arcade.draw_arc_filled(310, 350, 60, 100, arcade.csscolor.DARK_GREEN, 0, 180)

arcade.draw_lrtb_rectangle_filled(400, 420, 350, 290, arcade.csscolor.SIENNA)
arcade.draw_triangle_filled(410, 500, 370, 320, 450, 320, arcade.csscolor.DARK_GREEN)

arcade.draw_lrtb_rectangle_filled(500, 520, 350, 290, arcade.csscolor.SIENNA)
arcade.draw_polygon_filled(((510, 400),
                            (490, 360),
                            (480, 320),
                            (540, 320),
                            (530, 360)
                            ),
                           arcade.csscolor.DARK_GREEN)

arcade.draw_circle_filled(500, 550, 40, arcade.color.YELLOW)
arcade.draw_line(500, 550, 400, 550, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 600, 550, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 500, 450, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 500, 650, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 550, 600, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 550, 500, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 450, 600, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 450, 500, arcade.color.YELLOW, 3)

arcade.draw_text("This drawing was made by Jake B)", 150, 250, arcade.csscolor.WHITE, 15)

#  finish drawing
arcade.finish_render()

#  runs the program
arcade.run()
