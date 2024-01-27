import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, pack_name, count):
        super().__init__(sprite_fon)
        self.pack_name = pack_name
        self.count = count
        self.frames = []
        self.download_images()
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def download_images(self):
        self.rect = pygame.Rect(0, 0, width, height)
        for i in range(1, self.count + 1):
            self.image = load_image(self.pack_name + '/' + '0' * (4 - len(str(i))) + str(i) + '.jpg')
            self.frames.append(self.image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % (self.count - 1)
        self.image = self.frames[self.cur_frame]

    def draw(self, scren):
        scren.blit(self.image, self.rect)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, pack_name, count, sprite_width, sprite_height):
        super().__init__(ninjas_sprites)
        self.sprite_width, self.sprite_height = sprite_width, sprite_height
        self.pack_name = pack_name
        self.count = count

        self.stand = []
        self.walk = []
        self.run = []
        self.hit = []
        self.die = []
        self.attack = []
        self.frames = [self.stand, self.walk, self.run, self.hit, self.die, self.attack]
        self.list_pack_names = ['Stand', 'Walk', 'Run', 'Hit', 'Die', 'Attack']

        self.animashion_now = 0

        self.download_images()
        self.cur_frame = 0
        self.image = self.frames[self.animashion_now][self.cur_frame]
        self.rect = self.rect.move(x, y)

    def download_images(self):
        self.rect = pygame.Rect(0, 0, self.sprite_width, self.sprite_height)
        for j in range(len(self.list_pack_names)):
            for i in range(self.count):
                self.image = load_image(self.pack_name + '/' + self.list_pack_names[j] + '/' + str(i) + '.png')
                self.image = pygame.transform.scale(self.image, (720, 720))
                self.frames[j].append(self.image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % self.count
        self.image = self.frames[self.animashion_now][self.cur_frame]

    def draw(self, scren):
        scren.blit(self.image, self.rect)

    def go(self, x, y):
        self.rect = self.rect.move(x, y)

    def revers(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Button:
    def __init__(self, button_text, buttonwidth, buttonheight, pos, elevation):
        # Core attributes
        self.button_text = button_text
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (buttonwidth, buttonheight))
        self.top_color = (139, 0, 0)

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (buttonwidth, buttonheight))
        self.bottom_color = (0, 0, 0)
        # text
        self.font = pygame.font.Font(None, 90)
        self.text_surf = self.font.render(self.button_text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global Window_now, Music, music_button
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (200, 0, 0)
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed:
                    if self.button_text == 'exit':
                        exit()
                    elif self.button_text == 'play':
                        Window_now = 'play_menu'
                    elif self.button_text == 'back' and Window_now == 'play_menu':
                        Window_now = 'main_menu'
                    elif self.button_text == 'start':
                        Window_now = 'start_menu'
                    elif self.button_text == 'back' and Window_now == 'start_menu':
                        Window_now = 'play_menu'
                    elif self.button_text == 'settings':
                        Window_now = 'settings_menu'
                    elif self.button_text == 'back' and Window_now == 'settings_menu':
                        Window_now = 'main_menu'
                    elif self.button_text == 'music on':
                        self.button_text = 'music off'
                        Music = False
                        music_button = Button('music off', 600, 100, (630, 600), 7)
                    elif self.button_text == 'music off':
                        music_button = Button('music on', 600, 100, (630, 600), 7)
                        Music = True
                    elif self.button_text == 'account':
                        Window_now = 'account_menu'
                    elif self.button_text == 'back' and Window_now == 'account_menu':
                        Window_now = 'settings_menu'
                    elif self.button_text == 'play solo':
                        Window_now = 'play solo'
                        start_game()
                    print('click')
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = (139, 0, 0)
            if self.pressed and not (self.top_rect.collidepoint(mouse_pos)):
                self.pressed = False


def shadow_text(text, text_shadow, text_x, text_y):
    screen.blit(text_shadow, (text_x - 3, text_y))
    screen.blit(text_shadow, (text_x - 3, text_y + 3))
    screen.blit(text_shadow, (text_x - 3, text_y - 3))
    screen.blit(text_shadow, (text_x, text_y - 3))
    screen.blit(text_shadow, (text_x + 3, text_y))
    screen.blit(text_shadow, (text_x + 3, text_y - 3))
    screen.blit(text_shadow, (text_x + 3, text_y + 3))
    screen.blit(text_shadow, (text_x, text_y + 3))
    screen.blit(text, (text_x, text_y))


def draw_tittle():
    font = pygame.font.Font(None, 200)
    text = font.render("Nijia Fight", True, (139, 0, 0))
    text1 = font.render("Nijia Fight", True, (0, 0, 0))
    screen.blit(text1, (text_main_x + 7, text_main_y + 7))
    screen.blit(text, (text_main_x, text_main_y))


def start_game():
    global player1, skin1, player2, skin2, rever, \
        fight_player_1, fight_player_2, health_1, health_2, health_background_1, health_background_2, \
        text_time_shadow, text_time, font_text_time, round_time, time_ms, text_time_x, text_time_y, win, win_animation, \
        text_player_1_shadow, text_player_1, text_player_2_shadow, text_player_2, text_player_1_x, text_player_1_y, \
        text_player_2_x, text_player_2_y, zajim_player_1, zajim_player_2
    player1 = 'oktay'
    skin1 = list_of_ninjas[0]
    player2 = 'AI'
    skin2 = list_of_ninjas[1]
    skin2.revers()

    zajim_player_1 = False
    zajim_player_2 = False
    rever = True
    fight_player_1 = False
    fight_player_2 = False
    win = -1
    win_animation = False

    time_ms = 0

    round_time = 99

    skin1.cur_frame = -1
    skin2.cur_frame = -1

    skin1.rect.x, skin1.rect.y = 0, 570
    skin2.rect.x, skin2.rect.y = 1180, 570

    skin1.animashion_now = 0
    skin2.animashion_now = 0

    health_background_1 = [[200, 140], [850, 140], [890, 180], [240, 180]]
    health_background_2 = [[1060, 140], [1710, 140], [1670, 180], [1020, 180]]
    health_1 = [[213, 145], [848, 145], [878, 175], [243, 175]]
    health_2 = [[1063, 145], [1698, 145], [1668, 175], [1033, 175]]

    text_time_x = 905
    text_time_y = 120
    font_text_time = pygame.font.Font(None, 130)
    text_time = font_text_time.render(str(round_time), True, (255, 0, 0))
    text_time_shadow = font_text_time.render(str(round_time), True, (0, 0, 0))

    font_player_text = pygame.font.Font(None, 100)
    text_player_1 = font_player_text.render(player1, True, (200, 0, 0))
    text_player_1_shadow = font_player_text.render(player1, True, (0, 0, 0))
    text_player_2 = font_player_text.render(player2, True, (200, 0, 0))
    text_player_2_shadow = font_player_text.render(player2, True, (0, 0, 0))
    text_player_1_x, text_player_1_y = 210, 70
    text_player_2_x, text_player_2_y = 1700 - 50 * len(player2), 70


if __name__ == '__main__':
    pygame.init()

    ninjas_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite_fon = pygame.sprite.Group()

    pygame.display.set_caption('Ninja Fight')  # название окна
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    running = True

    fon = BackgroundSprite(0, 0, 'fon', 240)

    white_ninja = AnimatedSprite(0, 1500, 'SamuraiLight', 10, 500, 500)
    heavy_ninja = AnimatedSprite(0, 1500, 'SamuraiHeavy', 10, 500, 500)
    ninja_ninja = AnimatedSprite(0, 1500, 'Ninja', 10, 500, 500)

    list_of_ninjas = [white_ninja, heavy_ninja, ninja_ninja]

    text_moving = 1
    text_main_x = 600
    text_main_y = 150

    play_button = Button('play', 600, 100, (630, 470), 7)
    settings_button = Button('settings', 600, 100, (630, 600), 7)
    exit_button = Button('exit', 600, 100, (630, 730), 7)

    start_play_button = Button('start', 600, 100, (630, 470), 7)
    inventory_button = Button('inventory', 600, 100, (630, 600), 7)
    back_button = Button('back', 600, 100, (630, 730), 7)

    play_solo_button = Button('play solo', 600, 100, (630, 470), 7)
    play_duo_button = Button('play duo', 600, 100, (630, 600), 7)

    account_button = Button('account', 600, 100, (630, 470), 7)
    music_button = Button('music on', 600, 100, (630, 600), 7)

    signin_button = Button('sign in', 600, 100, (630, 470), 7)
    signup_button = Button('sign up', 600, 100, (630, 600), 7)

    Window_now = 'main_menu'

    time_update = 100
    time_escaped = 0
    GO = 10

    Music = True

while running:
    time = clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if (Window_now == 'main_menu' or Window_now == 'play_menu' or
            Window_now == 'start_menu' or Window_now == 'settings_menu' or Window_now == 'account_menu'):
        time_escaped += time

        sprite_fon.draw(screen)
        draw_tittle()

        if time_escaped >= time_update:
            time_escaped = 0
            sprite_fon.update()
            if text_moving == 1:
                text_main_y += 1
                text_moving = 0 if text_main_y > 160 else 1
            else:
                text_main_y -= 1
                text_moving = 1 if text_main_y < 150 else 0

    if Window_now == 'main_menu':
        play_button.draw()
        settings_button.draw()
        exit_button.draw()

    elif Window_now == 'play_menu':
        start_play_button.draw()
        inventory_button.draw()
        back_button.draw()

    elif Window_now == 'start_menu':
        play_solo_button.draw()
        play_duo_button.draw()
        back_button.draw()

    elif Window_now == 'settings_menu':
        account_button.draw()
        music_button.draw()
        back_button.draw()

    elif Window_now == 'account_menu':
        signin_button.draw()
        signup_button.draw()
        back_button.draw()

    elif Window_now == 'play solo':
        time_escaped += time

        sprite_fon.draw(screen)

        skin2.draw(screen)
        skin1.draw(screen)

        pygame.draw.polygon(screen, (50, 0, 0), health_background_1)
        pygame.draw.polygon(screen, (50, 0, 0), health_background_2)
        pygame.draw.polygon(screen, (pygame.Color('red')), health_1)
        pygame.draw.polygon(screen, (pygame.Color('red')), health_2)

        shadow_text(text_player_1, text_player_1_shadow, text_player_1_x, text_player_1_y)
        shadow_text(text_player_2, text_player_2_shadow, text_player_2_x, text_player_2_y)
        shadow_text(text_time, text_time_shadow, text_time_x, text_time_y)

        if time_escaped >= time_update:
            time_escaped = 0
            if win == 1:
                if skin2.cur_frame == 8:
                    Window_now = 'start_menu'
            elif win == 2:
                if skin1.cur_frame == 8:
                    Window_now = 'start_menu'
            else:
                time_ms += 1
                if time_ms == 10:
                    round_time -= 1
                    if round_time == 0:
                        Window_now = 'start_menu'
                    elif round_time < 10:
                        text_time_x = 940
                    time_ms = 0
                    text_time = font_text_time.render(str(round_time), True, (255, 0, 0))
                    text_time_shadow = font_text_time.render(str(round_time), True, (0, 0, 0))

            keys = pygame.key.get_pressed()

            if win != 1:
                if (rever and skin1.rect.x < skin2.rect.x <= skin1.rect.x + 400 or fight_player_2 or
                        not rever and skin2.rect.x < skin1.rect.x <= skin2.rect.x + 400):
                    if not fight_player_2:
                        skin2.cur_frame = -1
                        skin2.animashion_now = 5
                        fight_player_2 = True
                        zajim_player_2 = True
                    if skin2.cur_frame == 4:
                        if (rever and skin1.rect.x < skin2.rect.x <= skin1.rect.x + 400 or
                                not rever and skin2.rect.x < skin1.rect.x <= skin2.rect.x + 400):
                            health_1 = [health_1[0],
                                        [health_1[1][0] - 127, health_1[1][1]],
                                        [health_1[2][0] - 127, health_1[2][1]], health_1[3]]
                        if health_1[1] <= health_1[0]:
                            health_1 = [[0, 0], [0, 0], [0, 0], [0, 0]]
                            win = 2
                            if not win_animation:
                                skin1.cur_frame = 0
                                skin2.animashion_now = 0
                                skin1.animashion_now = 4
                                win_animation = True
                    if skin1.cur_frame == 8:
                        fight_player_2 = False
                else:
                    if win == -1:
                        if zajim_player_2:
                            skin1.cur_frame = -1
                        skin2.animashion_now = 1
                        zajim_player_2 = False
                        if rever:
                            skin2.rect.x -= 15
                        else:
                            skin2.rect.x += 17

            if win != 2:
                if keys[pygame.K_h] or fight_player_1:
                    if not fight_player_1:
                        skin1.cur_frame = -1
                        skin1.animashion_now = 5
                        fight_player_1 = True
                    if skin1.cur_frame == 4:
                        if (rever and skin1.rect.x < skin2.rect.x <= skin1.rect.x + 500 or
                                not rever and skin2.rect.x < skin1.rect.x <= skin2.rect.x + 500):
                            health_2 = [health_2[0],
                                        [health_2[1][0] - 127, health_2[1][1]],
                                        [health_2[2][0] - 127, health_2[2][1]], health_2[3]]
                        if health_2[1] <= health_2[0]:
                            health_2 = [[0, 0], [0, 0], [0, 0], [0, 0]]
                            win = 1
                            if not win_animation:
                                skin2.cur_frame = 0
                                skin2.animashion_now = 4
                                win_animation = True
                    if skin1.cur_frame == 8:
                        fight_player_1 = False
                else:
                    if (keys[pygame.K_a] and skin1.rect.x > end_x_left and keys[
                        pygame.K_d] and skin1.rect.x < end_x_right or
                            keys[pygame.K_a] and keys[pygame.K_LSHIFT] and skin1.rect.x > end_x_left and keys[
                                pygame.K_d]
                            and skin1.rect.x < end_x_right):
                        skin1.animashion_now = 0
                        if zajim_player_1:
                            skin1.cur_frame = -1
                        zajim_player_1 = False
                    elif keys[pygame.K_a] and keys[pygame.K_LSHIFT] and skin1.rect.x > end_x_left:
                        if not zajim_player_1:
                            skin1.cur_frame = -1
                            zajim_player_1 = True
                        skin1.animashion_now = 2
                        skin1.go(-25, 0)
                    elif keys[pygame.K_d] and keys[pygame.K_LSHIFT] and skin1.rect.x < end_x_right:
                        if not zajim_player_1:
                            skin1.cur_frame = -1
                            zajim_player_1 = True
                        skin1.animashion_now = 2
                        skin1.go(25, 0)
                    elif keys[pygame.K_a] and skin1.rect.x > end_x_left:
                        if not zajim_player_1:
                            skin1.cur_frame = -1
                            zajim_player_1 = True
                        skin1.animashion_now = 1
                        skin1.go(-10, 0)
                    elif keys[pygame.K_d] and skin1.rect.x < end_x_right:
                        if not zajim_player_1:
                            skin1.cur_frame = -1
                            zajim_player_1 = True
                        skin1.animashion_now = 1
                        skin1.go(10, 0)
                    else:
                        if zajim_player_1:
                            skin1.cur_frame = -1
                        skin1.animashion_now = 0
                        zajim_player_1 = False

            sprite_fon.update()
            skin1.update()
            skin2.update()
            if rever and skin1.rect.x > skin2.rect.x - 290:
                rever = False
                skin1.go(290, 0)
                skin2.go(-290, 0)
            elif not rever and skin2.rect.x > skin1.rect.x - 290:
                rever = True
                skin1.go(-290, 0)
                skin2.go(290, 0)
            if rever:
                end_x_left = -250
                end_x_right = 1180
                skin2.revers()
            else:
                skin1.revers()
                end_x_left = -250 + 290
                end_x_right = 1180 + 290

    pygame.display.flip()
