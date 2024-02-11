import turtle
import turtle as t
import pandas

screen = t.Screen()
screen.title("U.S. State")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
guessed_states = []
data = pandas.read_csv("50_states.csv")
states_name = data.state.to_list()
while len(guessed_states)<50:
    user_answer = screen.textinput(title=f"Guess the state {len(guessed_states)}/50",prompt="Whats the another state name?")

    if user_answer == "exit":
        missing_states = []
        for state in states_name:
            if state.lower() not in guessed_states:
                missing_states.append(state)
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("missing_states.csv")
        break
    if user_answer.lower() in [state.lower() for state in states_name]:
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state.str.lower() == user_answer.lower()]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(state_data.state.item())
        guessed_states.append(user_answer.lower())

turtle.mainloop()