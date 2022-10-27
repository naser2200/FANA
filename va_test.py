
import pygame
import pymunk
import random
  
pygame.init()

display = pygame.display.set_mode((800,800))
clock =pygame.time.Clock()
space = pymunk.Space()
FPS = 90

population = 300



class Ball():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = random.uniform(-100,100) , random.uniform(-100,100)
        self.shape = pymunk.Circle(self.body,10)
        self.shape.density = 1
        self.shape.elasticity =1
        self.infected = False
        space.add(self.body,self.shape)

    def draw(self):
        x,y = self.body.position
        if self.infected:
            pygame.draw.circle(display,(255,0,0),(int(x),int(y)),10)
        else:
            pygame.draw.circle(display,(255,255,255),(int(x),int(y)),10)
    
    def infect(self,space=0,arbiter=0,data=0):
        self.infected = True
        self.shape.collision_type = population+1
    
class Wall():
    def __init__(self,p1,p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body,p1,p2,5)
        self.shape.elasticity =1
        space.add(self.body,self.shape)

def game():
    balls = [Ball(random.randint(0,800),random.randint(0,800)) for i in range(population)]
    for i in range(1,population+1):
        balls[i-1].shape.collision_type = i
        handler = space.add_collision_handler(i,population+1)
        handler.separate = balls[i-1].infect
    random.choice(balls).infect()
    walls = [Wall((0,0),(0,800)),
             Wall((0,0),(800,0)),
             Wall((0,800),(800,800)),
             Wall((800,0),(800,800))]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        display.fill((0,0,0))
        # pygame.draw.rect(display, (100,100,100), [590, 315, 80 , 30])
        # smallText = pygame.font.Font("freesansbold.ttf",20)
        # msg = smallText.render('quit',True,(0,200,0))
        # display.blit(msg, (600,320))
        for ball in balls:
            ball.draw()
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

def main():
    game()
    pygame.quit()

if __name__ == "__main__":
    main()
