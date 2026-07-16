from settings import *

def cross_2d(vec_0: vec2, vec_1: vec2):
    return vec_0.x * vec_1.y - vec_1.x * vec_0.y

def is_on_front(vec_0: vec2, vec_1: vec2):
    # whether vec_0 is on the front side relative to vec_1
    return vec_0.x * vec_1.y < vec_1.x * vec_0.y 

def is_on_back(vec_0: vec2, vec_1: vec2):
    return not is_on_front(vec_0, vec_1)

def closest_point_on_segment(p0, p1, point):
    
    #Returns (closest_point, distance) from 'point' to the segment p0-p1.

    wall_vec = p1 - p0
    wall_length = length(wall_vec)
    wall_dir = wall_vec / wall_length
    
    to_point = point - p0
    proj_length = dot(to_point, wall_dir)
    
    if proj_length < 0:
        closest = p0
    elif proj_length > wall_length:
        closest = p1
    else:
        closest = p0 + wall_dir * proj_length
    
    dist = length(point - closest)
    return closest, dist
                          