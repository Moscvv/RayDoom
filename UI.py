from settings import *

class PlayerUI:
    def __init__(self, player):
        self.player = player
        
    def draw_health_bar(self):
        # Health bar background
        draw_rectangle(20, 20, 200, 30, Color(*DARKGREEN))
        # Current health
        health_width = int(200 * (self.player.health / 100))
        draw_rectangle(20, 20, health_width, 30, Color(*RED))
        # Health text
        draw_text(f"HP: {self.player.health}", 20, 55, 20, DARK_RED)

    def draw_action_indicator(self):
        action_text = f"Action: {self.player.current_action.upper()}"
        draw_text(action_text, 20, 80, 20, BLUE)

    def draw(self):
        self.draw_health_bar()
        self.draw_action_indicator()