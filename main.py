import pygame
import random
import pygame_menu
from my_car import MyCar
from road import Road
from traffic import TrafficCar
from button import Button
import os

pygame.init()
screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption('Traffic Race')
clock = pygame.time.Clock()
background_color = (0, 0, 0)


def start_game():
    # Запускает основной игровой цикл
    main_game_loop()


RECORDS_FILE = 'records.txt'
ACHIEVEMENTS_FILE = 'achievements.txt'


def save_record(distance):
    # Сохраняет новый рекорд в файл, если он больше текущих
    records = load_records()
    if not records or distance > max(records):
        records.append(distance)
        records = sorted(records, reverse=True)[:5]
        with open(RECORDS_FILE, 'w', encoding='utf8') as f:
            for record in records:
                f.write(f"{record}\n")


def load_records():
    # Загружает рекорды из файла
    if not os.path.exists(RECORDS_FILE):
        return []
    with open(RECORDS_FILE, 'r', encoding='utf8') as f:
        return [int(line.strip()) for line in f.readlines()]


def show_records():
    # Отображает список рекордов на экране
    records = load_records()
    records = records if records else [0]

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)
    back_button = Button(150, 700, 200, 50, "Back to Menu",
                         36, (255, 255, 255), (255, 0, 0), (128, 0, 0), main_menu)
    reset_button = Button(150, 630, 200, 50, "Reset Records",
                          36, (255, 255, 255), (0, 255, 0), (0, 128, 0), reset_records)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            back_button.handle_event(event)
            reset_button.handle_event(event)

        screen.fill((0, 0, 0))
        y_offset = 100

        title = font.render("Top Records", True, (255, 255, 255))
        screen.blit(title, (150, 50))

        for idx, record in enumerate(records, start=1):
            record_text = small_font.render(f"{idx}. {record} m", True, (200, 200, 200))
            screen.blit(record_text, (150, y_offset))
            y_offset += 40

        back_button.draw(screen)
        reset_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)


def reset_records():
    # Сбрасывает рекорды и обновляет экран
    with open(RECORDS_FILE, 'w', encoding='utf8') as f:
        f.write("")
    show_records()


def save_achievements(achievements):
    # Сохраняет достижения игрока в файл
    with open(ACHIEVEMENTS_FILE, 'w', encoding='utf8') as f:
        for name, completed in achievements.items():
            f.write(f"{name}:{int(completed)}\n")


def load_achievements():
    # Загружает достижения игрока из файла
    achievements = {
        "Преодолей 500 метров": False,
        "Преодолей 1000 метров": False,
        "Преодолей 2500 метров": False,
        "Преодолей 5000 метров": False,
        "Преодолей 10000 метров": False,
    }
    if os.path.exists(ACHIEVEMENTS_FILE):
        with open(ACHIEVEMENTS_FILE, 'r', encoding='utf8') as f:
            for line in f.readlines():
                name, completed = line.strip().split(':')
                achievements[name] = bool(int(completed))
    return achievements


def show_achievements():
    # Отображает достижения игрока
    achievements = load_achievements()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)
    back_button = Button(150, 700, 200, 50, "Back to Menu",
                         36, (255, 255, 255), (255, 0, 0), (128, 0, 0), main_menu)

    all_completed = all(achievements.values())

    claim_button = None
    if all_completed:
        claim_button = Button(150, 630, 200, 50, "Забрать приз",
                              36, (255, 255, 255), (0, 255, 0), (0, 128, 0), claim_prize)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            back_button.handle_event(event)
            if claim_button:
                claim_button.handle_event(event)

        screen.fill((0, 0, 0))
        y_offset = 100

        title = font.render("Achievements", True, (255, 255, 255))
        screen.blit(title, (150, 50))

        for name, completed in achievements.items():
            status = "Completed" if completed else "Incomplete"
            text = small_font.render(f"{name}: {status}", True, (200, 255, 200) if completed else (255, 200, 200))
            screen.blit(text, (50, y_offset))
            y_offset += 40

        love_text = small_font.render("Выполнив все достижения получите приз", True, (255, 255, 255))
        screen.blit(love_text, (50, 600))

        back_button.draw(screen)
        if claim_button:
            claim_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def claim_prize():
    # Окно с текстом "Ты прошел игру"
    font = pygame.font.Font(None, 36)
    text_lines = [
        "Молодец, ты прошел игру",
        "и выиграл ничего XD"
    ]

    # Создаем кнопки
    submit_button = Button(150, 500, 200, 50, "Back to Menu", 36, (255, 255, 255), (0, 255, 0), (0, 128, 0), main_menu)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            submit_button.handle_event(event)

        screen.fill((0, 0, 0))

        # Отображаем текст "Ты прошел игру"
        y_offset = 250
        for line in text_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (50, y_offset))
            y_offset += 50  # Смещаем следующую строку ниже

        submit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)


