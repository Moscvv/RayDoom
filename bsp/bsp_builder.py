from settings import *
from data_types import Segment, BSPNode
from utils import cross_2d
from copy import copy
import random


class BSPTreeBuilder:
    def __init__(self, engine):
        self.engine = engine
        self.raw_segments = engine.level_data.raw_segments
        #
        self.root_node = BSPNode()
        #
        self.segments = [] # segments created during BSP tree creation
        self.seg_id = 0
        #
        #seed = self.find_best_seed()
        seed = self.engine.level_data.settings['seed']
        random.seed(seed)
        random.shuffle(self.raw_segments)
        #
        self.num_front, self.num_back, self.num_splits = 0, 0, 0
        self.build_bsp_tree(self.root_node, self.raw_segments)
        #
        print('num_front:', self.num_front)
        print('num_back:', self.num_back)
        print('num_splits', self.num_splits)

    def find_best_seed(self, start_seed=0, end_seed=20_000, weight_factor=3):
        best_seed, best_score = -1, float('inf')
        #
        for seed in range(start_seed, end_seed):
            raw_segments = self.raw_segments.copy()
            random.seed(seed)
            random.shuffle(raw_segments)
            #
            root_node = BSPNode ()
            self.segments = []
            self.seg_id = 0
            #
            self.num_front, self.num_back, self.num_splits = 0, 0, 0
            self.build_bsp_tree(root_node, raw_segments)
            #
            score = abs(self.num_back - self.num_front) + weight_factor * self.num_splits
            if score < best_score:
                best_seed, best_score = seed, score  
        #
        print('best_seed =', best_seed, 'score = ', best_score)
        return best_seed             

    def split_space(self, node: BSPNode, input_segments: list[Segment]):
        splitter_seg = input_segments[0]
        splitter_pos = splitter_seg.pos
        splitter_vec = splitter_seg.vector

        node.splitter_vec = splitter_vec
        node.splitter_p0 = splitter_pos[0]
        node.splitter_p1 = splitter_pos[1]
        
        front_segs, back_segs = [], [] 

        for segment in input_segments[1:]:
            #
            segment_start = segment.pos[0]
            segment_end = segment.pos[1]
            segment_vector = segment.vector

            numerator = cross_2d((segment_start - splitter_pos[0]), splitter_vec)
            denominator = cross_2d(splitter_vec, segment_vector)

            # if the denominator is zero the line are parallel
            denominator_is_zero = abs(denominator) < EPS

            # segments are collinear if they are paraller and the numerator is zero
            numerator_is_zero = abs(numerator) < EPS
            #
            if denominator_is_zero and numerator_is_zero:
                front_segs.append(segment)
                continue

            if not denominator_is_zero:
                # intersection is the point on a line segment where the lines divides it
                intersection = numerator / denominator
                
                # segments that are not parallel and t is in (0,1) should be divided
                if 0.0 < intersection < 1.0:
                    self.num_splits += 1
                    #
                    intersection_point = segment_start + intersection * segment_vector

                    r_segment = copy(segment)
                    r_segment.pos = segment_start, intersection_point
                    r_segment.vector = r_segment.pos[1] - r_segment.pos[0]
                    #
                    l_segment = copy(segment)
                    l_segment.pos = intersection_point, segment_end
                    l_segment.vector = l_segment.pos[1] - l_segment.pos[0]

                    if numerator > 0:
                        l_segment, r_segment = r_segment, l_segment
                    #
                    front_segs.append(r_segment)
                    back_segs.append(l_segment)
                    continue

            if numerator < 0 or (numerator_is_zero and denominator > 0):
                front_segs.append(segment)
            #
            elif numerator > 0 or (numerator_is_zero and denominator < 0):
                back_segs.append(segment)

        self.add_segment(splitter_seg, node)
        return front_segs, back_segs                    
    
    def add_segment(self, splitter_seg: Segment, node: BSPNode):
        self.segments.append(splitter_seg)
        node.segment_id = self.seg_id
        #
        self.seg_id += 1


    def build_bsp_tree(self, node: BSPNode, input_segments: list[Segment]):
        if not input_segments:
            return None
        #
        front_segs, back_segs = self.split_space(node, input_segments)

        if back_segs:
            self.num_back += 1
            #
            node.back = BSPNode()
            self.build_bsp_tree(node.back, back_segs)

        if front_segs:
            self.num_front += 1
            #
            node.front = BSPNode()
            self.build_bsp_tree(node.front, front_segs)    
