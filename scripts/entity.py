# Setup Python ------------------------------------------------------------------------------------------------------------------------- Setup Python #
import pygame, math
from enums import EntityType

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, entity_type):
        super().__init__()
        if entity_type==EntityType.PERSON: # if entity's type is human
            self.image = pygame.image.load('textures/person_basic/person_basic_0.png').convert_alpha() # import image
            self.image = pygame.transform.scale(self.image, (32, 48)) # scale image
            self.image_clean = self.image # for rotation later
            self.rect = self.image.get_rect() # initialize rect
            self.pos = pos
            self.rect.center = pos
            self.speed = 2

    def move_to_target(self, target):

        if self.distance(target) > 1:
            angle = math.atan2((self.pos[1] - target[1]) , (target[0] - self.pos[0]))  # calculate angle

            change_in_posx = self.speed * math.cos(angle) # calculate change in x
            change_in_posy = self.speed * math.sin(angle) # calculate change in y

            (x,y) = self.pos # separate position into x and y variables for simplification
            self.pos = (x + change_in_posx, y - change_in_posy) # set position to current position plus the change in x and y
            self.rect.center = self.pos # update where rect is drawn and collider

    def distance(self, target):
        return math.sqrt(math.pow((target[0]-self.pos[0]), 2) + math.pow((target[1]-self.pos[1]), 2))

