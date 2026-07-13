from settings import *
from glm import vec3, normalize, cross
from input_handler import Key
from weapon_sprite import WeaponSprite
import math

class Player:
    def __init__(self, engine):
        self.engine = engine
        self.camera = engine.camera
        self.collision_handler = engine.collision_handler
        
        # Player state
        self.health = 100
        self.speed = CAM_SPEED  # From settings
        self.is_attacking = False
        self.current_action = 'idle'
        
        # Movement vectors
        self.velocity = vec3(0)
        self.forward = vec3(0)
        self.right = vec3(0)

        # Attack UI
        self.attack_cooldown = 0.0
        self.attack_duration = 1.5
        self.last_damage_time = 0.0
        self.damage_flash_duration = 0.2

        #
        self.weapon = WeaponSprite(self)

        #
        self.footstep_timer = 0.0
        self.footstep_interval = 0.5 # time between footsteps in seconds
        #
        self.load_footstep_sounds()

        
    def handle_input(self):
        # Movement input
        self.velocity = vec3(0)
        
        if is_key_down(Key.FORWARD):
            self.velocity += self.forward
        if is_key_down(Key.BACK):
            self.velocity -= self.forward
        if is_key_down(Key.STRAFE_RIGHT):
            self.velocity += self.right
        if is_key_down(Key.STRAFE_LEFT):
            self.velocity -= self.right
            
        # Normalize diagonal movement
        if length(self.velocity) > 0:
            self.velocity = normalize(self.velocity) * self.speed * self.engine.app.dt
            
        # Attack action
        if is_key_pressed(Key.ATTACK):  # Add SPACE to Key enum
            self.attack()
            
    def attack(self):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 0.7 # 1 second cooldown
            self.current_action = 'attacking'
    
        
    def update_vectors(self):
        # Sync with camera orientation
        self.forward = self.camera.get_forward()
        self.right = cross(self.forward, self.camera.fake_up)

    def load_footstep_sounds(self):
            
            self.footstep_sounds =[
                load_sound("assets/sounds/footsteps1.wav")
                #load_sound("assets/sounds/footstep2.wav"),
                #load_sound("assets/sounds/footstep3.wav"),
                #load_sound("assets/sounds/footstep4.wav")
            ]

    def update(self):
        dt = self.engine.app.dt
        self.handle_input()
        self.update_vectors()
        self.move()
        self.update_state()

        #
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.last_damage_time = max(0, self.last_damage_time - dt)
        #
        if self.is_attacking and self.attack_cooldown <= (1.0 - self.attack_duration):
            self.is_attacking = False

        #
        self.weapon.update(self.engine.app.dt)

        #
        self.update_footsteps(dt)  

    def update_footsteps(self, dt):
        # Only process footsteps when moving
        if length(self.velocity) > 0:
            self.footstep_timer += dt
        
            # Adjust footstep interval based on speed if needed
            # self.footstep_interval = 0.5 / (length(self.velocity) / self.speed)
        
            if self.footstep_timer >= self.footstep_interval:
                self.footstep_timer = 0
            
                # Play random footstep sound if available
                if hasattr(self, 'footstep_sounds') and self.footstep_sounds:
                    random_sound = self.footstep_sounds[get_random_value(0, len(self.footstep_sounds) - 1)]
                    play_sound(random_sound)
            
                # Add small vertical camera impact
                self.camera.add_impact(0.01)  # Smaller value for subtle effect

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        self.last_damage_time = self.damage_flash_duration        
        
    def move(self):
        if length(self.velocity) == 0:
            return
            
        # Convert 3D velocity to 2D for collision detection
        desired_pos_2d = self.camera.pos_2d + vec2(self.velocity.x, self.velocity.z)
        allowed_pos_2d = self.collision_handler.get_slide_position(
            self.camera.pos_2d, 
            desired_pos_2d
        )
        
        # Update camera position (player and camera share position)
        dx = allowed_pos_2d.x - self.camera.pos_2d.x
        dz = allowed_pos_2d.y - self.camera.pos_2d.y
        
        self.camera.move_x(dx)
        self.camera.move_z(dz)
        
    def update_state(self):
        self.current_action = 'run' if length(self.velocity) > 0 else 'idle'

    def get_animation_state(self):
        if self.is_attacking:
            return 'attack'
        #
        if length(self.velocity) > 0:
            return 'run'
        return 'idle'

    
    def calculate_screen_position(self):
        # Move sprite 1.5 units in front of camera along its forward vector
        forward_offset = self.camera.get_forward() 
        world_pos_glm = glm.vec3(
            self.camera.pos_3d.x + forward_offset.x,
            self.camera.pos_3d.y + CAM_HEIGHT - 0.2,  # Adjust vertical position
            self.camera.pos_3d.z + forward_offset.z
        )
    
        # Convert to pyray Vector3
        world_pos = Vector3(
            float(world_pos_glm.x),
            float(world_pos_glm.y),
            float(world_pos_glm.z)
        )
    
        return get_world_to_screen(world_pos, self.camera.m_cam)
    

    def draw(self):
        self.weapon.draw()
