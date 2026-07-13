from settings import *
from level_data import LevelData
from map_renderer import MapRenderer
from bsp.bsp_builder import BSPTreeBuilder
from bsp.bsp_traverser import BSPTreeTraverser
from camera import Camera
from input_handler import InputHandler
from view_renderer import ViewRenderer
from collision_handler import CollisionHandler
from player import Player
from UI import PlayerUI

class Engine:
    def __init__(self,app):
        self.app = app
        #
        self.level_data = LevelData(self)
        self.bsp_builder = BSPTreeBuilder(self)
        #
        self.collision_handler = CollisionHandler(self)
        self.camera = Camera(self)
        self.player = Player(self)
        self.input_handler = InputHandler(self)
        #
        self.bsp_traverser = BSPTreeTraverser(self)
        self.map_renderer = MapRenderer(self)
        self.view_renderer = ViewRenderer(self)
        #
        self.player_ui = PlayerUI(self.player)
        

    def update(self):
        self.player.update()
        self.camera.pre_update()
        #
        self.input_handler.update()
        #
        self.camera.update()
        self.bsp_traverser.update()
        self.view_renderer.update()
        
    def draw_2d(self):
        if self.map_renderer.should_draw:
            self.map_renderer.draw() 
        else:
            draw_fps (10,10)

    def draw_3d(self):
        begin_mode_3d(self.camera.m_cam)
        #
        self.view_renderer.draw()
        #
        end_mode_3d()

    def draw_damage_feedback(self):
        if self.player.last_damage_time > 0:
            alpha = int(150 * (self.player.last_damage_time / self.player.damage_flash_duration))

            draw_rectangle(0, 0, WIN_WIDTH, WIN_HEIGHT, Color(255, 0, 0, alpha))
    

    def draw(self):
        begin_drawing()
        #
        clear_background(BLACK)
        self.draw_3d()
        self.draw_2d()
        

        # /// Visual effects for Player UI
        self.draw_damage_feedback()
        self.player_ui.draw()
        #
        self.player.draw()
        end_drawing()


