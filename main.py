import pygame

from camera import Camera
from loader import load_central_manager
from order.order_creation import order_creation_update, order_creation_finish
from ui.ui_manager import UiManager

pygame.init()

running = True

WIN = pygame.display.set_mode([500, 500])
pygame.display.set_caption("Window")
camera = Camera(-100, -100)
font = pygame.font.Font(None, 32)

central_manager = load_central_manager("map.txt")
ui_manager = UiManager()

clock = pygame.time.Clock()
while running:
    WIN.fill([0,0,0])

    buttons = pygame.mouse.get_pressed()

    left_held  = buttons[0]
    middle_held = buttons[1]
    right_held = buttons[2]

    x, y = pygame.mouse.get_pos()
    if central_manager.has_active_troop():
        hover = ui_manager.on_hover(x, y)
        order_creation_update(x, y, camera, central_manager.troops_manager.active_troop_id,
                              ui_manager.current_order_creation, central_manager.order_manager)
        if left_held:
            id = ui_manager.on_click()
            ui_manager.set_button_active(id)
        else:
            ui_manager.not_click()
    else:
        hover = False
        order_creation_finish(central_manager.order_manager, central_manager.troops_manager)

    mouse_down = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not hover:
                central_manager.on_click(x, y, camera)

    central_manager.render(WIN, camera)
    if central_manager.has_active_troop():
        ui_manager.render(WIN, font)

    down = pygame.key.get_pressed()
    if down[pygame.K_w]:
        camera.add_y(-2)
    elif down[pygame.K_s]:
        camera.add_y(2)
    if down[pygame.K_d]:
        camera.add_x(2)
    elif down[pygame.K_a]:
        camera.add_x(-2)

    if down[pygame.K_q]:
        camera.add_zoom(0.05)
    elif down[pygame.K_e]:
        camera.add_zoom(-0.05)

    pygame.display.update()
    clock.tick(30)
