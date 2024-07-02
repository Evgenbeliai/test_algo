import pygame

pygame.init()

width, height = 1200. 700
screen = pygame.display.set_mode((width, height))

# Загрузка заднего фона и персонажа
background = pygame.image.load("bg.jpg")  # Замените "bg.jpg" на путь к вашему файлу с задним фоном
background = pygame.transform.scale(background, (width, height))


class Hero(pygame.sprite.Sprite):
    def __init__(self, animation_idle, animation_attack, x_img, y_img):
        self.animation_idle = animation_idle
        self.animation_attack = animation_attack

        self.character_rect = self.animation_idle[0].get_rect()
        self.character_rect.topleft = (x_img, y_img)
        self.animation_timer = 0
        self.current_frame = 0
        self.is_jumping = False
        self.jump_count = 8  # Высота прыжка
        self.gravity = 0.1  # Сила гравитации
        self.y_velocity = 0  # Начальная вертикальная скорость
        self.is_attacking = False

    def blit(self, animation_speed):
        if self.is_attacking:
            self.attack_animation_blit(animation_speed)
        else:
            screen.blit(self.animation_idle[self.current_frame], self.character_rect)
            self.animation_timer += 1
            if self.animation_timer >= animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_idle)

    def attack_animation_blit(self, animation_speed):
        screen.blit(self.animation_attack[self.current_frame], self.character_rect)
        self.animation_timer += 2
        if self.animation_timer >= animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_attack)
            if self.current_frame == 0:
                self.is_attacking = False

    def move_left(self, pixels):
        self.character_rect.x -= pixels
        self.direction = -1  # Устанавливаем направление влево

    def move_right(self, pixels):
        self.character_rect.x += pixels
        self.direction = 1  # Устанавливаем направление вправо

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = -self.jump_count

    def apply_gravity(self):
        if self.y_velocity < 5:  # Максимальная скорость падения
            self.y_velocity += self.gravity
        self.character_rect.y += self.y_velocity

        # Проверка столкновения с землей (например, высотой экрана)
        if self.character_rect.y >= height - self.character_rect.height:
            self.is_jumping = False
            self.y_velocity = 0
            self.character_rect.y = height - self.character_rect.height

    def attack(self):
        self.is_attacking = True
        self.current_frame = 0  # Сброс текущего кадра при начале анимации удара


animation_hero_idle = []
for i in range(1, 8):
    img = pygame.image.load(f"D:\MK\Hero Animation\stop\{i}_stop.png")
    animation_hero_idle.append(pygame.transform.scale(img, (img.get_width() + 100, img.get_height() + 200)))

animation_hero_attack = []
for i in range(1, 4):
    img = pygame.image.load(f"D:\MK\Hero Animation\hatack\{i}_atack.png")
    animation_hero_attack.append(pygame.transform.scale(img, (img.get_width() + 100, img.get_height() + 200)))

hero1 = Hero(animation_hero_idle, animation_hero_attack, 100, 600)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Прыжок по клавише SPACE
                hero1.jump()
            elif event.key == pygame.K_e:  # Атака по клавише E
                hero1.attack()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        hero1.move_left(1)
    elif keys[pygame.K_d]:
        hero1.move_right(1)
    else:
        hero1.direction = 0
    # Очистка экрана
    screen.blit(background, (0, 0))

    # Обновление экрана
    hero1.apply_gravity()  # Применение гравитации
    hero1.blit(100)  # Скорость анимации

    pygame.display.flip()

pygame.quit()
