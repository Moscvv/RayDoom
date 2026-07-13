from settings import *
from texture_id import *

_ = None


SETTINGS = {
    'seed': 4,
    'cam_pos': (1, CAM_HEIGHT, 1),
    'cam_target': (5, CAM_HEIGHT, 5)
}   


# points
P_00 = (0.0, -3.0)
P_01 = (7.0, 0.0)
P_02 = (12.0, -3.0)
P_03 = (12.0, 9.0)
P_04 = (7.0, 6.0)
P_05 = (0.0, 9.0)
#
P_06 = (5.0, 2.5)
P_07 = (4.5, 2.5)
P_08 = (4.5, 3.0)
P_09 = (5.0, 3.0)
# sector 2
P_10 = (9.0, 1.0)
P_11 = (11.0, 1.0)
P_12 = (11.0, 5.0)
P_13 = (9.0, 5.0)



SECTOR_DATA = {
    0: dict(
        floor_h=0.0, ceil_h=3.5,
        floor_tex_id=FlatTexID.TEST_3, ceil_tex_id=FlatTexID.TEST_5,
    ),
    1: dict(
        floor_h=0.5, ceil_h=4.0,
        ceil_tex_id=FlatTexID.TEST_4,
        nested_sector_ids=[2, ],
    ),
    2: dict(
        floor_h=1.0, ceil_h=3.0,
        floor_tex_id=FlatTexID.TEST_3, ceil_tex_id=FlatTexID.TEST_4,
    ),
}


SEGMENTS_OF_SECTOR_BOUNDARIES = [
    # seg points(p0 p1), sector ids(front sector, back sector adj), textures (lo mid up)

    # sector 0 
    [(P_00, P_01), (0, _), (_, _, _)],
    [(P_04, P_05), (0, _), (_, _, _)],
    [(P_05, P_00), (0, _), (_, _, _)],

    # sector 0 1
    [(P_01, P_04), (0, 1), (WallTexID.TEST_2, _, WallTexID.TEST_2)],

    # sector 1
    [(P_01, P_02), (1, _), (_, WallTexID.TEST_1, _)],
    [(P_02, P_03), (1, _), (_, WallTexID.TEST_1, _)], 
    [(P_03, P_04), (1, _), (_, WallTexID.TEST_1, _)],

    # sector 2 (nested in 1)
    [(P_11, P_10), (1, 2), (_, WallTexID.TEST_7, _)],
    [(P_12, P_11), (1, 2), (_, WallTexID.TEST_7, _)],
    [(P_13, P_12), (1, 2), (_, WallTexID.TEST_7, _)],
    [(P_10, P_13), (1, 2), (_, WallTexID.TEST_7, _)],

]

SEGMENTS_WITHIN_SECTORS = [
    # sector 0
    # column
    [(P_06, P_07), (0, _), (_, WallTexID.TEST_3, _)],
    [(P_07, P_08), (0, _), (_, WallTexID.TEST_3, _)],
    [(P_08, P_09), (0, _), (_, WallTexID.TEST_3, _)],
    [(P_09, P_06), (0, _), (_, WallTexID.TEST_3, _)],
]




