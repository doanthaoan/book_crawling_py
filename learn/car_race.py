import turtle
import random

def car_race():
    screen = turtle.Screen()
    screen.title("Car Racing")
    
    car1 = turtle.Turtle()
    car2 = turtle.Turtle()
    
    car1.shape("turtle")
    car1.color("red")
    car1.penup()
    car1.goto(-100, 50)
    
    car2.shape("turtle")
    car2.color("blue")
    car2.penup()
    car2.goto(-100, -50)

    for i in range(100):
        car1.forward(random.randint(1, 5))
        car2.forward(random.randint(1, 5))

    turtle.done()

car_race()
