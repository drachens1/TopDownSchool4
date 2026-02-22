import math

class Combat:
    def __init__(self, troop_a_id: int, troop_b_id: int):
        self.participants = {troop_a_id, troop_b_id}
        self.finished = False

    def add_participant(self, troop_id: int):
        self.participants.add(troop_id)

    def tick(self, troop_manager, order_manager):
        self.participants = {tid for tid in self.participants if troop_manager.troops[tid].hp > 0}

        if len(self.participants) < 2:
            self.finished = True
            return

        friendlies = [t for t in self.participants if troop_manager.troops[t].friendly]
        enemies = [t for t in self.participants if not troop_manager.troops[t].friendly]

        if not friendlies or not enemies:
            self.finished = True
            return

        for f_id in friendlies:
            target_id = enemies[0]
            self._execute_attack(f_id, target_id, troop_manager, order_manager)

        for e_id in enemies:
            target_id = friendlies[0]
            self._execute_attack(e_id, target_id, troop_manager, order_manager)

    def _execute_attack(self, attacker_id, victim_id, troop_manager, order_manager):
        attacker = troop_manager.troops[attacker_id]
        victim = troop_manager.troops[victim_id]

        victim.take_damage(1, order_manager)

        ax, ay = troop_manager.cell_to_xy(attacker.cell)
        vx, vy = troop_manager.cell_to_xy(victim.cell)

        dx = ax - vx
        dy = ay - vy

        target_rad = math.atan2(dy, dx)
        desired_angle = int((target_rad + math.pi + math.pi/8) / (math.pi/4)) % 8

        if victim.angle != desired_angle:
            diff = (desired_angle - victim.angle + 8) % 8
            if diff <= 4:
                victim.angle = (victim.angle + 1) % 8
            else:
                victim.angle = (victim.angle - 1 + 8) % 8