import pygame
from pygame.locals import *
import random, sys, asyncio, math

pygame.init()

async def main():

    FPS = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    font2 = pygame.font.SysFont(None, 80)
    font3 = pygame.font.SysFont(None, 50)

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    backcolour = (255, 255, 200)
    darkgray = (90, 90, 90)
    grey = (128, 128, 128)
    darkgreen = (1, 50, 32)
    blue = (0, 0, 255)

    run = False
    background = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Square Killer")

    score = 0
    hscore = 0
    enemycount = 180


    class You(pygame.sprite.Sprite):
        def __init__(self, x, y):
            self.radius = 19.5
            self.angle = 0
            self.x = x
            self.y = y
        
        def checkcolx(self, walls):
            playerrectx =  pygame.Rect(self.x - self.radius, self.y - 15, self.radius * 2, 15 * 2)
            if any(playerrectx.colliderect(wall.getrect()) for wall in walls):
                return True
            else:
                return False
        def checkcoly(self, walls):
            playerrecty =  pygame.Rect(self.x - 15, self.y - self.radius, 15 * 2, self.radius * 2)
            if any(playerrecty.colliderect(wall.getrect()) for wall in walls):
                return True
            else:
                return False
        

        def moveForward(self, pixels, walls):
            old_x = self.x
            old_y = self.y
            if 0 <= self.angle < 90:
                self.x += pixels * math.cos(self.angle)
                self.y -= pixels * math.sin(self.angle)

            if self.checkcolx(walls):
                self.x = old_x
            if self.checkcoly(walls):
                self.y = old_y   
                

        def getrect(self):
            return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)        


        def moveBackward(self, pixels, walls):    
            old_x = self.x
            old_y = self.y

            if 0 <= self.angle < 90:
                self.x -= pixels * math.cos(self.angle)
                self.y += pixels * math.sin(self.angle)
            
            if self.checkcolx(walls):
                self.x = old_x
                playerrectx =  pygame.Rect(self.x - 15, self.y - 15, self.radius * 2, 15 * 2)
                if any(playerrectx.colliderect(wall.getrect()) for wall in walls):
                    self.y = old_y
            if self.checkcoly(walls):
                self.y = old_y
                playerrectx =  pygame.Rect(self.x - 15, self.y - 15, self.radius * 2, 15 * 2)
                if any(playerrectx.colliderect(wall.getrect()) for wall in walls):
                    self.x = old_x
        
        def turnRight(self):
            self.angle -= 0.1
            if self.angle >= 6.3:
                self.angle = 0
            if self.angle < 0:
                self.angle = 6.2
        def turnLeft(self):
            self.angle += 0.1
            if self.angle >= 6.3:
                self.angle = 0
            if self.angle < 0:
                self.angle = 6.2


        def draw(self):
            pygame.draw.circle(background, green, (self.x, self.y), self.radius)
            if 0 <= self.angle < 90:
                x = 15 * math.cos(self.angle)
                y = 15 * math.sin(self.angle)
            pygame.draw.circle(background, grey, (self.x + x, self.y - y), 4.5)
            if 0 <= self.angle < 90:
                x = 10 * math.cos(self.angle - 1)
                y = 10 * math.sin(self.angle - 1)
            pygame.draw.circle(background, white, (self.x + x, self.y - y), 8.5)
            if 0 <= self.angle < 90:
                x = 10 * math.cos(self.angle + 1)
                y = 10 * math.sin(self.angle + 1)
            pygame.draw.circle(background, white, (self.x + x, self.y - y), 8.5)
            if 0 <= self.angle < 90:
                x = 10 * math.cos(self.angle + 1)
                y = 10 * math.sin(self.angle + 1)
            pygame.draw.circle(background, black, (self.x + x, self.y - y), 4)
            if 0 <= self.angle < 90:
                x = 10 * math.cos(self.angle - 1)
                y = 10 * math.sin(self.angle - 1)
            pygame.draw.circle(background, black, (self.x + x, self.y - y), 4)


        
    
    class Wall(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

        def getrect(self):
            return pygame.Rect(self.x, self.y, self.width, self.height)

        def draw(self):
            pygame.draw.rect(background, darkgray, (self.x, self.y, self.width, self.height))

    
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.angle = angle
            self.radius = 7
        

        def checkcolx(self, walls):
            playerrectx =  pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, 14)
            return any(playerrectx.colliderect(wall.getrect()) for wall in walls)
        def checkcoly(self, walls):
            playerrecty =  pygame.Rect(self.x - self.radius, self.y - self.radius, 14, self.radius * 2)
            return any(playerrecty.colliderect(wall.getrect()) for wall in walls)
        def getrect(self):
            return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius *2)
        

        def move(self, pixels, walls):
            if 0 <= self.angle < 6.4:
                self.x += pixels * math.cos(self.angle)
                self.y -= pixels * math.sin(self.angle)
            
            if self.checkcolx(walls):
                return True
            if self.checkcoly(walls):
                return True
            return False
        


        def draw(self):
            pygame.draw.circle(background, red, (self.x, self.y), self.radius)


    class Ring(pygame.sprite.Sprite):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.radius = 2

        def move(self):
            self.radius += 2
            if self.radius == 60:
                return True
            return False
        
        def draw(self, x, y):
            pygame.draw.circle(background, darkgreen, (x, y), self.radius, 5)

        def getrect(self):
            return pygame.Rect(self.x - (self.radius/2), self.y - self.radius, self.radius, self.radius * 2)

        def getrect2(self):
            return pygame.Rect(self.x - self.radius, self.y - (self.radius/2), self.radius * 2, self.radius)


    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.width = 30
            self.height = 30
            self.angle = angle

        def draw(self):
            pygame.draw.rect(background, black, (self.x, self.y, self.width, self.height))
            if 0 <= self.angle < 90:
                x = 8 * math.cos(self.angle - 1)
                y = 8 * math.sin(self.angle - 1)
            pygame.draw.circle(background, white, (self.x + 15 + x, self.y  + 15 - y), 5)
            if 0 <= self.angle < 90:
                x = 8 * math.cos(self.angle + 1)
                y = 8 * math.sin(self.angle + 1)
            pygame.draw.circle(background, white, (self.x + 15 + x, self.y  + 15 - y), 5)
            if 0 <= self.angle < 90:
                x = 8 * math.cos(self.angle - 1)
                y = 8 * math.sin(self.angle - 1)
            pygame.draw.circle(background, black, (self.x + 15 + x, self.y  + 15 - y), 2)
            if 0 <= self.angle < 90:
                x = 8 * math.cos(self.angle + 1)
                y = 8 * math.sin(self.angle + 1)
            pygame.draw.circle(background, black, (self.x + 15 + x, self.y  + 15 - y), 2)

        def checkcol(self, walls):
            playerrectx =  pygame.Rect(self.x, self.y ,30, 30)
            return any(playerrectx.colliderect(bullet.getrect()) for wall in walls)

        def hit(self, bul):
            if self.checkcol(bul):
                return True

            return False
        
    class Enebul(pygame.sprite.Sprite):
        def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.angle = angle
            self.radius = 5

        def checkcol(self, walls):
            playerrectx =  pygame.Rect(self.x +15 - self.radius, self.y + 15 - self.radius, self.radius * 2, 10)
            return any(playerrectx.colliderect(wall.getrect()) for wall in walls)
        def checkcol2(self, walls):
            playerrectx =  pygame.Rect(self.x + 15 - self.radius, self.y + 15  - self.radius, self.radius * 2, 10)
            return any(playerrectx.colliderect(wall.getrect2()) for wall in walls)
        def checkcolp(self, walls):
            playerrectx =  pygame.Rect(self.x + 15 - self.radius, self.y + 15 - self.radius, self.radius * 2, 10)
            return playerrectx.colliderect(walls.getrect())
        def getrect(self):
            return pygame.Rect(self.x + 15 - self.radius, self.y + 15- self.radius, self.radius * 2, self.radius *  2)
            

        def draw(self):
            pygame.draw.circle(background, red, (self.x + 15, self.y + 15), 5)

        def move(self, pixels, walls):
            if 0 <= self.angle < 90:
                self.x += pixels * math.cos(self.angle)
                self.y -= pixels * math.sin(self.angle)

        def hit(self, bul):
            if self.checkcol(bul):
                return True

            return False
        
        def hit2(self, bul):
            if self.checkcol2(bul):
                return True

            return False
        
        def hitp(self, bul):
            if self.checkcolp(bul):
                return True

            return False
        

    class Button(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height, bord, colour, radius):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.colour = colour
            self.bord = bord
            self.radius = radius

        def draw(self):
            pygame.draw.rect(background, self.colour, (self.x, self.y, self.width, self.height), self.bord, self.radius)
        




    border1 = [Wall(0, 0, 1000, 30), Wall(970, 0, 30, 700), Wall(0, 670, 1000, 30), Wall(0, 30, 30, 700), Wall(300, 0, 30, 200), Wall(800, 90, 30, 1000), Wall(500, 90, 300, 30), Wall(200, 250, 500, 30), Wall(200, 250, 30, 300), Wall(0, 550, 230, 30), Wall(150, 170, 150, 30), Wall(670, 250, 30, 320), Wall(300, 570, 400, 30), Wall(300, 350, 30, 250), Wall(300, 350, 300, 30), Wall(570, 350, 30, 150), Wall(0, 300, 120, 30), Wall(100, 450, 100, 30)]
    border2 = [Wall(0, 0, 1000, 30), Wall(970, 0, 30, 700), Wall(0, 670, 1000, 30), Wall(0, 30, 30, 700), Wall(450, 300, 30, 300), Wall(450, 300, 1000, 30), Wall(550, 400, 30, 300), Wall(550, 400, 300, 30), Wall(650, 500, 400, 30), Wall(300, 200, 30, 1000), Wall(800, 200, 200, 100), Wall(650, 100, 30, 200), Wall(400, 200, 250, 30), Wall(0, 300, 225, 30), Wall(195, 300, 30, 100), Wall(90, 380, 30, 100), Wall(90, 480, 230, 30), Wall(200, 0, 30, 200)]
    border3 = [Wall(0, 0, 1000, 30), Wall(970, 0, 30, 700), Wall(0, 670, 1000, 30), Wall(0, 30, 30, 700), Wall(485, 100, 30, 500), Wall(150, 335, 850, 30), Wall(500, 465, 50, 30), Wall(500, 205, 50, 30), Wall(620, 205, 200, 30), Wall(620, 465, 200, 30), Wall(890, 205, 200, 30), Wall(890, 465, 200, 30), Wall(720, 205, 30, 260), Wall(150, 100, 30, 500), Wall(250, 465, 250, 30), Wall(250, 205, 250, 30), Wall(350, 0, 30, 150), Wall(350, 550, 30, 150)]



    b = random.randint(1,3)
    if b == 1:
        border = border1
        enemies = [Enemy(200, 100, 3.2), Enemy(700, 200, 3.2), Enemy(500, 500, 6.4), Enemy(400, 400, 6.4), Enemy(900, 600, 4.8), Enemy(150, 500, 3.2)]
    elif b == 2:
        border = border2
        enemies = [Enemy(400, 100, 3.2), Enemy(700, 200, 1.6), Enemy(900, 600, 3.2), Enemy(500, 500, 4.8), Enemy(50, 50, 4.8), Enemy(600, 250, 3.2)]
    elif b == 3:
        border = border3
        enemies = [Enemy(400, 100, 4.8), Enemy(920, 260, 3.2), Enemy(400, 570, 1.6), Enemy(920, 410, 3.2), Enemy(670, 410, 3.2), Enemy(670, 260, 3.2), Enemy(400, 260, 3.2), Enemy(900, 600, 3.2)]


    round = 0
    playerbullets = []
    enemybullets = []
    playerring = []
    boxes = [Button(250, 100, 500, 100, 0, green, 10), Button(250, 100, 500, 100, 10, darkgreen, 10), Button(80, 300, 500, 300, 0, green, 15), Button(80, 300, 500, 300, 10, darkgreen, 15)]
    but = [Button(700, 500, 275, 80, 0, green, 10), Button(700, 500, 275, 80, 5, darkgreen, 10)]
    countdown = 0
    countdown2 = 0
    speed = 3
    if b == 1:
        h = 70
        j = 630
    elif b == 2:
        h = 270
        j = 630
    elif b == 3:
        h = 70
        j = 350
    P1 = You(h, j)
    ant = True
    run2 = True
    run3 = False
    while ant == True:
        round = 0
        countdown = 0
        countdown2 = 0
        while run2 == True:
            if score > hscore:
                hscore = score
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ant = False
                    run2 = False

            mouse = pygame.mouse.get_pressed()

            background.fill(backcolour)


            for box in boxes:
                box.draw()
            for button in but:
                button.draw()
            st_text = font2.render("Square Killer", True, black)
            background.blit(st_text, (320, 115))
            srt_text = font.render(">CLICK TO START!<", True, black)
            background.blit(srt_text, (720, 520))
            inst_text = font3.render("How To Play", True, black)
            background.blit(inst_text, (220, 320))
            line1 = font.render("W/Up Arrow  --  Move Forward", True, black)
            line2 = font.render("S/Down Arrow  --  Move Backward", True, black)
            line3 = font.render("A/Left Arrow  --  Turn Left", True, black)
            line4 = font.render("D/Right Arrow  --  Turn Right", True, black)
            line5 = font.render("B  --  Shoot", True, black)
            line6 = font.render("N  --  Aura Shield", True, black)
            line7 = font.render("P  --  Exit Game", True, black)
            background.blit(line1, (100, 370))
            background.blit(line2, (100, 400))
            background.blit(line3, (100, 430))
            background.blit(line4, (100, 460))
            background.blit(line5, (100, 490))
            background.blit(line6, (100, 520))
            background.blit(line7, (100, 550))
            hscore_text = font.render(f"High Score: {hscore}", True, black)
            background.blit(hscore_text, (5, 5))
            
            mousex, mousey = pygame.mouse.get_pos()
            
            if 700 < mousex < 975:
                if 500 < mousey < 580:
                    if mouse[0]:
                        run2 = False
                        run = True
            
            
            pygame.display.update()
            FPS.tick(60)
            await asyncio.sleep(0)



        b = random.randint(1,3)
        if b == 1:
            border = border1
            enemies = [Enemy(200, 100, 3.2), Enemy(700, 200, 3.2), Enemy(500, 500, 6.4), Enemy(400, 400, 6.4), Enemy(900, 600, 4.8), Enemy(150, 500, 3.2)]
        elif b == 2:
            border = border2
            enemies = [Enemy(400, 100, 3.2), Enemy(700, 200, 1.6), Enemy(900, 600, 3.2), Enemy(500, 500, 4.8), Enemy(50, 50, 4.8), Enemy(600, 250, 3.2)]
        elif b == 3:
            border = border3
            enemies = [Enemy(400, 100, 4.8), Enemy(920, 260, 3.2), Enemy(400, 570, 1.6), Enemy(920, 410, 3.2), Enemy(670, 410, 3.2), Enemy(670, 260, 3.2), Enemy(400, 260, 3.2), Enemy(900, 600, 3.2)]


        round = 0
        playerbullets = []
        enemybullets = []
        playerring = []
        boxes = []
        but = []
        boxes = [Button(250, 100, 500, 100, 0, green, 10), Button(250, 100, 500, 100, 10, darkgreen, 10), Button(80, 300, 500, 300, 0, green, 15), Button(80, 300, 500, 300, 10, darkgreen, 15)]
        but = [Button(700, 500, 275, 80, 0, green, 10), Button(700, 500, 275, 80, 5, darkgreen, 10)]
        countdown = 0
        countdown2 = 0
        speed = 3
        score = 0
        if b == 1:
            h = 70
            j = 630
        elif b == 2:
            h = 270
            j = 630
        elif b == 3:
            h = 70
            j = 350
        P1 = You(h, j)
        while run == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    ant = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        run = False
                        run2 = True
            

            background.fill(backcolour)


            keys = pygame.key.get_pressed()

            
            
            if keys[pygame.K_LEFT]:
                if keys[pygame.K_a]:
                    P1.turnLeft()
                else:
                    P1.turnLeft()
                
            if keys[pygame.K_RIGHT]:
                if keys[pygame.K_d]:
                    P1.turnRight()
                else:
                    P1.turnRight()
            if keys[pygame.K_UP]:
                if keys[pygame.K_w]:
                    P1.moveForward(speed, border)
                else:
                    P1.moveForward(speed, border)
            if keys[pygame.K_DOWN]:
                if keys[pygame.K_s]:
                    P1.moveBackward(speed, border)
                else:
                    P1.moveBackward(speed, border)
            
            if keys[pygame.K_d]:
                if keys[pygame.K_RIGHT]:
                    donothing = 1
                else:
                    P1.turnRight()
            if keys[pygame.K_a]:
                if keys[pygame.K_LEFT]:
                    donothing = 1
                else:
                    P1.turnLeft()
            if keys[pygame.K_w]:
                if keys[pygame.K_UP]:
                    donothing = 1
                else:
                    P1.moveForward(speed, border)
            if keys[pygame.K_s]:
                if keys[pygame.K_DOWN]:
                    donothing = 1
                else:
                    P1.moveBackward(speed, border)

            if keys[pygame.K_b]:
                if countdown <= 0:
                    playerbullets.append(Bullet(P1.x, P1.y, P1.angle))
                    countdown = 30
            
            if keys[pygame.K_n]:
                if countdown2 <= 0:
                    playerring.append(Ring(P1.x, P1.y))
                    countdown2 = 40
                


            for bullet in playerbullets:
                if bullet.move(4, border):
                    playerbullets.remove(bullet)
                bullet.draw()
                
            countdown -= 1
            enemycount -= 1
            countdown2 -= 1

            for ring in playerring:
                if ring.move():
                    playerring.remove(ring)
                ring.draw(P1.x, P1.y)

            for enemy in enemies:
                if enemy.hit(playerbullets):
                    enemies.remove(enemy)
                    score += 1
                enemy.draw()
                
            a = 90
            if enemycount < 0:
                for enemy in enemies:
                    a = 6.4
                    while a > 0:
                        enemybullets.append(Enebul(enemy.x, enemy.y, a))
                        a -= 0.4
                enemycount = 300
            

            for enebil in enemybullets:
                if enebil.hit(border):
                    enemybullets.remove(enebil)
                enebil.move(4, border)
                enebil.draw()

            for enebil in enemybullets:
                for bullet in playerbullets:
                    if enebil.hit(playerbullets):
                        enemybullets.remove(enebil)
                for ring in playerring:
                    if enebil.hit(playerring):
                        enemybullets.remove(enebil)
                    if enebil.hit2(playerring):
                        enemybullets.remove(enebil)
            
            
            for wall in border:
                wall.draw()
        
        
        
            for enebil in enemybullets:
                if enebil.hitp(P1):
                    run = False
                    run2 = True
                    lose_text = font2.render("You Lose!", True, blue)
                    background.blit(lose_text, (350, 300))


        
            P1.draw()
            if len(enemies) == 0:
                if border == border1:
                    border = border2
                    enemies = [Enemy(400, 100, 3.2), Enemy(700, 200, 1.6), Enemy(900, 600, 3.2), Enemy(500, 500, 4.8), Enemy(50, 50, 4.8), Enemy(600, 250, 3.2)]
                    P1.x = 270 
                    P1.y = 630
                    round += 1
                    if round < 3:
                        playerbullets = []
                        pygame.display.update()
                        next_text = font2.render("You Beat The Level!", True, black)
                        background.blit(next_text, (220, 300))
                        pygame.display.update()
                        pygame.time.delay(3000)

                elif border == border2:
                    border = border3
                    enemies = [Enemy(400, 100, 4.8), Enemy(920, 260, 3.2), Enemy(400, 570, 1.6), Enemy(920, 410, 3.2), Enemy(670, 410, 3.2), Enemy(670, 260, 3.2), Enemy(400, 260, 3.2), Enemy(900, 600, 3.2)]
                    P1.x = 70
                    P1.y = 350
                    round += 1
                    if round < 3:
                        playerbullets = []
                        pygame.display.update()
                        next_text = font2.render("You Beat The Level!", True, black)
                        background.blit(next_text, (220, 300))
                        pygame.display.update()
                        pygame.time.delay(3000)


                elif border == border3:
                    border = border1
                    enemies = [Enemy(200, 100, 3.2), Enemy(700, 200, 3.2), Enemy(500, 500, 6.4), Enemy(400, 400, 6.4), Enemy(900, 600, 4.8), Enemy(150, 500, 3.2)]
                    P1.x = 70
                    P1.y = 630
                    round += 1
                    if round < 3:
                        playerbullets = []
                        pygame.display.update()
                        next_text = font2.render("You Beat The Level!", True, black)
                        background.blit(next_text, (220, 300))
                        pygame.display.update()
                        pygame.time.delay(3000)
                
            if round == 3:
                pygame.display.update()
                finish_text = font2.render("You Win!", True, black)
                background.blit(finish_text, (300, 300))
                run = False
                run2 = True
            


            score_text = font.render(f"Score: {score} ", True, black)
            background.blit(score_text, (5, 5))


            
            pygame.display.update()
            FPS.tick(60)
            await asyncio.sleep(0)
        

        
        enemies = []
        enemybullets = []
        playerbullets = []
        playerring = []
        P1 = 0
        pygame.time.delay(3000)
        await asyncio.sleep(0)
asyncio.run(main())



