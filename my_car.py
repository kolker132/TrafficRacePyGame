import pygame.key
import pygame


class MyCar(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = 5  # Скорость движения
        self.game_status = 'game'
        self.fps = 60

    def move(self):
        keys = pygame.key.get_pressed()
        # Движение влево
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        # Движение вправо
        if keys[pygame.K_d] and self.rect.right < 500:
            self.rect.x += self.speed
        # Движение вперед (вверх)
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        # Движение назад (вниз)
        if keys[pygame.K_s] and self.rect.bottom < 800:
            self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def crash(self, crash_sound, traffic_cars_group):
        # Проверка на столкновение с трафиком
        if pygame.sprite.spritecollide(self, traffic_cars_group, False):
            self.game_status = 'game_over'
            crash_sound.play()
