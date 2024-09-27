import pygame
from sys import exit
from random import shuffle
import word_banks

pygame.init()
pygame.time.Clock()
pygame.display.set_caption('Connections')

# Global Vars
screen = pygame.display.set_mode((800, 650))
game_active = True
font = pygame.font.Font('arial-font/arial.ttf', 12)
subtitle_font = pygame.font.Font('arial-font/arial.ttf', 16)
title_font = pygame.font.Font('arial-font/arial.ttf', 25)
answer_groups = word_banks.super_hard
word_bank = [item for group in list(map(lambda group: group[1], answer_groups)) for item in group]
complete_sets = []
cards = []
selected_cards = []
num_complete = 0
num_mistakes_left = 5
start_time = 0
shuffle_rect = pygame.Rect(200, 525, 125, 75)
submit_rect = pygame.Rect(475, 525, 125, 75)
play_button_rect = pygame.Rect(300, 300, 200, 75)
play_text = font.render('PLAY AGAIN', True, 'Black')
play_rect = play_text.get_rect(center=(400, 337.5))
fail_sound = pygame.mixer.Sound('sounds/fail.mp3')
success_sound = pygame.mixer.Sound('sounds/success.mp3')

class Card:
    def __init__(self, text):
        self.text = text
        self.word = font.render(text, True, 'Black')
        self.word_rect = self.word.get_rect(center = (0, 0))
        self.selected = False
        self.complete = False
        self.card_rect = pygame.Rect(0, 0, 100, 75)
        self.bg_color = 'white'

    def draw(self):
        pygame.draw.rect(screen, self.bg_color, self.card_rect, border_radius=5)
        screen.blit(self.word, self.word_rect)

class CompleteSet:
    def __init__(self, category, words, x, y, bg_color):
        self.box_rect = pygame.Rect(x-237.5, y-37.5, 475, 75)
        self.words = font.render(', '.join(words), True, 'Black')
        self.words_rect = self.words.get_rect(center = (x, y+15))
        self.category = title_font.render(category, True, 'Black')
        self.category_rect = self.category.get_rect(center=(x, y-5))
        self.bg_color = bg_color

    def draw(self):
        pygame.draw.rect(screen, self.bg_color, self.box_rect, border_radius=5)
        screen.blit(self.category, self.category_rect)
        screen.blit(self.words, self.words_rect)

def generate_cards():
    for word in word_bank:
        card = Card(word)
        cards.append(card)

def shuffle_cards():
    shuffle(cards)

def draw_cards():
    x, y = 212.5, 125 + 100*num_complete
    for i in range(len(cards)):
        card = cards[i]
        word = card.word
        card.word_rect = word.get_rect(center = (x, y))
        card.card_rect = pygame.Rect(x-50, y-37.5, 100, 75)
        card.draw()
        x += 125
        if (i+1) % 4 == 0:
            x = 212.5
            y += 100

def draw_complete_sets():
    x, y = 400, 125
    for complete_set in complete_sets:
        completed = CompleteSet(complete_set[0], complete_set[1], x, y, complete_set[2])
        completed.draw()
        y += 100

def draw_shuffle_button():
    pygame.draw.rect(screen, 'White', shuffle_rect, border_radius=5)
    text = font.render('SHUFFLE', True, 'Black')
    text_rect = text.get_rect(center = (262.5, 562.5))
    screen.blit(text, text_rect)

def draw_submit_button():
    pygame.draw.rect(screen, 'White', submit_rect, border_radius=5)
    text = font.render('SUBMIT', True, 'Black')
    text_rect = text.get_rect(center = (537.5, 562.5))
    screen.blit(text, text_rect)

def draw_remaining():
    remaining_text = subtitle_font.render('Mistakes Remaining:', True, 'Black')
    remaining_rect = remaining_text.get_rect(midleft=(225, 495))
    cover_rect = pygame.Rect(385, 480, 200, 25)
    pygame.draw.rect(screen, 'Tan', cover_rect)
    
    x = 400
    for i in range(num_mistakes_left):
        dot = pygame.image.load('imgs/dot.png').convert_alpha()
        dot = pygame.transform.rotozoom(dot, 0, 0.015)
        dot_rect = dot.get_rect(center=(x, 495))
        screen.blit(dot, dot_rect)
        x += 25
    
    screen.blit(remaining_text, remaining_rect)

