from  turtle import Turtle,Screen
import random
screen = Screen()
# screen.bgcolor("black")
screen.setup(500,400)
position = [160,120,80,40,0,-40]
color = ["Green", "Red", "Yellow", "black","purple","blue"]
all_turtle =[]
for turtle_index in range(0,6):
    tim = Turtle(shape="turtle")
    tim.penup()
    tim.color(color[turtle_index])
    tim.setposition(-240,position[turtle_index])
    all_turtle.append(tim)


user_bet = screen.textinput(title="Make your bet", prompt="Which turtle wins the game pick a colour : ")
print(user_bet)

race_is_on = False
if user_bet:
    race_is_on = True
winner = ""
while race_is_on:
    for tim in all_turtle:
        speed = random.randint(0,10)
        tim.forward(speed)
        if tim.xcor() > 230:
            winner = tim.pencolor()
            race_is_on = False
            break
if winner.lower() == user_bet.lower():
    print(f"your bet {user_bet} wins the game")
else:
    print(f"your bet {user_bet} loses the game")
    print(f"the winner is {winner}")


screen.clear()


#
# def move_forward():
#     tim.forward(10)
#
# def move_right():
#     tim.right(10)
# def move_left():
#     tim.left(10)
#
# def move_backward():
#     tim.backward(10)
#
# def clear_screen():
#     tim.home()
#     tim.clear()
#
# screen.listen()
# screen.onkey(key="w", fun=move_forward)
# screen.onkey(key="s", fun=move_backward)
# screen.onkey(key="d", fun=move_right)
# screen.onkey(key="a", fun=move_left)
# screen.onkey(key="c", fun=clear_screen)
screen.exitonclick()