game_stat = {
    "Выездов": 0,  # Количество выездов на автомобиле
    "Преодоленные машины": 0,  # Количество прошедших машин
    "Время в игре": 0,  # Время, проведенное в игре
}


def show_statistics():
    # Отображает статистику
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)
    back_button = Button(150, 700, 200, 50, "Back to Menu",
                         36, (255, 255, 255), (255, 0, 0), (128, 0, 0), main_menu)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            back_button.handle_event(event)

        screen.fill((0, 0, 0))
        y_offset = 100

        title = font.render("Statistics", True, (255, 255, 255))
        screen.blit(title, (150, 50))

        # Отображаем статистику
        stats = [
            f"Выездов: {game_stat['Выездов']}",
            f"Преодоленные машины: {game_stat['Преодоленные машины']}",
            f"Время в игре: {game_stat['Время в игре']} секунд"
        ]

        for stat in stats:
            stat_text = small_font.render(stat, True, (255, 255, 255))
            screen.blit(stat_text, (50, y_offset))
            y_offset += 40

        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)


def save_statistics():
    # Сохраняет статистику в файл
    with open('statistics.txt', 'w', encoding='utf8') as f:
        f.write(f"Выездов: {game_stat['Выездов']}\n")
        f.write(f"Преодоленные машины: {game_stat['Преодоленные машины']}\n")
        f.write(f"Время в игре: {game_stat['Время в игре']} секунд\n")