def check_guess():
    global selected_cards, num_complete, num_mistakes_left, game_active, cards
    is_set = False
    selected_words = list(map(lambda card: card.text, selected_cards))
    for group in answer_groups:
        if set(selected_words) == set(group[1]):
            for card in selected_cards:
                card.complete = True
                card.bg_color = group[2]
                card.draw()
            selected_cards.clear()
            num_complete += 1
            is_set = True
            complete_sets.append(group)
            cards = list(filter(lambda card: card.text not in selected_words, cards))

            pygame.display.update()
            pygame.time.delay(1000)
            draw_complete_sets()
            draw_cards()
            pygame.display.update()
                
    if num_complete == 4:
        cards.clear()
        game_active = False
        pygame.time.wait(3000)
        draw_finish_screen()
    if not is_set:
        num_mistakes_left -= 1
        draw_remaining()
        if num_mistakes_left == 0:
            pygame.display.update()
            cards.clear()
            game_active = False
            pygame.time.delay(1000)
            draw_fail_screen()


def draw_finish_screen():
    success_sound.play()
    finish_text = title_font.render('Congratulations', True, 'Black')
    finish_rect = finish_text.get_rect(center=(400, 200))
    cur_time = (pygame.time.get_ticks() - start_time) // 1000
    min = cur_time // 60
    sec = cur_time % 60
    time_text = subtitle_font.render(f'You finished in {min} min. {sec} sec.', True, 'Black')
    time_rect = time_text.get_rect(center=(400, 250))

    screen.fill('Green')
    screen.blit(finish_text, finish_rect)
    screen.blit(time_text, time_rect)
    pygame.draw.rect(screen, 'White', play_button_rect, border_radius=5)
    screen.blit(play_text, play_rect)

def draw_fail_screen():
    fail_sound.play()
    fail_text = title_font.render('Better Luck Next Time', True, 'Black')
    fail_rect = fail_text.get_rect(center=(400, 250))

    screen.fill('Grey')
    screen.blit(fail_text, fail_rect)
    pygame.draw.rect(screen, 'White', play_button_rect, border_radius=5)
    screen.blit(play_text, play_rect)

def init_game():
    global num_mistakes_left, start_time, game_active, cards, selected_cards, num_complete
    screen.fill("Tan")
    start_time = pygame.time.get_ticks()
    num_mistakes_left = 5
    game_active = True
    cards.clear()
    selected_cards.clear()
    complete_sets.clear()
    num_complete = 0

    instructions_text = subtitle_font.render('Make 4 groups of 4', True, 'Black')
    instructions_rect = instructions_text.get_rect(center=(400, 55))
    screen.blit(instructions_text, instructions_rect)

    generate_cards()
    shuffle_cards()
    draw_cards()
    draw_remaining()
    draw_shuffle_button()
    draw_submit_button()

init_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                if shuffle_rect.collidepoint(event.pos):
                    shuffle_cards()
                    draw_cards()
                elif submit_rect.collidepoint(event.pos):
                    if len(selected_cards) == 4:
                        check_guess()
                else:
                    for card in cards:
                        if card.card_rect.collidepoint(event.pos):
                            if not card.complete:
                                if card.selected:
                                    card.selected = False
                                    selected_cards.remove(card)
                                    card.bg_color = 'White'
                                    card.draw()
                                else:
                                    if len(selected_cards) < 4:
                                        card.selected = True
                                        selected_cards.append(card)
                                        card.bg_color = 'Grey'
                                        card.draw()
            else:
                if play_button_rect.collidepoint(event.pos):
                    answer_groups = word_banks.law
                    word_bank = [item for group in list(map(lambda group: group[1], answer_groups)) for item in group]                    
                    init_game()

    pygame.display.update()
