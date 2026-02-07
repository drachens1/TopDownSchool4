from order.order_creators import OrderCreator
from order.orders import Order
from troop.troops_manager import TroopsManager

class OrderManager:
    orders: list[Order]
    free_list: list[int]
    order_creation: OrderCreator

    def __init__(self):
        self.orders = []
        self.free_list = []
        self.order_creation = None

    def add_order(self, order) -> int:
        self.orders.append(order)
        return len(self.orders) - 1

    def remove_order(self, order_id: int):
        print("prev")
        self.orders.pop(order_id)

    def render(self, WIN, camera):
        for order in self.orders:
            order.render(WIN, camera)
        if self.order_creation != None:
            self.order_creation.render(WIN, camera)

    def tick(self, map, troop_manager: TroopsManager, mx, my, camera):
        for i, order in enumerate(self.orders):
            order.order_tick(map, troop_manager)
            if order.finished:
                self.remove_order(i)
                troop_manager.troops[order.target_troop_id].current_order = -1
        if self.order_creation != None:
            self.order_creation.tick(mx, my, map, troop_manager, camera)

