import turtle  
skk = turtle.Turtle()
 
skk.color("blue","red")
skk.begin_fill()
for i in range(4): 
    skk.forward(50) 
    skk.right(90) 

skk.end_fill()
# # Hinh hop      
# skk.left(120)
# skk.forward(50)
# skk.right(120)
# skk.forward(50)
# skk.right(60)
# skk.forward(50)
# skk.right(60)

skk.left(120)
skk.penup()
skk.forward(250)
skk.pendown()
skk.right(60)
skk.forward(50)
skk.right(120)
skk.forward(50)
skk.right(120)
skk.forward(50)
skk.fillcolor("red")
turtle.done() 