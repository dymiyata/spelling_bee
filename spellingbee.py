# A clone of the New York Times Spelling Bee Game

import pygame
import math
import random

# Get a list of all words from the file 'EnglishWords.txt'
with open('EnglishWords.txt') as file:
    all_words = []
    pangrams = []
    for line in file:
        word = line.rstrip()
        all_words.append(word)
        if len(set(list(word))) == 7:
            pangrams.append(word)


# Get a list of all valid answers given the list of letters
def get_words(letters, special_letter):
    word_list=[]
    for word in all_words:
        if len(word) < 4:
            continue
        if special_letter not in word:
            continue
        okay = True
        for s in word:
            if s not in letters:
                okay = False
                break
        if okay:
            word_list.append(word)
    return word_list

# Return True if word is in word_list otherwise return False
def is_good(word, letters, all_words):
    mistake_message = ''
    result = True
    if len(word) < 4: 
        mistake_message = 'Too short'
        result = False
    elif word not in all_words:
        mistake_message = 'Not in dictionary'
        result = False
    elif letters[0] not in word:
        mistake_message = 'Missing center letter'
        result = False
    else:
        for char in word:
            if char not in letters:
                mistake_message = 'Bad letters'
                result = False
                break
    return result, mistake_message

# Check if word is a pangram
def is_pangram(word, letters):
    if len(word) < 7:
        return False
    for char in letters:
        if char not in word:
            return False
    return True

# Computes the score of the given word
def compute_score(word, letters):
    length = len(word)
    if length == 4:
        return 1
    if is_pangram(word, letters):
        return length + 7
    return length
        
# Draw a solid hexagon
def draw_hex(Surface, color, radius, position):
    vertex_list = []
    for i in range(6):    
        x = math.cos(2 * math.pi * i / 6) * radius * 0.95 + position[0]
        y = math.sin(2 * math.pi * i / 6) * radius * 0.95 + position[1]
        vertex_list.append((x,y))
    return pygame.draw.polygon(Surface, color, vertex_list)

# Draw text centered at position
def draw_text_center(Surface, text, position, font, color):
    Text = font.render(text, True, color) 
    Surface.blit(Text, Text.get_rect(center = position))

# Draw text not centered
def draw_text(Surface, text, position, font, color):
    Text = font.render(text, True, color) 
    Surface.blit(Text, position)

# Draw the hexangonal grid for the spelling bee game
def draw_hex_grid(Surface, radius, position, letters, font, font_color):
    pi = math.pi
    draw_hex(Surface, (243,219,34), radius, position)
    draw_text_center(Surface, letters[0].upper(), position, font, font_color)
    for i in range(6):
        theta = pi/6 + i*pi*2/6
        pos = (position[0]+radius*math.sqrt(3) * math.cos(theta) , position[1] + radius*math.sqrt(3)*math.sin(theta))
        draw_hex(Surface, (230,230,230), radius, pos)
        draw_text_center(Surface, letters[i+1].upper(), pos, font, font_color)

# Shuffle the order of the letters (except for the first letter)
def shuffle_letters(letters):
    return letters[0] + ''.join(random.sample(letters[1:], len(letters[1:])))

# Generate random 7 letters
def gen_letters():
    the_word = random.choice(pangrams)
    the_string = ''.join(random.sample(set(list(the_word)), 7))
    return the_string

# Prompt for getting the letters
def get_letters(Surface):

    font = pygame.font.SysFont("Calibri", 50, True) 
    font2 = pygame.font.SysFont("Calibri", 30, True) 
    font3 = pygame.font.SysFont("Calibri", 20, True) 

    # Create shuffle button
    shuffle_button = pygame.Rect(425, 75, 50, 50)
    shuffle_icon = pygame.image.load('shuffle_icon.svg')
    shuffle_icon = pygame.transform.scale(shuffle_icon, (50,50))

    screen = pygame.display.set_mode([900,400])

    # The current entered letters
    text = ''

    # Error message if typed letters aren't allowed
    error_message = ''

    while True:

        # Quit if close button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Did the user click the shuffle button?
            if event.type == pygame.MOUSEBUTTONDOWN:
                error_message = 'Press enter'
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button
                if shuffle_button.collidepoint(mouse_pos):
                    text = gen_letters()

            if event.type == pygame.KEYDOWN:

                # Did the user press Enter?
                if event.key == pygame.K_RETURN:
                    if len(text) < 7:
                        error_message = 'Too few letters'
                    if len(text) == 7:
                        return text

                # Did the user press Backspace
                elif event.key == pygame.K_BACKSPACE:
                    error_message = ''
                    text = text[:-1]

                # Did the user press a letter?
                elif event.unicode.isalpha():
                    error_message = ''
                    if event.unicode.lower() in text:
                        error_message = 'Duplicate letter'
                    if len(text) == 7:
                        error_message = 'Press enter'
                    else:
                        text += event.unicode.lower()
                        if len(text) == 7:
                            error_message = 'Press enter'

        
        screen.fill((255,255,255))

        # Draw prompt
        draw_text_center(screen, "Enter 7 letters or randomly generate them", (450,50), font2, (143,143,143))

        # Draw error message
        draw_text_center(screen, error_message, (450,350), font3, (143,143,143))

        # Draw current typed letters
        draw_text_center(screen, text.upper(), (450,200), font, (0,0,0))

        # Draw shuffle button
        pygame.draw.rect(screen, (255,255,255), shuffle_button)
        screen.blit(shuffle_icon, shuffle_icon.get_rect(center = shuffle_button.center))

        pygame.display.flip()

