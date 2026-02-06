from grid_helper import screen_to_map_coords
from order.order_manager import OrderManager
from order.orders import Order, GO_TO_TYPE, GoTo
from troop.troops_manager import TroopsManager

def order_creation_update(mx: int, my: int, camera, troop_id: int, creation_order_type: int, orders: OrderManager) -> Order:
    x, y = screen_to_map_coords(mx, my, camera)
    if creation_order_type == GO_TO_TYPE:
        order = GoTo(troop_id, x, y)
        orders.order_creation = order

def order_creation_finish(orders: OrderManager, troops_manager: TroopsManager):
    current = orders.order_creation
    if current is None:
        return
    troop = troops_manager.troops[current.target_troop_id]
    if troop.current_order != -1:
        orders.remove_order(troop.current_order)
    id = len(orders.orders)
    orders.add_order(current)
    troop.current_order = id
    orders.order_creation = None
