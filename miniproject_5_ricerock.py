# Rickrock

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        ship_center = ship_info.get_center()
        if self.thrust:
            canvas.draw_image(self.image,[self.image_center[0] * 3, self.image_center[1] ], 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image,self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
    def update(self):
        # orientation update
        self.angle += self.angle_vel
        
        # position update
        self.pos[0] = (self.pos[0] + self.vel[0]) %  WIDTH 
        self.pos[1] = (self.pos[1] + self.vel[1]) %  HEIGHT 
        
        # velocity update due to constant friction
        self.vel[0] *= (1 - 0.009)
        self.vel[1] *= (1 - 0.009)
        
        # accelaration in the direction of forward vector
        if self.thrust:
            acceleration = angle_to_vector(self.angle)
            self.vel[0] += acceleration[0] * 0.15
            self.vel[1] += acceleration[1] * 0.15
        
        
    # Turning ship clockwise
    def increment_ship_angle(self):
        ship_orient_inc = 0.1
        self.angle_vel +=  ship_orient_inc    
   
    # Turning ship counter clockwise
    def decrement_ship_angle(self):
        ship_orient_inc = 0.1
        self.angle_vel -=  ship_orient_inc
    
    # set the thrust_status and play or rewind the associated sound
    def thrust_status(self, status):
        self.thrust = status
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
    
    # spawns a new missile, give it velocity in the direction of ship tip and its magnitute depending up the ship velocity
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_vel = [self.vel[0] + forward[0] * 7, self.vel[1] + forward[1] * 7]
        tip_ship = [self.pos[0] + (forward[0] * self.radius) ,
                    self.pos[1] + (forward[1] * self.radius)] # need to understand why the position of the missile changes with multiple of forwards vectors
        missile_group.add(Sprite(tip_ship, missile_vel, self.angle, 0,  missile_image, missile_info, missile_sound))
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        self.age += 1
        # animation
        if self.animated:
            center = [ self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]]
            canvas.draw_image(self.image, center, self.image_size, 
                          self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        # updates the orientation
        self.angle += self.angle_vel
        
        # updates the position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH 
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # To check whether age is greater than lifespan of the sprite
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
        
       
            
        
    def collide(self, other_object):
        dist_between_objs = dist(self.pos, other_object.pos)
        if dist_between_objs <= self.radius + other_object.radius:
            return True
        else:
            return False
    
# timer handler that spawns a rock    
def rock_spawner():
    global score 
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_spin = random.random() * .2 - .1
    scaling_fac_1 = 0.9
    scaling_fac_2 = 0.30
    if 10< score < 20:
        scaling_fac_1 *= 2
        scaling_fac_2 *= 2
    elif 20 < score < 30:
        scaling_fac_1 *= 4
        scaling_fac_2 *= 4
    elif 30 < score < 50:
        scaling_fac_1 *= 6
        scaling_fac_2 *= 6
    elif score > 50:
        scaling_fac_1 *= 12
        scaling_fac_2 *= 12
    
    rock_vel = [random.random() * scaling_fac_1 - scaling_fac_2, random.random() * scaling_fac_1 - scaling_fac_2]
    if len(rock_group) < 12 and dist(rock_pos, my_ship.get_position()) > 100:
        rock_group.add(Sprite(rock_pos,rock_vel, 0, rock_spin, asteroid_image, asteroid_info))
        
# key handlers for controling the orientation of spaceship
def keydown(key):
    if key == simplegui.KEY_MAP["right"]:
        my_ship.increment_ship_angle()        
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.decrement_ship_angle()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_status(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP["right"]:
        my_ship.decrement_ship_angle()
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.increment_ship_angle()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_status(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        timer.start()
        soundtrack.play()
        
#helper functions
def process_sprite_group(canvas, a_set):
    for sprite in list(a_set):
        sprite.draw(canvas)
        if sprite.update():
            a_set.remove(sprite)
            
def group_collide(set_group, other_object):
    collision = False
    for sprite in list(set_group):
        if sprite.collide(other_object):
            set_group.remove(sprite)
            collision = True
    return collision

def group_group_collide(set_group, another_set_group):
    num_colliding_elements = 0
    for sprite in list(set_group):
        if group_collide(another_set_group, sprite):
            set_group.remove(sprite)
            num_colliding_elements += 1
            explosion_group.add(Sprite(sprite.pos, [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
    return num_colliding_elements
            
    


# The main draw function that draw things on canvas
def draw(canvas):
    global time, score, lives, started, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text(f"Score: {score}", (WIDTH / 9, HEIGHT / 8), 30, "White")
    canvas.draw_text(f"Lives: {lives}", (WIDTH - WIDTH / 4 , HEIGHT / 8), 30, "White")
    
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
                                
    # update ship and sprites
    my_ship.update()
    
    # collision of ship with rocks
    if group_collide(rock_group, my_ship):
        lives -= 1
        if lives <= 0:
            started = False
            rock_group = set([])
            timer.stop()
            soundtrack.rewind()
            
    # collision of missiles with rocks
    if group_group_collide(rock_group, missile_group):
        score += 1
        
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling

frame.start()

