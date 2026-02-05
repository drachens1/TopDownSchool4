from order.orders import Order

class OrderManager:
    orders: list[Order]
    free_list: list[int]
    order_creation: Order

    def __init__(self):
        self.orders = []
        self.free_list = []
        self.order_creation = None

    def add_order(self, order):
        self.orders.append(order)

    def remove_order(self, order_id: int):
        self.orders.pop(order_id)

    def render(self, WIN, camera):
        for order in self.orders:
            order.render(WIN, camera)
        if self.order_creation != None:
            self.order_creation.render(WIN, camera)

    def tick(self, ):
        for order in self.orders:
            order.tick()
        if self.order_creation != None:
            self.order_creation.tick()

