from turtle import Turtle
from random import randint

# Define Functions
def draw_rectangle(artist, fill_color, start_x, start_y, rect_width, rect_height):
    artist.penup()
    artist.color(fill_color)
    artist.fillcolor(fill_color)
    artist.goto(start_x, start_y)
    artist.pendown()
    artist.begin_fill()
    for _ in range(2):
        artist.forward(rect_width)
        artist.left(90)
        artist.forward(rect_height)
        artist.left(90)
    artist.end_fill()
    artist.setheading(0)

def draw_circle(artist, center_x, center_y, circle_radius, color):
    artist.penup()
    artist.color(color)
    artist.fillcolor(color)
    artist.goto(center_x, center_y - circle_radius)
    artist.pendown()
    artist.begin_fill()
    artist.circle(circle_radius)
    artist.end_fill()

# Initialize the Turtle object
master_oshos = Turtle()

master_oshos.speed(2)
canvas = master_oshos.getscreen()

# Set background color and title
canvas.bgcolor("darkblue")
canvas.title("Festive Greetings")

canvas.setup(width=3.0, height=3.0)

y_position = -100

# Draw the tree trunk
draw_rectangle(master_oshos, "brown", -20, y_position-90, 60, 90)

# Draw the Christmas tree
tree_width = 340
master_oshos.speed(20)
while tree_width > 20:
    tree_width -= 20
    tree_height = 15
    x_position = 0 - tree_width/2
    draw_rectangle(master_oshos, "darkgreen", x_position, y_position, tree_width, tree_height)
    y_position += tree_height

# Draw a star on top of the tree
master_oshos.speed(1)
master_oshos.penup()
master_oshos.color('gold')
master_oshos.goto(-25, y_position+15)
master_oshos.begin_fill()
master_oshos.pendown()
for i in range(5):
    master_oshos.forward(50)
    master_oshos.right(144)
master_oshos.end_fill()

# Decorate the tree with colorful ornaments
ornament_positions = [(20, 80, "silver", 12), (-50, 40, "purple", 18),
                      (40, 0, "pink", 12), (95, -90, "darkgreen", 22),
                      (-40, -50, "lightblue", 18), (-120, -110, "gold", 25)]
for x, y, color, size in ornament_positions:
    master_oshos.penup()
    master_oshos.goto(x, y)
    master_oshos.color(color)
    master_oshos.begin_fill()
    master_oshos.circle(size)
    master_oshos.end_fill()

tree_top_y = y_position + 50

# Draw the moon and then cover it partially to create a crescent shape
draw_circle(master_oshos, 250, 200, 70, "white")
draw_circle(master_oshos, 235, 200, 70, "lightblue")

# Draw stars in the sky
master_oshos.speed(10)
number_of_stars = randint(15,25)
for _ in range(number_of_stars):
    x_star = randint(-(canvas.window_width()//2), canvas.window_width()//2)
    y_star = randint(tree_top_y, canvas.window_height()//2)
    star_size = randint(3,15)
    master_oshos.penup()
    master_oshos.color('white')
    master_oshos.goto(x_star, y_star)
    master_oshos.begin_fill()
    master_oshos.pendown()
    for i in range(5):
        master_oshos.forward(star_size)
        master_oshos.right(144)
    master_oshos.end_fill()

# Display festive messages
master_oshos.speed(1)
master_oshos.penup()

messages = [("🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄", -220, "red", 30),
            ("HAPPY HOLIDAYS FROM MR OSHOS", -320, "gold", 45)]
for msg, y, color, font_size in messages:
    master_oshos.goto(0, y)
    master_oshos.color(color)
    master_oshos.write(msg, move=False, align="center", font=("Arial", font_size, "bold"))

master_oshos.hideturtle()
canvas.mainloop()
