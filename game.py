import turtle as t
import winsound
import os
import random

from PIL import Image

# t.register_shape("./enemy1.gif")
t.register_shape("./player.gif")


class Screen:
    def __init__(self, caption, bg_path, bg_color, w, h):
        self.sc = t.Screen()

        self.sc.bgcolor(bg_color)
        self.sc.title(caption)
        self.sc.bgpic(bg_path)

        self.score = -1

        self.sc.setup(1.0, 1.0)

        self.score_pen = t.Turtle()
        self.uptate_score()

    def uptate_score(self):
        self.score_pen.clear()
        self.score += 1
        self.score_pen.speed(0)
        self.score_pen.color("white")
        self.score_pen.penup()
        self.score_pen.setposition(-290, 280)
        self.score_pen.write(f"Score: {self.score}", False, align="left", font=("Arial", 14, "normal"))
        self.score_pen.hideturtle()


class Enemy(t.Turtle):
    def __init__(self, img_path, speed, w, h, size):
        t.Turtle.__init__(self)

        self.shape(img_path)
        self.speed(0)
        self.penup()
        x = random.randint(-200, 200)
        y = random.randint(100, 250)

        self.setposition(x, y)

        self.sp = speed * random.choice([-1, 1])

        self.w, self.h = w, h

        self.size = size

    def move(self):
        dx = self.xcor() + self.sp
        if dx > self.w // 2:
            self.setx(self.w // 2)
            self.sp *= -1

            self.sety(self.ycor() - 40)
        else:
            self.setx(dx)

        if dx < -self.w // 2:
            self.setx(-self.w // 2)
            self.sp *= -1

            self.sety(self.ycor() - 40)
        else:
            self.setx(dx)


class Bullet(t.Turtle):
    def __init__(self, color):
        t.Turtle.__init__(self)

        self.hideturtle()
        self.shape("triangle")
        self.color(color)
        self.setheading(90)
        self.penup()
        self.speed(0)
        self.shapesize(0.5, 0.5)

        self.state = "ready"

        self.setposition(0, -250)


class Player(t.Turtle):
    def __init__(self, img_path, speed, num_bullet):
        t.Turtle.__init__(self)

        self.shape(img_path)
        self.speed(0)
        self.setposition(0, -250)
        self.setheading(90)

        self.sp = speed

        self.bullets = [Bullet("yellow") for _ in range(num_bullet)]

    def move_left(self):
        x = self.xcor()
        x -= self.sp
        if x < -280:
            x = -280
        self.setx(x)

    def move_right(self):
        print(1)
        x = self.xcor()
        x += self.sp
        if x > 280:
            x = 280
        self.setx(x)

    def move_up(self):
        y = self.ycor()
        y += self.sp
        if y > 280:
            y = 280
        self.sety(y)

    def move_down(self):
        y = self.ycor()
        y -= self.sp
        if y < -280:
            y = -280
        self.sety(y)

    def fire(self):
        for bullet in self.bullets:
            if bullet.state == "ready":
                bullet.state = "fire"
                x = self.xcor()
                y = self.ycor() + 10
                bullet.setposition(x, y)
                bullet.showturtle()
                break

    def update_bullet(self):
        for bullet in self.bullets:
            if bullet.state == "fire":
                y = bullet.ycor()
                y += self.sp
                bullet.sety(y)

            if bullet.ycor() > 275:
                bullet.hideturtle()
                bullet.state = "ready"

    def isCollision_enemy_bullet(self, enemy):
        # for bullet in self.bullets:
        #     if bullet.distance(enemy) < enemy.size[1]:
        #         bullet.hideturtle()
        #         bullet.state = "ready"
        #         bullet.setposition(0, -400)
        #     return True

        return False

    def isCollision_enemy_player(self, enemy):
        if self.distance(enemy) < enemy.size[1]:
            return True
        else:
            return False


width = 500
height = 500

screen = Screen("Chien binh khong gian", "./background.gif", "white", width + 20, height + 20)

player = Player("./player.gif", 100, 20)
enemies = []

list_enemy_path = [f"./enemies/{x}" for x in os.listdir("./enemies")]

for x in list_enemy_path:
    t.register_shape(x)

list_speeds = [10, 15, 20, 25, 30, 35, 40, 45, 50]

for i in range(10):
    path = random.choice(list_enemy_path)
    speed = random.choice(list_speeds)

    img = Image.open(path)

    enemy = Enemy(path, speed, width, height, img.size)
    enemies.append(enemy)

    print(img.size)

t.listen()
t.onkey(player.move_left, "Left")
t.onkey(player.move_right, "Right")
t.onkey(player.move_up, "Up")
t.onkey(player.move_down, "Down")
t.onkey(player.fire, "space")

isLoss = False

while not isLoss:

    for enemy in enemies:
        enemy.move()

        for bullet in player.bullets:
            if bullet.distance(enemy) < enemy.size[1]:
                winsound.PlaySound("./explosion-e+b.wav", winsound.SND_ASYNC)
                x = random.randint(-200, 200)
                y = random.randint(100, 250)
                enemy.setposition(x, y)
                screen.uptate_score()

        if player.isCollision_enemy_player(enemy):
            winsound.PlaySound("explosion-e+p.wav", winsound.SND_ASYNC)
            player.hideturtle()

            for e in enemies:
                e.hideturtle()
            screen.sc.bgpic("end.gif")
            isLoss = True

    player.update_bullet()

    t.update()
