from pyray import *
import os
import math
from settings import *

class WeaponSprite:
    def __init__(self, player):
        self.player = player
        self.is_visible = True
        self.scale = 4.0  # Increased from 2.0 to make the weapon larger
        self.position = Vector2(WIN_WIDTH // 2, WIN_HEIGHT - 200)
        
        # Animation state
        self.current_animation = 'idle'
        self.current_frame = 0
        self.frame_time = 0
        self.animations = {}
        
        # Calculate weapon position relative to screen
        self.x_offset = 0
        self.y_offset = 0
        self.weapon_bob_amount = 0
        self.weapon_bob_time = 0
        self.weapon_bob_speed = 10.0
        
        # Load animations
        self.load_animations()
        
    def load_animations(self):
        # Define animation configurations
        animation_configs = {
            'idle': {'frames': 1, 'duration': 0.25, 'loop': True},  # Appears to be 1 frame from your images
            'attack': {'frames': 8, 'duration': 0.13, 'loop': False},  # Assuming 6 frames for attack
            'run': {'frames': 1, 'duration': 0.1, 'loop': True}  # Might be the same as idle
        }
        
        # Print current working directory for debugging
        print(f"Current working directory: {os.getcwd()}")
        
        # For each animation type
        for anim_name, config in animation_configs.items():
            frames = []
            print(f"Trying to load animation: {anim_name}")
            
            # Try loading from folder with individual frames first (this seems to be your structure)
            frame_folder = f'assets/weapons/{anim_name}'
            if os.path.exists(frame_folder):
                print(f"Found folder: {frame_folder}")
                frame_files = [f for f in os.listdir(frame_folder) 
                              if f.endswith('.png')]
                
                # Sort frames by number if possible
                try:
                    frame_files.sort(key=lambda f: int(f.split('_')[1].split('.')[0]))
                except:
                    frame_files.sort()  # Basic sort if numbering is different
                
                print(f"Found {len(frame_files)} files: {frame_files}")
                
                for frame_file in frame_files:
                    frame_path = os.path.join(frame_folder, frame_file)
                    texture = load_texture(frame_path)
                    source_rect = Rectangle(0, 0, texture.width, texture.height)
                    frames.append((texture, source_rect))
                    print(f"Loaded frame: {frame_path}")
            else:
                print(f"Folder {frame_folder} not found, trying alternative methods...")
                
                # Try loading from spritesheet
                spritesheet_path = f'assets/weapons/{anim_name}.png'
                if os.path.exists(spritesheet_path):
                    print(f"Found spritesheet: {spritesheet_path}")
                    # Load from spritesheet
                    texture = load_texture(spritesheet_path)
                    frame_width = texture.width // config['frames']
                    frame_height = texture.height
                    
                    for i in range(config['frames']):
                        source_rect = Rectangle(i * frame_width, 0, frame_width, frame_height)
                        frames.append((texture, source_rect))
                        print(f"Loaded frame {i} from spritesheet")
                else:
                    print(f"Spritesheet {spritesheet_path} not found, trying individual files...")
                    
                    # Try loading individual files with pattern anim_name_0.png, anim_name_1.png, etc.
                    for i in range(config['frames']):
                        frame_path = f'assets/weapons/{anim_name}_{i}.png'
                        if os.path.exists(frame_path):
                            print(f"Found individual frame: {frame_path}")
                            texture = load_texture(frame_path)
                            source_rect = Rectangle(0, 0, texture.width, texture.height)
                            frames.append((texture, source_rect))
                            print(f"Loaded individual frame: {frame_path}")
                        else:
                            print(f"Individual frame {frame_path} not found")
            
            if frames:
                print(f"Successfully loaded {len(frames)} frames for {anim_name}")
                self.animations[anim_name] = {
                    'frames': frames,
                    'duration': config['duration'],
                    'loop': config['loop']
                }
            else:
                print(f"WARNING: Could not load any frames for animation '{anim_name}'")
        
        # If no animations were loaded, create a placeholder
        if not self.animations:
            print("No weapon animations found. Creating placeholder.")
            img = gen_image_color(64, 64, RED)
            texture = load_texture_from_image(img)
            unload_image(img)
            
            source_rect = Rectangle(0, 0, texture.width, texture.height)
            self.animations['idle'] = {
                'frames': [(texture, source_rect)],
                'duration': 0.15,
                'loop': True
            }
    
    def set_animation(self, animation_name):
        """Set the current animation if it's available and different from current"""
        if animation_name in self.animations and self.current_animation != animation_name:
            print(f"Setting animation from {self.current_animation} to {animation_name}")
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_time = 0
        elif animation_name not in self.animations:
            print(f"WARNING: Animation {animation_name} not available")
    
    def update(self, dt):
        # Update animation based on player state
        player_state = self.player.get_animation_state()
       # print(f"Player state: {player_state}, Current animation: {self.current_animation}, Is attacking: {self.player.is_attacking}")
        
        # Set animation based on state
        if player_state != self.current_animation:
            print(f"Changing animation from {self.current_animation} to {player_state}")
            self.set_animation(player_state)
        
        # Update weapon bob when moving
        if player_state == 'run':
            self.weapon_bob_time += dt * self.weapon_bob_speed
            self.weapon_bob_amount = math.sin(self.weapon_bob_time) * 10.0
        else:
            # Gradually reset weapon bob when idle
            self.weapon_bob_amount *= 0.9
            
        # Update animation frames
        if self.current_animation in self.animations:
            anim = self.animations[self.current_animation]
            frame_count = len(anim['frames'])
            
            if frame_count > 0:  # Ensure we have frames to animate
                self.frame_time += dt
                
                if self.frame_time >= anim['duration']:
                    self.frame_time = 0
                    old_frame = self.current_frame
                    self.current_frame = (self.current_frame + 1) % frame_count if anim['loop'] else min(self.current_frame + 1, frame_count - 1)
                    #print(f"Animation {self.current_animation}: frame changed from {old_frame} to {self.current_frame}")
                    
                    # If attack animation is done, return to idle
                    if self.current_animation == 'attack' and self.current_frame >= frame_count - 1 and not anim['loop']:
                        print("Attack animation completed, returning to idle")
                        self.player.is_attacking = False
                        self.set_animation('idle')
    
        # Weapon breathing effect
        if self.player.get_animation_state() == 'idle':
            self.breathing_time = getattr(self, 'breathing_time', 0) + dt * 0.5
            self.weapon_bob_amount = math.sin(self.breathing_time) * 3.0  # Very subtle movement
            self.x_offset = math.sin(self.breathing_time * 0.3) * 1.0  # Even more subtle side movement            

    def draw(self):
        if not self.is_visible:
           # print("Weapon not visible, skipping draw")
            return
            
        if self.current_animation not in self.animations:
            #print(f"Animation {self.current_animation} not in loaded animations, skipping draw")
            return
            
        anim = self.animations[self.current_animation]
        if not anim['frames']:
            #print(f"No frames in animation {self.current_animation}, skipping draw")
            return
            
        if self.current_frame >= len(anim['frames']):
            #print(f"Frame index {self.current_frame} out of bounds for animation {self.current_animation} with {len(anim['frames'])} frames")
            return
            
        # Debug info
        #print(f"Drawing: {self.current_animation}, frame {self.current_frame}/{len(anim['frames'])-1}, time: {self.frame_time:.2f}/{anim['duration']:.2f}")
        
        texture, source_rect = anim['frames'][self.current_frame]
        
        # Calculate destination rectangle for proper positioning
        scale_factor = self.scale * (WIN_HEIGHT / 1080)  # Scale based on window height
        dest_width = source_rect.width * scale_factor
        dest_height = source_rect.height * scale_factor
        
        # Position at bottom of screen, centered horizontally, adjusted up a bit
        dest_x = (WIN_WIDTH - dest_width) / 2 + self.x_offset
        dest_y = WIN_HEIGHT - dest_height * 1.0 + self.y_offset + self.weapon_bob_amount  # Raised up a bit


        draw_texture_pro(
            texture,
            source_rect,
            Rectangle(dest_x, dest_y, dest_width, dest_height),
            Vector2(0, 0),  # origin
            0,  # rotation
            WHITE
        )