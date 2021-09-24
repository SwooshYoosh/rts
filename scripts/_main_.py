# Setup Python ------------------------------------------------------------------------------------------------------------------------- Setup Python #
import pygame, sys, entity, math

from pygame import cursors
from enums import EntityType

# Initialize Variables ----------------------------------------------------------------------------------------------------------------- Initialize Variables #
# pygame initializing
mainClock = pygame.time.Clock() # set up clock
from pygame.locals import * # imports pygame's locals (display, event, key, ect.)
pygame.init() # initiate pygame
# screen initializing
pygame.display.set_caption('RTS?!?!') # set game window's name
SCREEN = pygame.display.set_mode((1280, 720)) # initiate the screen
#DISPLAY = pygame.Surface((320, 180)) # initialize the area of what will be shown on screen
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h] # get the width and hight of monitor and save in a list

selected_entities = [] # list of selected entities
target_point = None # used to save the position of mouse when right clicked

mouse_pos_1 = (0, 0)
mouse_pos_2 = (0, 0)


###### SPRITES ############################################
test_person = entity.Entity((50, 500), EntityType.PERSON)
tester_guy = entity.Entity((100, 500), EntityType.PERSON)
all_sprites = pygame.sprite.Group()
all_sprites.add(test_person)
all_sprites.add(tester_guy)
###### SPRITES ##########################################

# Functions ---------------------------------------------------------------------------------------------------------------------------- Functions

def selection_rect(pos1, pos2):
    if pos1[0] > pos2[0]:
        if pos1[1] > pos2[1]:
            return pygame.Rect(pos2, (pos1[0] - pos2[0], pos1[1] - pos2[1])) # top left square 
        else:
            return pygame.Rect((pos2[0], pos1[1]), (pos1[0] - pos2[0], pos2[1] - pos1[1])) # bottom left square 
    else:
        if pos1[1] > pos2[1]:
            return pygame.Rect((pos1[0], pos2[1]), (pos2[0] - pos1[0], pos1[1] - pos2[1])) # top right square
        else:
            return pygame.Rect(pos1, (pos2[0] - pos1[0], pos2[1] - pos1[1])) # bottom right square

def get_positions_list(target_position, distance, selected_entities):
    position_list = []
    amount = len(selected_entities)
    for i in amount:
        angle = i * (360 / amount)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        new_pos = (target_position[0] + x, target_position[1] + y)
        position_list.append(new_pos)
    return position_list

def get_positions_ring(target_position, distances, ring_amount):
    position_list = [target_position]
    for i in ring_amount:
        new_pos = get_positions_list(target_position, distances[i], ring_amount[i])
        position_list.append(new_pos)
    return position_list

# Main Game Loop ----------------------------------------------------------------------------------------------------------------------- Main Game Loop #
while True: 

    # Events ---------------------------------------------------------------------------------------------------------------------------- Events #
    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # quit when X is pressed
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: # if left mouse button is clicked
                mouse_pos_1 = pygame.mouse.get_pos() # get position of mouse
            if event.button == 3: # if right mouse button is clicked
                #for entity in selected_entities: # for every entity selected
                #    entity.move_to_target(pygame.mouse.get_pos()) # call move_to_target() function and set target as mouse position
                    target_point = pygame.mouse.get_pos() # set target_point to the mouse position
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                selected_entities = [] # reset selected_entities list to be empty
                target_point = None
                mouse_pos_2 = pygame.mouse.get_pos() # get position of mouse

                selection = selection_rect(mouse_pos_1, mouse_pos_2) # create select in variable that holds the proper selection coords

                for sprite in all_sprites: # for all sprites
                    if selection.colliderect(sprite.rect): # if sprite is colliding with selection rect
                        selected_entities.append(sprite) # add all selected entities to selected_entities list

    if selected_entities:
        for entity in selected_entities:
            if target_point is not None:
                entity.move_to_target(target_point)

    if target_point is not None:
        target_position_list = get_positions_ring(target_point, [20, 30, 40], [3, 5, 10, 20])

    i = 0
    for entity in selected_entities:
        entity.move_to_target(get_positions_list[i])
        
        i = (i + 1) % len(target_position_list)

    # Drawing ----------------------------------------------------------------------------------------------------------------------------- Drawing #

    SCREEN.fill((0, 0, 0)) # fill screen with black ( so sprites arn't drawn ontop of each other )

    all_sprites.draw(SCREEN) # draw all sprites onto screen

    if pygame.mouse.get_pressed()[0]: # if left mouse button is pressed
       pygame.draw.rect(SCREEN, (0, 255, 0), selection_rect(mouse_pos_1, pygame.mouse.get_pos())) # draw the selection_rect

    # Update Screen ---------------------------------------------------------------------------------------------------------------------- Update Screen #
    #surf = pygame.transform.scale(DISPLAY, WINDOW_SIZE)
    #SCREEN.blit(surf, (0,0))
    pygame.display.update() # update display
    mainClock.tick(60) # maintian 60 fps