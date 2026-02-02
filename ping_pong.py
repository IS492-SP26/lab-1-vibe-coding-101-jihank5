import time
import turtle


def setup_screen():
    # Configure the game window.
    screen = turtle.Screen()
    screen.title("Ping-Pong")
    screen.bgcolor("black")
    screen.setup(width=800, height=600)
    screen.tracer(0)
    return screen


def create_paddle(x_pos):
    # Create a paddle at the given x position.
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    paddle.penup()
    paddle.goto(x_pos, 0)
    return paddle


def create_ball():
    # Create the ball with initial velocity.
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 0.75
    ball.dy = 0.75
    return ball


def create_scoreboard():
    # Create a turtle used to display the score.
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    return pen


def move_paddle(paddle, dy):
    # Move a paddle up/down while keeping it on-screen.
    y = paddle.ycor() + dy
    if y > 250:
        y = 250
    if y < -250:
        y = -250
    paddle.sety(y)


def update_scoreboard(pen, left_score, right_score):
    # Redraw the score text.
    pen.clear()
    pen.write(
        f"Left Player: {left_score}    Right Player: {right_score}",
        align="center",
        font=("Courier", 18, "normal"),
    )


def main():
    screen = setup_screen()

    left_paddle = create_paddle(-350)
    right_paddle = create_paddle(350)
    ball = create_ball()
    pen = create_scoreboard()

    left_score = 0
    right_score = 0
    update_scoreboard(pen, left_score, right_score)

    # Key bindings for paddle controls.
    screen.listen()
    screen.onkeypress(lambda: move_paddle(left_paddle, 20), "w")
    screen.onkeypress(lambda: move_paddle(left_paddle, -20), "s")
    screen.onkeypress(lambda: move_paddle(right_paddle, 20), "Up")
    screen.onkeypress(lambda: move_paddle(right_paddle, -20), "Down")

    # Main game loop.
    while True:
        screen.update()
        time.sleep(0.003)

        # Move the ball.
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Bounce off top and bottom walls.
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1

        # Score updates when the ball goes past a paddle.
        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            left_score += 1
            update_scoreboard(pen, left_score, right_score)
        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            right_score += 1
            update_scoreboard(pen, left_score, right_score)

        # Bounce off paddles.
        if (
            340 < ball.xcor() < 350
            and right_paddle.ycor() - 50 < ball.ycor() < right_paddle.ycor() + 50
        ):
            ball.setx(340)
            ball.dx *= -1
        if (
            -350 < ball.xcor() < -340
            and left_paddle.ycor() - 50 < ball.ycor() < left_paddle.ycor() + 50
        ):
            ball.setx(-340)
            ball.dx *= -1


if __name__ == "__main__":
    main()
