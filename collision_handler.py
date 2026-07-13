from settings import *
from data_types import Segment

class CollisionHandler:
    def __init__(self, engine):
        self.engine = engine
        self.player_radius = 0.3  # adjust based on scale
        self.debug_mode = False   # Set to True to print debugging info

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
            return False
            
        # If this is a portal, check if player can pass through
        if segment.back_sector_id is not None:
            # Get sector information
            front_sector = self.engine.level_data.sectors[segment.sector_id]
            back_sector = self.engine.level_data.sectors[segment.back_sector_id]
            
            # Player position data
            player_feet_y = self.engine.camera.pos_3d.y
            player_height = CAM_HEIGHT
            player_head_y = player_feet_y + player_height
            player_eye_level = player_feet_y + player_height * 0.85  # Approximate eye level
            
            # Determine which sector the player is currently in
            # This helps determine which way we're trying to cross the portal
            current_sector_id = self._get_player_current_sector()
            is_entering_back = (current_sector_id == segment.sector_id)
            
            # Get the sector we're trying to enter
            target_sector = back_sector if is_entering_back else front_sector
            current_sector = front_sector if is_entering_back else back_sector
            
            # Max height the player can step up
            max_step_height = 0.5
            
            # Check portal passability
            passable = True
            
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
            
            # For passable portals, we still need to check if we're colliding with the wall
            if passable:
                # Check if we're actually colliding with the wall segment
                if self._check_wall_collision(segment, new_pos_2d):
                    # Automatically adjust player height when passing through portals with different floor heights
                    if is_close_to_segment(segment, new_pos_2d, threshold=0.05):  # Extra close check for transition
                        # If we're very close to a passable portal with a different floor height,
                        # adjust the player's height to match the new floor
                        if abs(floor_diff) > 0.05:  # Only adjust if there's a significant difference
                            # Schedule a height adjustment for the next frame
                            self.engine.camera.scheduled_height_adjust = floor_diff
                    return False  # No collision, allow passage
            
            # For impassable portals, treat as a wall
            if not passable:
                return self._check_wall_collision(segment, new_pos_2d)
        
        # For solid walls
        return self._check_wall_collision(segment, new_pos_2d)
    
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

        # Vector from p0 to p1
        wall_vec = p1 - p0
        wall_length = length(wall_vec)
        wall_dir = wall_vec / wall_length

        # Vector from wall start to player position
        to_player = new_pos_2d - p0

        # Project player position onto the wall line
        proj_length = dot(to_player, wall_dir)

        # Closest point on the wall line to the player
        if proj_length < 0:
            closest = p0
        elif proj_length > wall_length:
            closest = p1
        else:
            closest = p0 + wall_dir * proj_length

        # Distance from player to the closest point on the wall
        dist = length(new_pos_2d - closest)

        # Collision if distance is less than player radius
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
        
# Helper function for extra close proximity check
def is_close_to_segment(segment, pos, threshold=0.05):
    p0, p1 = segment.pos
    
    # Vector from p0 to p1
    wall_vec = p1 - p0
    wall_length = length(wall_vec)
    wall_dir = wall_vec / wall_length
    
    # Vector from wall start to player position
    to_player = pos - p0
    
    # Project player position onto the wall line
    proj_length = dot(to_player, wall_dir)
    
    # Closest point on the wall line to the player
    if proj_length < 0:
        closest = p0
    elif proj_length > wall_length:
        closest = p1
    else:
        closest = p0 + wall_dir * proj_length
    
    # Distance from player to the closest point on the wall
    dist = length(pos - closest)
    
    # Return true if very close
    return dist < threshold
                          