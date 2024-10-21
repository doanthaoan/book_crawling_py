import turtle

# Cấu hình màn hình
win = turtle.Screen()
win.title("Pong by @Python")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# Thanh bên trái
left_paddle = turtle.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color("white")
left_paddle.shapesize(stretch_wid=6, stretch_len=1)
left_paddle.penup()
left_paddle.goto(-350, 0)

# Thanh bên phải
right_paddle = turtle.Turtle()
right_paddle.speed(0)
right_paddle.shape("square")
right_paddle.color("white")
right_paddle.shapesize(stretch_wid=6, stretch_len=1)
right_paddle.penup()
right_paddle.goto(350, 0)

# Bóng
ball = turtle.Turtle()
ball.speed(1)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.15
ball.dy = -0.15

# Điều khiển
def paddle_left_up():
    y = left_paddle.ycor()
    y += 20
    left_paddle.sety(y)

def paddle_left_down():
    y = left_paddle.ycor()
    y -= 20
    left_paddle.sety(y)

def paddle_right_up():
    y = right_paddle.ycor()
    y += 20
    right_paddle.sety(y)

def paddle_right_down():
    y = right_paddle.ycor()
    y -= 20
    right_paddle.sety(y)

# Lắng nghe bàn phím
win.listen()
win.onkeypress(paddle_left_up, "w")
win.onkeypress(paddle_left_down, "s")
win.onkeypress(paddle_right_up, "Up")
win.onkeypress(paddle_right_down, "Down")

# Vòng lặp chính
while True:
    win.update()

    # Di chuyển bóng
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Kiểm tra biên trên/dưới
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Kiểm tra biên trái/phải
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
