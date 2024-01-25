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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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
                    print('click')
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = (139, 0, 0)


def drawtittle():
    font = pygame.font.Font(None, 200)
    text = font.render("Nijia Fight", True, (139, 0, 0))
    text1 = font.render("Nijia Fight", True, (0, 0, 0))
    screen.blit(text1, (text_x + 7, text_y + 7))
    screen.blit(text, (text_x, text_y))


if __name__ == '__main__':
    pygame.init()

    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()

    pygame.display.set_caption('Недореверси')  # название окна
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    running = True

    fon = AnimatedSprite(load_image("merged_images.png"), 60, 1, 0, 0)

    textmoving = 1
    text_x = 600
    text_y = 150

    play_button = Button('play', 600, 100, (630, 470), 7)
    settings_button = Button('settings', 600, 100, (630, 600), 7)
    exit_button = Button('exit', 600, 100, (630, 730), 7)

    Window_now = 'main_menu'

    time_update = 100
    time_escaped = 0

while running:

    time = clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if Window_now == 'main_menu':
        all_sprites.draw(screen)
        time_escaped += time
        drawtittle()
        play_button.draw()
        exit_button.draw()
        settings_button.draw()

        if time_escaped >= time_update:
            time_escaped = 0
            all_sprites.update()
            if textmoving == 1:
                text_y += 1
                textmoving = 0 if text_y > 160 else 1
            else:
                text_y -= 1
                textmoving = 1 if text_y < 150 else 0

    pygame.display.flip()
