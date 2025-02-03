import pygame


class Button:
    def __init__(self, x, y, width, height, text, font, text_color, button_color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        if self.is_hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.button_color, self.rect)

        font = pygame.font.Font(None, self.font)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.action()


def button_click_action():
    print("Button Clicked!")


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

button = Button(300, 200, 200, 50, "Click Me", 36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_action)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button.handle_event(event)

    screen.fill((0, 0, 0))
    button.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
