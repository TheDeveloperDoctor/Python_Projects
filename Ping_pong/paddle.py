from turtle import Turtle

class paddle(Turtle):
    # TODO: Implement a constructor which create a paddle
    def __init__(self,number):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.color("white")
        self.penup()
        self.score = 0
        if number == 1:
            self.goto(-350, 0)
        elif number == 2:
            self.goto(350, 0)

    # TODO: A function that will move it to up direction
    def go_up(self):
        if self.ycor() < 280:
            y = self.ycor()
            y += 30
            self.goto(self.xcor(), y)

    # TODO: A function that will move it to down direction
    def go_down(self):
        if self.ycor() > -280:
            y = self.ycor()
            y -= 30
            self.goto(self.xcor(), y)
