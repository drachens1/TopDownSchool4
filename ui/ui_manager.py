from order.orders import FACE_TYPE, GO_TO_TYPE, STAND_STILL_TYPE, FOLLOW_TYPE
from ui.button import Button


class UiManager:
    follow_button: Button
    go_to_button: Button
    stand_still_button: Button
    face_button: Button
    current_order_creation: int

    def __init__(self):
        y = 100
        w = 50
        h = 50
        self.follow_button = Button("Follow", 100, y, w, h)
        self.go_to_button = Button("Go To", 200, y, w, h)
        self.stand_still_button = Button("Stand still", 300, y, w, h)
        self.face_button = Button("Face", 400, y, w, h)
        self.current_order_creation = -1

    def on_click(self) -> int:
        clicked = self.face_button.hover
        self.face_button.set_clicked(clicked)
        if clicked: return FACE_TYPE
        clicked = self.go_to_button.hover
        self.go_to_button.set_clicked(clicked)
        if clicked: return GO_TO_TYPE
        clicked = self.stand_still_button.hover
        self.stand_still_button.set_clicked(clicked)
        if clicked: return STAND_STILL_TYPE
        clicked = self.follow_button.hover
        self.follow_button.set_clicked(clicked)
        if clicked: return FOLLOW_TYPE
        return -1

    def set_button_active(self, order_type: int):
        self.face_button.set_active(False)
        self.go_to_button.set_active(False)
        self.stand_still_button.set_active(False)
        self.follow_button.set_active(False)
        self.current_order_creation = order_type
        if order_type == FACE_TYPE:
            self.face_button.set_active(True)
        elif order_type == GO_TO_TYPE:
            self.go_to_button.set_active(True)
        elif order_type == STAND_STILL_TYPE:
            self.stand_still_button.set_active(True)
        elif order_type == FOLLOW_TYPE:
            self.follow_button.set_active(True)


    def on_hover(self, mouse_x: int, mouse_y: int) -> bool:
        hover = self.face_button.on_hover(mouse_x, mouse_y)
        self.face_button.set_hover(hover)
        if hover: return True
        hover = self.go_to_button.on_hover(mouse_x, mouse_y)
        self.go_to_button.set_hover(hover)
        if hover: return True
        hover = self.stand_still_button.on_hover(mouse_x, mouse_y)
        self.stand_still_button.set_hover(hover)
        if hover: return True
        hover = self.follow_button.on_hover(mouse_x, mouse_y)
        self.follow_button.set_hover(hover)
        return hover

    def not_click(self):
        self.face_button.set_clicked(False)
        self.go_to_button.set_clicked(False)
        self.stand_still_button.set_clicked(False)
        self.follow_button.set_clicked(False)

    def render(self, WIN, font):
        self.face_button.render(WIN, font)
        self.go_to_button.render(WIN, font)
        self.stand_still_button.render(WIN, font)
        self.follow_button.render(WIN, font)