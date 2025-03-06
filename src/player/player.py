from ursina import Entity, Vec3, time, held_keys, mouse, color, clamp
from src.physics.collision_system import CollisionSystem
from src.physics.slope_handler import SlopeHandler
from src.audio.footstep_system import FootstepSystem
from src.player import camera
from src.player.head_bob import HeadBob
from src.weapons.weapon_manager import WeaponManager
from src.config import PLAYER_HEIGHT, FOV, MOUSE_SENSITIVITY, PLAYER_SPEED, PLAYER_RUNNING_SPEED, PLAYER_JUMP_HEIGHT, CAMERA_MIN_ANGLE, CAMERA_MAX_ANGLE

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.setup_player()
        self.setup_camera()
        self.setup_controls()
        self.setup_physics()
        self.weapon_manager = WeaponManager(self)
        
        # Initialize new systems
        self.collision_system = CollisionSystem()
        self.slope_handler = SlopeHandler()
        self.footstep_system = FootstepSystem(self)
        self.head_bob = HeadBob(camera)
        
        # Movement state
        self.velocity = Vec3(0, 0, 0)
        self.running = False
        self.grounded = False

    def update(self):
        self.handle_movement()
        self.handle_camera()
        self.apply_gravity()
        self.update_systems()

    def handle_movement(self):
        # Get movement direction
        direction = Vec3(0, 0, 0)
        if held_keys['w']: direction += self.forward
        if held_keys['s']: direction -= self.forward
        if held_keys['a']: direction -= self.right
        if held_keys['d']: direction += self.right

        # Normalize direction and apply speed
        if direction.length() > 0:
            direction = direction.normalized()
        
        self.running = held_keys['shift']
        speed = PLAYER_RUNNING_SPEED if self.running else PLAYER_SPEED
        self.velocity.x = direction.x * speed
        self.velocity.z = direction.z * speed

        # Handle jumping
        if held_keys['space'] and self.grounded:
            current_time = time.time()
            if current_time - self.last_jump >= self.jump_cooldown:
                self.velocity.y = self.jump_height
                self.grounded = False
                self.last_jump = current_time

    def handle_camera(self):
        # Horizontal rotation
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[0] * time.dt

        # Vertical rotation
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[1] * time.dt
        self.camera_pivot.rotation_x = clamp(
            self.camera_pivot.rotation_x, 
            CAMERA_MIN_ANGLE, 
            CAMERA_MAX_ANGLE
        )

    def apply_gravity(self):
        # Apply gravity
        if not self.grounded:
            self.velocity.y -= self.gravity * time.dt
            self.position.y += self.velocity.y * time.dt

        # Ground check
        if self.position.y < 1:
            self.position.y = 1
            self.velocity.y = 0
            self.grounded = True

    def update_systems(self):
        # Handle slope movement
        self.velocity = self.slope_handler.handle_slope(
            self,
            self.velocity,
            time.dt
        )
        
        # Check collisions and update position
        new_pos, hit_normal = self.collision_system.check_collision(
            self,
            self.velocity,
            time.dt
        )
        self.position = new_pos
        
        # Update grounded state
        self.grounded = hit_normal is not None and hit_normal.y > 0
        
        # Update footsteps
        self.footstep_system.update()
        
        # Update head bobbing
        self.head_bob.update(
            time.dt,
            self.velocity,
            self.running,
            self.grounded
        )

    def setup_player(self):
        model = 'cube'  # Temporary model for collision
        self.position = Vec3(0, 1, 0)
        self.scale_y = PLAYER_HEIGHT
        self.collider = 'box'
        self.visible = False

    def setup_camera(self):
        camera.parent = self
        camera.position = (0, 2, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = FOV
        mouse.locked = True
        self.mouse_sensitivity = MOUSE_SENSITIVITY
        self.camera_pivot = Entity(parent=self, y=2)

        # Add crosshair
        self.crosshair = self.Entity(
            parent=camera.ui,
            model='quad',
            scale=.008,
            color=color.white,
            rotation_z=45
        )

    def setup_controls(self):
        self.walking = False
        self.running = False
        self.grounded = False
        
    def setup_physics(self):
        self.velocity = Vec3(0, 0, 0)
        self.gravity = 9.81
        self.jump_height = PLAYER_JUMP_HEIGHT
        self.jump_duration = 0.5
        self.jump_cooldown = 0.1
        self.last_jump = 0

    def input(self, key):
        if key == 'escape':
            mouse.locked = not mouse.locked