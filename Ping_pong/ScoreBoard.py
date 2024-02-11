from turtle import Turtle
class scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.L_score = 0
        self.R_score = 0

        self.update_ScoreBoard()
    def update_ScoreBoard(self):
        self.clear()
        self.goto(-100, 200)
        self.write(self.L_score, align="center", font=("Courier", 80, "normal"))
        self.goto(100, 200)
        self.write(self.R_score, align="center", font=("Courier", 80, "normal"))

    def l_score(self):
        self.R_score += 1
        self.update_ScoreBoard()
    def r_score(self):
        self.L_score += 1
        self.update_ScoreBoard()
