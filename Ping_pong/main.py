from turtle import Screen, Turtle
from paddle import paddle
from Pong_Ball import ball
import time
from ScoreBoard import scoreboard

# TODO: Create a Screen for our game
screen = Screen()
screen.setup(800,600)
screen.bgcolor("black")
screen.title("Ping Pong Game")
screen.tracer(0)


# TODO: Display the score
scoreboard1 = scoreboard()
# TODO: Create a bar
bar1 = paddle(1)
bar2 = paddle(2)
pong = ball()
screen.listen()

screen.onkey(bar1.go_up,"w")
screen.onkey(bar1.go_down,"s")

screen.onkey(bar2.go_up,"Up")
screen.onkey(bar2.go_down,"Down")
# screen.onkey(pong.start,"space")

game_is_ready = True
# TODO: this should run the game
while game_is_ready:
    time.sleep(pong.ballspeed)
    screen.update()
    pong.start()
    #  TODO: Detect the collision with the wall
    if pong.ycor() > 280 or pong.ycor() < -280:
        pong.bounce_y()
    #     TODO: Detect the collision with the wall behind the R_paddle
    if pong.xcor() > 380:
        time.sleep(1)
        pong.ball_reset()
        scoreboard1.r_score()

    #     TODO: Detect the collision with the L_paddle
    if pong.xcor() < -380:
        time.sleep(1)
        pong.ball_reset()
        scoreboard1.l_score()

#     TODO: Detect the collision with the paddle
    if pong.distance(bar2) < 50 and pong.xcor() > 320 or pong.distance(bar1) < 50 and pong.xcor() < -320:
        pong.bounce_x()





screen.exitonclick()
