from src.physics.collision_system import CollisionSystem
from src.physics.slope_handler import SlopeHandler
from src.audio.footstep_system import FootstepSystem
from src.player.head_bob import HeadBob

class Player(Entity):
    def __init__(self):
        super().__init__()
        # ... existing initialization code ...
        
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
        # Get movement input
        direction = Vec3(0, 0, 0)
        if held_keys['w']: direction += self.forward
        if held_keys['s']: direction -= self.forward
        if held_keys['a']: direction -= self.right
        if held_keys['d']: direction += self.right
        
        # Normalize direction
        if direction.length() > 0:
            direction = direction.normalized()
        
        # Update running state
        self.running = held_keys['shift']
        
        # Calculate movement speed
        speed = (
            self.run_speed if self.running 
            else self.walk_speed
        )
        
        # Apply movement to velocity
        self.velocity.x = direction.x * speed
        self.velocity.z = direction.z * speed
        
        # Apply gravity
        if not self.grounded:
            self.velocity.y -= self.gravity * time.dt
        
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