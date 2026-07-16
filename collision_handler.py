from settings import *
from data_types import Segment
from utils import *

class CollisionHandler:
    def __init__(self, engine):
        self.engine = engine
        self.player_radius = 0.3  # adjust based on scale
        self.debug_mode = True   # Set to True/Flase to print(not print) debugging info
        self.last_adjusted_segment = None

    def check_collision(self, new_pos_2d):
        # // Check if the new position would cause a collision with any wall ///
        segments = self.engine.bsp_builder.segments

        for segment in segments:
            if self.check_segment_collision(segment, new_pos_2d):
                return True
        return False
    
    def check_segment_collision(self, segment: Segment, new_pos_2d):
        # First check if we're even near this wall segment
        if not self._is_close_to_segment(segment, new_pos_2d):
           #free to trigger again later on?
            if segment is self.last_adjusted_segment:
                self.last_adjusted_segment = None
            return False
        
        if segment.back_sector_id is None:
            #solid wall
            return self._check_wall_collision(segment, new_pos_2d)
        
        # portal
        passable, floor_diff = self._is_portal_passable(segment, new_pos_2d)

        if passable:
            if self._check_wall_collision(segment, new_pos_2d):
                self._maybe_schedule_height_adjust(segment, new_pos_2d, floor_diff)
            return False # allow passage
        
        return self._check_wall_collision(segment, new_pos_2d)
             
    
    def _is_portal_passable(self, segment, new_pos_2d):
            front_sector = self.engine.level_data.sectors[segment.sector_id]
            back_sector = self.engine.level_data.sectors[segment.back_sector_id]
            
            # Player position data
            player_feet_y = self.engine.camera.pos_3d.y
            player_height = CAM_HEIGHT
            player_head_y = player_feet_y + player_height
            
            # This helps determine which way we're trying to cross the portal
            is_entering_back = self._is_entering_back(segment, new_pos_2d)
            
            # Get the sector we're trying to enter
            target_sector = back_sector if is_entering_back else front_sector
            current_sector = front_sector if is_entering_back else back_sector
            

            max_step_height = 0.5  # Max height the player can step up
            passable = True    # Check portal passability

            # Check if the floor is too high to step up
            floor_diff = target_sector.floor_h - current_sector.floor_h
            if floor_diff > max_step_height:
                if self.debug_mode:
                    print(f"Floor too high: {floor_diff} (max: {max_step_height})")
                passable = False
            
            # Check if the ceiling is too low
            if target_sector.ceil_h < player_head_y:
                if self.debug_mode:
                    print(f"Ceiling too low: {target_sector.ceil_h} < {player_head_y}")
                passable = False
            
            # Check if portal opening is tall enough
            portal_height = target_sector.ceil_h - target_sector.floor_h
            if portal_height < player_height:
                if self.debug_mode:
                    print(f"Portal opening too small: {portal_height} < {player_height}")
                passable = False

            return passable, floor_diff
       

    def _maybe_schedule_height_adjust(self, segment, new_pos_2d, floor_diff):  
        _, dist_to_wall = closest_point_on_segment(*segment.pos, new_pos_2d)
        if dist_to_wall <0.05:

        # If we're very close to a passable portal with a different floor height,
        # adjust the player's height to match the new floor
                        
            if abs(floor_diff) > 0.05:  # Only adjust if there's a significant difference
                # Schedule a height adjustment for the next frame
                if segment is not self.last_adjusted_segment:
                    if self.debug_mode:
                         print(f"SETTING height adjust: {floor_diff}")
                    self.engine.camera.scheduled_height_adjust = floor_diff
                    self.last_adjusted_segment = segment
            
    
    def _is_close_to_segment(self, segment, pos, threshold=1.0):
        """Quick check to see if a position is close enough to a segment to bother with collision"""
        p0, p1 = segment.pos
        # Get bounding box of segment with some margin
        min_x = min(p0.x, p1.x) - threshold
        max_x = max(p0.x, p1.x) + threshold
        min_y = min(p0.y, p1.y) - threshold
        max_y = max(p0.y, p1.y) + threshold
        
        # Check if position is within bounding box
        return (min_x <= pos.x <= max_x) and (min_y <= pos.y <= max_y)
    
    def _is_entering_back(self, segment, pos):
        """Which side of this segment's line is 'pos' on - front or back?"""
        p0, p1 = segment.pos
        wall_vec = p1 - p0
        to_pos = pos - p0
        cross = wall_vec.x * to_pos.y - wall_vec.y * to_pos.x
        print(f"cross={cross}")
        return cross > 0
    
    def _get_player_current_sector(self):
        """Determine which sector the player is currently in"""
        pos_2d = self.engine.camera.pos_2d
        # This is a simplified approach - in a real engine you'd use the BSP
        # tree to efficiently determine which sector contains the point
        
        # For now, check based on which sectors the player is inside
        for sector_id, sector in self.engine.level_data.sectors.items():
            if self._point_in_sector(pos_2d, sector_id):
                return sector_id
                
        # Fallback to a default sector if not found
        return 0  # Assuming sector 0 is always valid
        
    def _point_in_sector(self, point, sector_id):
        """Check if a point is inside a sector"""
        # This is a simplified approach
        # In a real engine, you'd use point-in-polygon tests with the sector's outline
        
        # For now, assume each sector has a bounding box or explicit check
        # This would need to be implemented based on your sector data structure
        
        # Since we don't have the full implementation, return a placeholder
        # You would replace this with actual sector boundary checks
        sector = self.engine.level_data.sectors[sector_id]
        # Return True if point is inside sector boundary
        return True  # Placeholder - replace with actual check
    
    def _check_wall_collision(self, segment, new_pos_2d):
        # Helper method to check actual wall collision geometry
        p0, p1 = segment.pos
        _, dist = closest_point_on_segment(p0, p1, new_pos_2d)
        return dist < self.player_radius


    def get_slide_position(self, current_pos, desired_pos):
        # /// If collision detected, calculate a sliding position /// 
        # Try to slide along the wall
        if self.check_collision(desired_pos):
            # X-axis movement only
            slide_x = vec2(desired_pos.x, current_pos.y)
            if not self.check_collision(slide_x):
                return slide_x
            
            # Z-axis movement only
            slide_z = vec2(current_pos.x, desired_pos.y)
            if not self.check_collision(slide_z):
                return slide_z
            
            # Both failed, don't move
            return current_pos
        
        # No collision, accept the move
        return desired_pos
        
    
   