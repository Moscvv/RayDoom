from pyray import * 
import glm
from glm import vec2, vec3, ivec2, normalize, cross, dot, atan2, sin, cos, length, distance2

# resolution
WIN_RES = WIN_WIDTH, WIN_HEIGHT = 1920, 1080
#WIN_RES = WIN_WIDTH, WIN_HEIGHT = 1600, 900

MAP_OFFSET = 50
MAP_WIDTH, MAP_HEIGHT = WIN_WIDTH - MAP_OFFSET, WIN_HEIGHT - MAP_OFFSET

EPS = 1e-4

# camera settings
CAM_HEIGHT = 0.7
CAM_SPEED = 3.0
CAM_ROT_SPEED = 6.0
CAM_DIAG_MOVE_CORR = 1 / pow(2, 0.5)

# frustum
FOV_Y_DEG = 50

#
LIGHT_POS = vec2(-30)

#
VEC3_ZERO = Vector3(0, 0, 0)
VEC2_ZERO = Vector2(0, 0)
#
WHITE_COLOR= Color(255, 255, 255, 255)
BLACK_COLOR= Color(0, 0, 0, 255)
DARK_GRAY_COLOR = Color(80, 80, 80, 255)
#
SHADING_COLOR = Color(220, 220, 220, 255)
SHADING_DARK_COLOR = Color(45, 45, 45, 255)
DARK_RED = Color(255, 0, 0, 139)

#
PITCH_LIMIT_DEG = 89 # hardcoded
PITCH_LIMIT = glm.radians(PITCH_LIMIT_DEG) #- FOV_Y