def load_statistics():
    # Загружает статистику из файла
    if not os.path.exists('statistics.txt'):
        return {'Выездов': 0, 'Преодоленные машины': 0, 'Время в игре': 0}

    with open('statistics.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        stats = {}
        for line in lines:
            key, value = line.strip().split(': ')
            stats[key] = int(value) if key != 'Время в игре' else int(value.split()[0])
        return stats


game_stat = load_statistics()  # Загружаем статистику при старте игры


def update_statistics():
    # Обновляет статистику, когда игра завершена
    game_stat["Время в игре"] = (pygame.time.get_ticks() - start_ticks) // 1000  # Время в секундах
    save_statistics()  # Сохраняем статистику


def main_game_loop():
    achievements = load_achievements()
    my_car_sound = pygame.mixer.Sound('sounds/engine.wav')
    my_car_sound.set_volume(0.1)
    my_car_sound.play(-1)

    crash_sound = pygame.mixer.Sound('sounds/crash.wav')
    crash_sound.set_volume(0.1)

    road_group = pygame.sprite.Group()
    spawn_road_time = pygame.USEREVENT
    pygame.time.set_timer(spawn_road_time, 1000)

    traffic_cars_group = pygame.sprite.Group()
    spawn_traffic_time = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_traffic_time, 750)

    global start_ticks
    start_ticks = pygame.time.get_ticks()  # Получаем время старта игры в миллисекундах
    game_stat["Выездов"] += 1  # Увеличиваем счетчик выездов при начале игры

    def get_car_image(filename, size, angle):
        # Загружает и поворачивает изображение машины
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, size)
        image = pygame.transform.rotate(image, angle)
        return image

    my_car_image = get_car_image('images/mercedes.png', (100, 70), -90)
    road_image = pygame.image.load('images/road.png')
    road_image = pygame.transform.scale(road_image, (500, 800))
    crashed_car_image = pygame.image.load('images/crashed_mercedes.jpg')
    crashed_car_image = pygame.transform.scale(crashed_car_image, (500, 800))

    traffic_car_images = [
        get_car_image('images/traffic_car1.png', (100, 70), 90),
        get_car_image('images/traffic_car2.png', (100, 70), -90),
        get_car_image('images/traffic_car3.png', (100, 70), -90),
    ]

    road = Road(road_image, (250, 400))
    road_group.add(road)
    road = Road(road_image, (250, 0))
    road_group.add(road)

    def spawn_road():
        # Спавнит новые дорожные фоны
        road_bg = Road(road_image, (250, -600))
        road_group.add(road_bg)

    def spawn_traffic():
        # Спавнит новые машины на дороге
        position = (random.randint(40, 460), random.randint(-60, -40))
        speed = random.randint(7, 20)
        traffic_car = TrafficCar(random.choice(traffic_car_images), position, speed, my_car)
        traffic_cars_group.add(traffic_car)
        game_stat["Преодоленные машины"] += 1  # Увеличиваем счетчик прошедших машин

    def draw_all():
        # Отображает все игровые элементы на экране
        road_group.update()
        road_group.draw(screen)
        traffic_cars_group.update()
        traffic_cars_group.draw(screen)
        my_car.draw(screen)

    def button_click_restart_action():
        # Действие при нажатии кнопки "Перезапустить игру"
        traffic_cars_group.empty()
        my_car_sound.play(-1)
        my_car.game_status = 'game'
        nonlocal distance_travelled
        save_record(distance_travelled)
        distance_travelled = 0
        update_statistics()  # Обновляем статистику при рестарте игры

    def button_click_menu_action():
        # Действие при нажатии кнопки "Меню"
        my_car_sound.stop()
        save_record(distance_travelled)
        save_achievements(achievements)
        update_statistics()  # Обновляем статистику перед выходом в меню
        main_menu()

    button_repair = Button(0, 500, 500, 50, "Restart game",
                           36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_restart_action)

    button_menu = Button(0, 570, 500, 50, "Exit to Menu",
                         36, (255, 255, 255), (255, 0, 0), (128, 0, 0), button_click_menu_action)

    my_car = MyCar((300, 600), my_car_image)

    distance_travelled = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == spawn_road_time:
                spawn_road()
            if event.type == spawn_traffic_time:
                spawn_traffic()
            button_repair.handle_event(event)
            button_menu.handle_event(event)

        if my_car.rect.top > 0 and my_car.game_status == 'game':
            my_car.move()
            distance_travelled += 1

            # Проверка на достижение новых достижений
            if distance_travelled >= 500 and not achievements["Преодолей 500 метров"]:
                achievements["Преодолей 500 метров"] = True
            if distance_travelled >= 1000 and not achievements["Преодолей 1000 метров"]:
                achievements["Преодолей 1000 метров"] = True
            if distance_travelled >= 2500 and not achievements["Преодолей 2500 метров"]:
                achievements["Преодолей 2500 метров"] = True
            if distance_travelled >= 5000 and not achievements["Преодолей 5000 метров"]:
                achievements["Преодолей 5000 метров"] = True
            if distance_travelled >= 10000 and not achievements["Преодолей 10000 метров"]:
                achievements["Преодолей 10000 метров"] = True

        screen.fill(background_color)
        if my_car.game_status == 'game':
            draw_all()
            my_car.crash(crash_sound, traffic_cars_group)

            # ✅ Отображаем счетчик только в режиме "game"
            font = pygame.font.Font(None, 36)
            distance_text = font.render(f'{distance_travelled} m', True, (255, 255, 255))
            screen.blit(distance_text, (400, 20))

        elif my_car.game_status == 'game_over':
            screen.blit(crashed_car_image, (0, 0))
            my_car_sound.stop()
            button_repair.draw(screen)
            button_menu.draw(screen)

        game_stat["Время в игре"] = (pygame.time.get_ticks() - start_ticks) // 1000  # Время в секундах

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main_menu():
    # Главное меню игры

    menu = pygame_menu.Menu(
        height=800,
        width=500,
        theme=pygame_menu.themes.THEME_DARK.copy(),
        title='Welcome to Traffic Race :3',
    )
    menu.get_theme().widget_font = pygame_menu.font.FONT_BEBAS
    menu.get_theme().widget_font_color = (255, 255, 255)
    menu.get_theme().title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

    menu.add.button('Play', start_game)
    menu.add.button('Instructions', show_instructions)
    menu.add.button('Records', show_records)
    menu.add.button('Achievements', show_achievements)
    menu.add.button('Statistics', show_statistics)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        menu.update(pygame.event.get())
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)


def show_instructions():
    instructions = [
        "Добро пожаловать в игру Traffic Race!",
        "",
        "Управление:",
        "- Используйте кнопки W A S D что бы "
        "",
        "  управлять автомобилем.",

        "",
        "Игра:",
        "- Уворачивайтесь от встречных машин.",
        "- Достигайте новых рекордов!",
        "Удачи на дороге!",
    ]

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)
    back_button = Button(150, 700, 200, 50, "Back to Menu",
                         36, (255, 255, 255), (255, 0, 0), (128, 0, 0), main_menu)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            back_button.handle_event(event)

        screen.fill((0, 0, 0))

        y_offset = 100

        title = font.render("Инструкция", True, (255, 255, 255))
        screen.blit(title, (150, y_offset))
        y_offset += 50

        for line in instructions:
            if line.strip() == "":
                y_offset += 20
            else:
                text = small_font.render(line, True, (255, 255, 255))
                screen.blit(text, (50, y_offset))
                y_offset += 40
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