# Main program
def main():

    # Run prompt for getting letters
    letter_gen_screen = pygame.display.set_mode([500,300])
    letters = get_letters(letter_gen_screen)
    # Close program if user closed the prompt
    if not letters:
        return

    # Specify the letters for the game in a string 
    # The frist character should be the central letter. 
    the_letters = letters
    special_letter = the_letters[0]

    # Creates list of valid answers
    dict = get_words(the_letters,special_letter)


    # The list of answers that have already been found
    found  = []
    found_words =[]

    # The font for the letters in the hexagons
    font = pygame.font.SysFont("Calibri", 50, True) 

    # The font for other stuff
    font2 = pygame.font.SysFont("Calibri", 30, True) 

    # The font for the already found words
    font3 = pygame.font.SysFont("Calibri", 20, True) 

    # Set up the drawing window and clock
    screen = pygame.display.set_mode([2000, 1000])

    # Create shuffle button and load the shuffle icon and scale it
    shuffle_button = pygame.Rect(475, 700, 50, 50)
    shuffle_icon = pygame.image.load('shuffle_icon.svg')
    shuffle_icon = pygame.transform.scale(shuffle_icon, (50,50))


    # Currently typed letters
    text = ''
    total_score = 0
    mistake_message = ''

    while True:
        for event in pygame.event.get():

            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                return

            # Did the user click the shuffle button?
            if event.type == pygame.MOUSEBUTTONDOWN:
                mistake_message = ''
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button
                if shuffle_button.collidepoint(mouse_pos):
                    the_letters = shuffle_letters(the_letters)
            
            # Did the user press a key?
            elif event.type == pygame.KEYDOWN:
                mistake_message = ''

                # Did the user press enter?
                if event.key == pygame.K_RETURN:
                    result, mistake_message = is_good(text, the_letters, all_words)
                    if result:
                        if text in found_words:
                            mistake_message = 'Already found'
                        else: 
                            if is_pangram(text, the_letters):
                                word_color = (26,26,24)
                            else: 
                                word_color = (143,143,143)
                            score = compute_score(text, the_letters)
                            total_score += score
                            found_display = text[0].upper() + text[1:].lower() + " (" + str(score) + ")"
                            found.append((found_display, word_color))
                            found.sort()
                            found_words.append(text)
                            print("nice")
                    print(text)
                    text = ""

                # Did the user press Backspace
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                # Did the user press a letter
                elif event.unicode.isalpha():
                    text += event.unicode.lower()

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw the spelling bee grid
        draw_hex_grid(screen, 100, (500,400), the_letters, font, (26,26,24))

        # Draw the shuffle button
        pygame.draw.rect(screen, (255,255,255), shuffle_button)
        # Draw shuffle symbol on shuffle button
        screen.blit(shuffle_icon, shuffle_icon.get_rect(center = shuffle_button.center))

        # Print currently typed letters
        draw_text_center(screen,text.upper(),(500,100), font, (26,26,24))

        # Print mistake message if relevent
        draw_text_center(screen, mistake_message, (500,850), font2, (143,143,143))

        # Print current score
        score_string = str(len(found)) + " words; " + str(total_score) + " points"
        draw_text(screen, score_string,(900,750), font3, (26,26,24))

        # Print the found answers. Pangrams are different color
        i=0
        for display, color in found:
            draw_text(screen, display, (900+ 250 * (i//20) , (i%20) * 25 + 150), font3, color)
            i+=1

        # Print message if all words are found
        if len(found) == len(dict):
            draw_text_center(screen, "Queen Bee!", (500, 850), font, (26,26,24))

        # Flip the display
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()