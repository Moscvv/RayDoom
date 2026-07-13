from settings import *
from data_types import BSPNode, Segment
from utils import is_on_front


class BSPTreeTraverser:
    def __init__(self, engine):
        self.engine = engine
        self.root_node = engine.bsp_builder.root_node
        self.segments = engine.bsp_builder.segments

        self.camera = engine.camera
        self.pos_2d = self.camera.pos_2d
        #
        self.seg_ids_to_draw = []
        self.masked_seg_ids_to_draw = []

    def update(self):
        self.seg_ids_to_draw.clear()
        self.masked_seg_ids_to_draw.clear()
        self.traverse(self.root_node)

    def traverse(self, node: BSPNode):
        if node is None:
            return None

        on_front = is_on_front(self.pos_2d - node.splitter_p0, node.splitter_vec)
        #
        if on_front:
            self.traverse(node.front)
            #
            self.seg_ids_to_draw.append(node.segment_id)
            #
            self.traverse(node.back)
        else:
            self.traverse(node.back)
            #
            self.traverse(node.front)        

    #trying to create collition between walls
    def check_collision(self, position: Vector3) -> bool:
    #"""Check if a 3D point collides with solid geometry."""
        node = self._find_leaf_node(position.x, position.z)  # Traverse BSP to find sector
        return node.is_solid or position.y < node.floor_height or position.y > node.ceiling_height     